import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pandas as pd
from src.utils.template_utils import load_prompt_template
from src.utils.config_utils import load_config
from src.agents.agents import FinancialExtractorAgent

class Extraction:
    def  __init__(self):
        pass
    def run_extraction(self):
        """
        Runs the financial data extraction process:
        - Loads configuration from conf.yaml
        - Iterates over company folders and PDFs inside the data/raw directory
        - Extracts text from each PDF
        - Creates a prompt and queries OpenAI for financial metrics
        - Parses and collects extracted data
        - Saves the results into outputs/financial_metrics.csv
        """
        config = load_config()
        extractor = FinancialExtractorAgent(config=config)
        pdf_folder = config["pdf_folder"]
        output_csv = config["output_csv"]
        results = []

        for company_folder in os.listdir(pdf_folder):
            company_path = os.path.join(pdf_folder, company_folder)
            if not os.path.isdir(company_path):
                continue

            for pdf_file in os.listdir(company_path):
                if not pdf_file.endswith(".pdf"):
                    continue

                pdf_path = os.path.join(company_path, pdf_file)
                print(f"Extracting from: {pdf_path}")

                text = extractor.extract_text_from_pdf(pdf_path)
                if not text.strip():
                    print(f"Skipped empty PDF: {pdf_file}")
                    continue

                prompt = extractor.create_prompt(text)
                response = extractor.query_openai(prompt)
                data = extractor.parse_response(response)                

                if "error" in data:
                    print(f"Extraction failed for: {pdf_file}")
                    continue

                data["company"] = company_folder
                data["file"] = pdf_file
                results.append(data)

        df = pd.DataFrame(results)
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        df.to_csv(output_csv, index=False)
        print(f"Extraction complete. Data saved to {output_csv}")
