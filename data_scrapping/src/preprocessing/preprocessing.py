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
        output_csv = config["preprocessd_csv"]
        output_json = config["preprocessed_json"]
        output_json_dashboard = config["dashboard_preprocessed_json"]

        if not os.path.exists(input_csv):
            print(f"Input file not found: {input_csv}")
            return

        preprocessor = PreprocessingAgent(config=config)
        df = pd.read_csv(input_csv)

        cleaned_data = []
        df = df.sort_values(by=["company", "Year", "Quarter"], ascending=[True, False, True])

        df["Year"] = df["Year"].ffill().bfill()
        df["Quarter"] = df["Quarter"].ffill().bfill()

        for idx, row in df.iterrows():
            raw_data = row.to_dict()
            print(f"Cleaning data for file: {raw_data.get('file', 'Unknown')}")

            prompt = preprocessor.create_prompt(raw_data)
            response = preprocessor.query_openai(prompt)
            cleaned = preprocessor.parse_response(response)

            if "error" in cleaned:
                print(f"Preprocessing failed for: {raw_data.get('file', 'Unknown')}")
                continue

            cleaned["company"] = raw_data.get("company")

            cleaned["file"] = raw_data.get("file")
           

           

            cleaned_data.append(cleaned)

        # Save to CSV and JSON
        final_df = pd.DataFrame(cleaned_data)
        final_df = final_df.rename(columns={
                            "Year": "year",
                            "Quarter": "quarter",
                        })
    
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        final_df.to_csv(output_csv, index=False)
        final_df.to_json(output_json, orient="records")
        final_df.to_json(output_json_dashboard,orient="records")

        print(f"Preprocessing complete.")
        print(f"Cleaned CSV saved to: {output_csv}")
        print(f"Cleaned JSON saved to: {output_json}")
