#main.py

from data_processing.load_csv import load_csv
from data_processing.data_cleaning import clean_data_set
from data_processing.data_cleaning import clean_samer
from graph.building import *
from config import *
from graph.retrieving import *
import pandas as pd

def main():
    SAMER_df, df_dev, data_set, test_sent, test_doc = load_csv()

    samer_cleaned = clean_samer(SAMER_df)

    data_set_cleaned = clean_data_set(data_set)

    generate_lemmas_from_samer(samer_cleaned)

    generate_sentence_from_data_set(data_set_cleaned, samer_cleaned)

    retrieve_sentences()

    retrieve_lemmas()

    retrieve_sentence_lemma()

    retrieve_lemma_lemma()

    retrieve_sentence_domain()

    retrieve_sentence_class()

if __name__ == "__main__":
    main()
    logging.info("Processing completed successfully.")