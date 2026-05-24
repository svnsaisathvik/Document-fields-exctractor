import cv2
import pytesseract
import re
from ai_extractor import ai_extract_fields

def preprocess_image(image_path):
    # Read image
    image = cv2.imread(image_path)

    # Change: convert image to grayscale for better OCR accuracy
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Change: apply thresholding to make text clearer
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return thresh


def extract_fields(text):
    # Change: created dictionary to store separated fields
    fields = {}

    # Change: example DOB extraction
    dob_match = re.search(r'\d{2}[/-]\d{2}[/-]\d{4}', text)
    if dob_match:
        fields["dob"] = dob_match.group()

    # Change: example Aadhaar-like number extraction
    aadhaar_match = re.search(r'\d{4}\s\d{4}\s\d{4}', text)
    if aadhaar_match:
        fields["aadhaar_number"] = aadhaar_match.group()

    # Change: example PAN-like number extraction
    pan_match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', text)
    if pan_match:
        fields["pan_number"] = pan_match.group()

    return fields

def process_image(image_path):
    processed_image = preprocess_image(image_path)

    extracted_text = pytesseract.image_to_string(processed_image)

    ai_fields = ai_extract_fields(extracted_text)

    return {
        "success": True,
        "raw_text": extracted_text,
        "fields": ai_fields
    }