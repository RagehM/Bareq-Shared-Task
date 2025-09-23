# load_csv.py

import pandas as pd
import logging
from pathlib import Path


def load_csv():
    try:
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent

        raw_data = project_root / "data" / "raw"

        SAMER_df = pd.read_csv(raw_data / "SAMER-Readability-Lexicon-v1.tsv", sep="\t")
        df_dev = pd.read_csv(raw_data / "dev.csv")
        test_sent = pd.read_csv(raw_data / "test_sent.csv")
        test_doc = pd.read_csv(raw_data / "test_doc.csv")

        # Hugging Face dataset (not local, so keep as string path)
        data_set = pd.read_csv("hf://datasets/CAMeL-Lab/BAREC-Shared-Task-2025-sent/train.csv")

        logging.info("CSV files loaded successfully.")

        return SAMER_df, df_dev, data_set, test_sent, test_doc

    except Exception as e:
        logging.error(f"Error loading CSV files: {e}")
        return None, None, None, None, None
