#main.py

from src.data_processing.data_cleaning import clean_data_set
from src.data_processing.data_cleaning import clean_samer
import pandas as pd

def main():
    SAMER_df = pd.read_csv('../data/raw/SAMER-Readability-Lexicon-v1.tsv', sep='\t')

    df_dev = pd.read_csv('../data/raw/dev.csv')

    data_set = pd.read_csv("hf://datasets/CAMeL-Lab/BAREC-Shared-Task-2025-sent/" + "train.csv")
    data_set = pd.DataFrame(data_set)

    test_sent = pd.read_csv("../data/raw/test_sent.csv")

    test_doc = pd.read_csv("../data/raw/test_doc.csv")

    samer_cleaned = clean_samer(SAMER_df)

    data_set_cleaned = clean_data_set(data_set)



main()