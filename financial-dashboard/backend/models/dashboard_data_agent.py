import os
import pandas as pd
import numpy as np

class DashboardDataAgent:
    def __init__(self, dataset_path=None):
        default_path = os.path.join(os.path.dirname(__file__), '../data/processed_dataset.json')
        self.dataset_path = dataset_path or default_path
        self.df = self._load_dataset()

    def _load_dataset(self):
        try:
            df = pd.read_json(self.dataset_path)
            df = df.replace([np.inf, -np.inf], np.nan).fillna(0)  
            print("Dashboard dataset loaded.")
            return df
        except Exception as e:
            print("Failed to load dataset:", e)
            return pd.DataFrame()

    def get_full_data(self):
        return self.df.to_dict(orient="records")

    def get_raw_df(self):
        return self.df
