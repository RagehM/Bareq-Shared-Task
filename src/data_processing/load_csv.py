#load_csv.py

import pandas as pd

def load_csv():
    try:
        SAMER_df = pd.read_csv('../data/raw/SAMER-Readability-Lexicon-v1.tsv', sep='\t')

        df_dev = pd.read_csv("../data/raw/dev.csv")

        data_set = pd.read_csv("hf://datasets/CAMeL-Lab/BAREC-Shared-Task-2025-sent/" + "train.csv")

        test_sent = pd.read_csv("../data/raw/test_sent.csv")

        test_doc = pd.read_csv("../data/raw/test_doc.csv")

        print("CSV files loaded successfully.")

        return SAMER_df, df_dev, data_set, test_sent, test_doc
    except Exception as e:
        print(f"Error loading CSV files: {e}")
        return None, None, None, None, None
