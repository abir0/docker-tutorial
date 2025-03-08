import json

from config import settings
from models import PrescriptionData
from openai import OpenAI


class TextExtractor:
    """Handles extraction of structured data from text."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

        self.system_prompt = """
        You are a medical data extraction expert. Extract the following information from the prescription text:
        - Patient name and date of birth
        - Medication name, strength, form, and quantity
        - Dosage instructions (frequency, duration, special instructions)
        - Prescriber name and ID
        - Date written
        - Refill information
        - Whether it's a controlled substance
        - Any other relevant prescription details
        
        Format the response as a JSON object following the PrescriptionData schema.
        """

    def extract_prescription_data(self, text: str) -> PrescriptionData:
        """Extract structured prescription data from text."""
        try:
            response = self.client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text},
                ],
                response_format=PrescriptionData,
            )

            # Get the JSON content from the response
            parsed_data = response.choices[0].message.parsed

            return parsed_data

        except Exception as e:
            raise Exception(f"Error extracting prescription data: {str(e)}")
