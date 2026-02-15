from typing import Dict, List, Optional
from presidio_analyzer import AnalyzerEngine, RecognizerResult

from recognizers.custom_dictionary_recognizer import (
    ClientIDRecognizer,
    AccountReferenceRecognizer,
    PhonePlaceholderRecognizer,
    OrganizationRecognizer
)


class MaskingAgent:
    def __init__(self, pii_categories_enabled: Optional[Dict[str, bool]] = None):
        self.analyzer = AnalyzerEngine()
        
        # Register all custom recognizers
        self.analyzer.registry.add_recognizer(ClientIDRecognizer())
        self.analyzer.registry.add_recognizer(AccountReferenceRecognizer())
        self.analyzer.registry.add_recognizer(PhonePlaceholderRecognizer())
        self.analyzer.registry.add_recognizer(OrganizationRecognizer())
        
        self.pii_categories_enabled = pii_categories_enabled or {}

    def run(self, text: str):
        results: List[RecognizerResult] = self.analyzer.analyze(
            text=text,
            language="en",
        )

        # Filter by enabled categories if provided
        if self.pii_categories_enabled:
            results = [
                r for r in results
                if self.pii_categories_enabled.get(r.entity_type, True)
            ]

        # Remove overlapping detections (keep the one with highest score)
        results = self._remove_overlaps(results)

        mapping: Dict[str, str] = {}
        entity_counters: Dict[str, int] = {}
        replacements: List[Dict] = []

        # Build replacement instructions
        for res in results:
            original_value = text[res.start:res.end]
            
            # Track counter per entity type
            if res.entity_type not in entity_counters:
                entity_counters[res.entity_type] = 0
            entity_counters[res.entity_type] += 1
            
            placeholder = f"<{res.entity_type}_{entity_counters[res.entity_type]}>"
            mapping[placeholder] = original_value
            
            # Store replacement info (start, end, placeholder)
            replacements.append({
                'start': res.start,
                'end': res.end,
                'placeholder': placeholder,
                'original': original_value
            })

        # Sort replacements by start position (descending) to avoid index shifts
        replacements.sort(key=lambda x: x['start'], reverse=True)
        
        # Apply replacements from end to start to maintain correct indices
        masked_text = text
        for rep in replacements:
            masked_text = masked_text[:rep['start']] + rep['placeholder'] + masked_text[rep['end']:]

        return masked_text, mapping

    def _remove_overlaps(self, results: List[RecognizerResult]) -> List[RecognizerResult]:
        """Remove overlapping detections intelligently"""
        if not results:
            return results
        
        # Priority order: higher priority = keeps in case of overlap
        priority_map = {
            "CLIENT_ID": 10,
            "ACCOUNT_REFERENCE": 10,
            "ORGANIZATION": 9,
            "PERSON": 8,
            "EMAIL_ADDRESS": 7,
            "PHONE_NUMBER": 7,
            "LOCATION": 6,
            "IP_ADDRESS": 5,
            "CREDIT_CARD": 5,
        }
        
        # Sort by: start position, then by priority (higher first), then by score (higher first)
        sorted_results = sorted(
            results, 
            key=lambda x: (
                x.start, 
                -priority_map.get(x.entity_type, 0),
                -x.score
            )
        )
        
        filtered = []
        for res in sorted_results:
            # Check if this result has significant overlap with any kept result
            has_overlap = False
            for existing in filtered:
                # Calculate overlap
                overlap_start = max(res.start, existing.start)
                overlap_end = min(res.end, existing.end)
                overlap_len = max(0, overlap_end - overlap_start)
                res_len = res.end - res.start
                
                # Only remove if more than 50% overlaps
                if overlap_len > res_len * 0.5:
                    has_overlap = True
                    break
            
            if not has_overlap:
                filtered.append(res)
        
        return filtered

        return masked_text, mapping
