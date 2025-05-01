import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
from src.utils.config_utils import load_config
from src.agents.agents import PreprocessingAgent

class Preprocessing:

    def __init__(self):
        pass

    def run_preprocessing(self):
        """
        Runs the preprocessing and normalization of extracted financial data:
        - Loads raw extracted data from outputs/financial_metrics.csv
        - Cleans and normalizes each row using OpenAI and the PreprocessingAgent
        - Extracts year and quarter from the 'file' column
        - Saves the cleaned data to outputs/processed_dataset.csv and processed_dataset.json
        """
        config = load_config()

        input_csv = config["output_csv"]
        output_csv = "./outputs/processed_dataset.csv"
        output_json = "./outputs/processed_dataset.json"
        output_json_dashboard = r"C:\Users\ASUS\Desktop\project_quater_analysis\financial-dashboard\src\data\processed_dataset.json"



        if not os.path.exists(input_csv):
            print(f"Input file not found: {input_csv}")
            return

        preprocessor = PreprocessingAgent(config=config)
        df = pd.read_csv(input_csv)

        # Extract year and quarter from 'file' column
        def extract_year_quarter(filename):
            try:
                date_part = filename.split("_")[1].replace(".pdf", "")
                year, month, _ = date_part.split("-")
                month = int(month)
                if 1 <= month <= 3:
                    quarter = "Q1"
                elif 4 <= month <= 6:
                    quarter = "Q2"
                elif 7 <= month <= 9:
                    quarter = "Q3"
                else:
                    quarter = "Q4"
                return int(year), quarter
            except Exception:
                return None, None

        df["year"], df["quarter"] = zip(*df["file"].map(extract_year_quarter))

        cleaned_data = []

        for idx, row in df.iterrows():
            raw_data = row.to_dict()
            print(f"Cleaning data for file: {raw_data.get('file', 'Unknown')}")

            prompt = preprocessor.create_prompt(raw_data)
            response = preprocessor.query_openai(prompt)
            cleaned = preprocessor.parse_response(response)

            if "error" in cleaned:
                print(f"Preprocessing failed for: {raw_data.get('file', 'Unknown')}")
                continue

            # Retain metadata fields
            cleaned["company"] = raw_data.get("company")
            cleaned["file"] = raw_data.get("file")
            cleaned["year"] = raw_data.get("year")
            cleaned["quarter"] = raw_data.get("quarter")
            cleaned_data.append(cleaned)

        # Save to CSV and JSON
        final_df = pd.DataFrame(cleaned_data)
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        final_df.to_csv(output_csv, index=False)
        final_df.to_json(output_json, orient="records")
        final_df.to_json(output_json_dashboard,orient="records")

        print(f"Preprocessing complete.")
        print(f"Cleaned CSV saved to: {output_csv}")
        print(f"Cleaned JSON saved to: {output_json}")
