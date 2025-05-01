print("MAIN.PY STARTED") 
from src.utils.config_utils import load_config
from src.extraction.extraction import Extraction
from src.preprocessing.preprocessing import Preprocessing
import subprocess
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
os.chdir(PROJECT_ROOT)

def run_extraction():
    print("Starting Extraction Step")
    try:
        result = Extraction().run_extraction()
    except:
        print("extraction failed")

  

def run_preprocessing():
    print("Starting Preprocessing Step")
    try:
        result= Preprocessing().run_preprocessing()
    except:
        print("preprocessing failed")
    

def main():
    print("Main function started")
    run_extraction() 
    run_preprocessing()
    print("Pipeline Completed Successfully.")

if __name__ == "__main__":
    print("__main__ condition triggered")
    main()
