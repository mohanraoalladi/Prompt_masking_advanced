from presidio_analyzer import PatternRecognizer, Pattern


class ClientIDRecognizer(PatternRecognizer):
    """Recognizer for Client ID patterns like CUST-0001"""
    def __init__(self):
        patterns = [
            Pattern(
                name="Client ID",
                regex=r"\bCUST[‑-]\d{4}\b",
                score=0.95
            )
        ]
        super().__init__(
            supported_entity="CLIENT_ID",
            patterns=patterns,
        )


class AccountReferenceRecognizer(PatternRecognizer):
    """Recognizer for Account References like ACC-1234-XYZ"""
    def __init__(self):
        patterns = [
            Pattern(
                name="Account Reference",
                regex=r"\bACC[‑-]\d{4}[‑-][A-Z]{3}\b",
                score=0.95
            )
        ]
        super().__init__(
            supported_entity="ACCOUNT_REFERENCE",
            patterns=patterns,
        )


class PhonePlaceholderRecognizer(PatternRecognizer):
    """Recognizer for placeholder phone numbers like 555-0100"""
    def __init__(self):
        patterns = [
            Pattern(
                name="Placeholder Phone",
                regex=r"\b555[‑-]\d{4}\b",
                score=0.90
            )
        ]
        super().__init__(
            supported_entity="PHONE_NUMBER",
            patterns=patterns,
        )


class OrganizationRecognizer(PatternRecognizer):
    """Recognizer for organization names"""
    def __init__(self):
        patterns = [
            Pattern(
                name="Organization",
                regex=r"\b(RaboBank|MySecretClient|InternalProjectX)\b",
                score=0.9
            )
        ]
        super().__init__(
            supported_entity="ORGANIZATION",
            patterns=patterns,
        )
