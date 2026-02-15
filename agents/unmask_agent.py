from typing import Dict

class UnmaskAgent:
    def run(self, text: str, mapping: Dict[str, str]) -> str:
        for placeholder, original in mapping.items():
            text = text.replace(placeholder, original)
        return text
