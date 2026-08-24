from pathlib import Path
import pandas as pd

def load_data():
    file_path = Path(__file__).resolve().parents[1] / "data" / "application_train.csv"
    df = pd.read_csv(file_path)
    return df
