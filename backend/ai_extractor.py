import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Change: load Gemini API key from .env
load_dotenv()

# Change: configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def ai_extract_fields(raw_text):
    prompt = f"""
Extract meaningful fields from this OCR text.

Return only valid JSON.
Do not include markdown.
Do not include explanation.

If document is Aadhaar, extract:
document_type, name, dob, gender, mobile_number, aadhaar_number, vid, address, pincode.

OCR Text:
{raw_text}
"""

    response = model.generate_content(prompt)

    content = response.text.strip()

    # Change: remove markdown json block if Gemini returns it
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(content)
    except:
        # Change: fallback to extract JSON object from response
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            return json.loads(match.group())

        return {
            "ai_raw_response": content
        }