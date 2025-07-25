#load_csv.py

import pandas as pd

def load_csv():
    try:
        SAMER_df = pd.read_csv('../../data/raw/SAMER-Readability-Lexicon-v1.tsv', sep='\t')

        df_dev = pd.read_csv('../../data/raw/dev.csv')

        data_set = pd.read_csv("hf://datasets/CAMeL-Lab/BAREC-Shared-Task-2025-sent/" + "train.csv")
        data_set = pd.DataFrame(data_set)

        test_sent = pd.read_csv("../../data/raw/test_sent.csv")

        test_doc = pd.read_csv("../../data/test_doc.csv")
    except Exception as e:
        print(f"Error loading CSV files: {e}")
