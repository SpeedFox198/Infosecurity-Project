import cv2
import pytesseract as pt
import re
import string

pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

whitelisted_characters = string.ascii_letters + string.digits + " -"
pt_config = fr"-c tessedit_char_whitelist={whitelisted_characters} --psm 6"

CREDIT_CARD_PATTERN = r'(?:4[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|3[47][0-9]{3}[ -]?[0-9]{6}[ -]?[0-9]{5}|3(?:0[0-5]|[68][0-9])[0-9]{3}[ -]?[0-9]{6}[ -]?[0-9]{4}|6(?:011|5[0-9]{2})[0-9]{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}|(?:2131|1800|35\d{3})\d{3}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4})'
NRIC_PATTERN = r'[STst][0-9]{7}[A-Za-z]'


def ocr_scan(path: str) -> bool:
    patterns = [CREDIT_CARD_PATTERN, NRIC_PATTERN]

    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    results = pt.image_to_string(invert, config=pt_config)

    for pattern in patterns:
        if re.search(pattern, results):
            return True

    return False
