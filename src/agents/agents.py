import os
import pdfplumber
import json
from dotenv import load_dotenv
from openai import OpenAI
from src.utils.template_utils import load_prompt_template

class FinancialExtractorAgent:
    """
    An AI agent that extracts financial metrics from text extracted from a PDF report using OpenAI.
    """

    def __init__(self, config=None):
        """
        Initializes the FinancialExtractorAgent with API credentials and prompt template path.
        """
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL")
        self.endpoint = os.getenv("OPENAI_END_POINT")  
        self.client = OpenAI(api_key=self.api_key)  

        self.prompt_path = config.get("prompt_templates", {}).get("extractor") if config else "./prompts/extraction_prompt.jinja2"
        self.max_tokens = config.get("openai_params", {}).get("max_tokens", 500)
        self.temperature = config.get("openai_params", {}).get("temperature", 0.0)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extracts all text from a PDF file using pdfplumber.
        """
        extracted_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
        return extracted_text

    def create_prompt(self, extracted_text: str) -> str:
        """
        Generates a prompt using the extraction prompt template and extracted PDF text.
        """
        template = load_prompt_template(self.prompt_path)
        return template.render(text=extracted_text)

    def query_openai(self, prompt: str) -> dict:
        """
        Sends the generated prompt to OpenAI Chat API and returns the response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response
        except Exception as e:
            print(f"OpenAI API error (Extractor): {e}")
            return {}

    def parse_response(self, response: dict) -> dict:
        """
        Parses the JSON content from the OpenAI response.
        """
        if not response:
            return {"error": "Empty response"}
        try:
            content = response.choices[0].message.content  
            return json.loads(content)
        except Exception as e:
            print(f"Error parsing OpenAI response (Extractor): {e}")
            return {"error": "Failed to parse JSON"}


class PreprocessingAgent:
    """
    An AI agent that normalizes and cleans raw extracted financial data using OpenAI.
    """

    def __init__(self, config=None):
        """
        Initializes the PreprocessingAgent with API credentials and prompt template path.
        """
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL")
        self.endpoint = os.getenv("OPENAI_END_POINT")
        self.client = OpenAI(api_key=self.api_key)  

        self.prompt_path = config.get("prompt_templates", {}).get("preprocessor") if config else "./prompts/preprocessing_prompt.jinja2"
        self.max_tokens = config.get("openai_params", {}).get("max_tokens", 500)
        self.temperature = config.get("openai_params", {}).get("temperature", 0.0)

    def create_prompt(self, raw_data: dict) -> str:
        """
        Generates a prompt using the preprocessing prompt template and raw extracted data.
        """
        template = load_prompt_template(self.prompt_path)
        return template.render(raw_data=json.dumps(raw_data, indent=2))

    def query_openai(self, prompt: str) -> dict:
        """
        Sends the cleaning prompt to OpenAI Chat API and returns the response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial data normalizer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response
        except Exception as e:
            print(f"OpenAI API error (Preprocessor): {e}")
            return {}

    def parse_response(self, response: dict) -> dict:
        """
        Parses the JSON content from the OpenAI response.
        """
        if not response:
            return {"error": "Empty response"}
        try:
            content = response.choices[0].message.content 
            return json.loads(content)
        except Exception as e:
            print(f"Error parsing OpenAI response (Preprocessor): {e}")
            return {"error": "Failed to parse JSON", "raw": content}
