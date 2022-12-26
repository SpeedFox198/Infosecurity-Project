import re


async def mask_sensitive_data(word: str) -> str:
    """
    Detects the following
    Credit cards - Visa, Mastercard, American Express, Diners Club, Discover and JCB
    NRIC
    """
    CREDIT_CARD_NUMBERS_PATTERN = r"(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})"
    NRIC_PATTERN = r"[STst][0-9]{7}[A-Za-z]"

    masked = len(word) * "*"

    if re.fullmatch(CREDIT_CARD_NUMBERS_PATTERN, word) \
            or re.fullmatch(NRIC_PATTERN, word):
        return word.replace(word, masked)

    return word
