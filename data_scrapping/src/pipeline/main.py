print("MAIN.PY STARTED") 
from src.utils.config_utils import load_config
from src.extraction.extraction import Extraction
from src.preprocessing.preprocessing import Preprocessing
from src.scrapper.download_pdfs import SeleniumScraper
import subprocess
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
os.chdir(PROJECT_ROOT)

# scraper = SeleniumScraper(headless=True)
# for symbol in ["DIPD", "REXP"]:
#     print(f"\nFetching reports for {symbol}")
#     scraper.fetch_quarterly_pdfs(symbol)
# scraper.close()

def run_extraction():
    print("Starting Extraction Step")
    try:
        result = Extraction().run_extraction()
    except Exception as e:
        print("extraction failed")
        raise e

  

def run_preprocessing():
    print("Starting Preprocessing Step")
    try:
        result= Preprocessing().run_preprocessing()
    except Exception as e:
        print("preprocessing failed")
        raise e
    

def main():
    print("Main function started")
    # run_extraction() 
    run_preprocessing()
    print("Pipeline Completed Successfully.")

if __name__ == "__main__":
    print("__main__ condition triggered")
    main()
