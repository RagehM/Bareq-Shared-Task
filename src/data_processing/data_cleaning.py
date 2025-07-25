#data_cleaning.py

from src.utils.arabic import remove_diacritics

def clean_data_set(data_set):
    # Remove Unwanted Columns
    data_set_cleaned = data_set.drop(columns=["Word_Count", "Readability_Level_19", "Readability_Level_7", "Readability_Level_5", "Readability_Level_3", "Annotator", "Document", "Source", "Book", "Author"])

    # Remove Dublicate Rows
    data_set_cleaned = data_set_cleaned.drop_duplicates(subset='Sentence', keep='first')

    # Save the cleaned dataset to a CSV file
    data_set_cleaned.to_csv("../data/cleaned/cleaned_data_set.csv", index=False)

    print("Data set cleaned and saved successfully.")

    return data_set_cleaned

def clean_samer(SAMER_df):
    # Remove unwanted columns
    samer_cleaned = SAMER_df.drop(columns=['Hindawi (5594310)', 'Giga (5594256)', 'Answer1 - Egyptian', 'Answer2 - Syrian', 'Answer3 - Saudi Arabian'])

    # Split 'lemma#pos' into separate columns
    samer_cleaned[['lemma', 'pos']] = samer_cleaned['lemma#pos'].str.split('#', expand=True)

    # Remove the original 'lemma#pos' column
    samer_cleaned = samer_cleaned.drop(columns=['lemma#pos'])

    # Remove diacritics from the 'lemma' column
    samer_cleaned['lemma'] = samer_cleaned['lemma'].apply(remove_diacritics)

    # Remove duplicates based on the 'lemma' column
    samer_cleaned = samer_cleaned.drop_duplicates(subset='lemma', keep='first')

    # Save the cleaned DataFrame to a CSV file
    samer_cleaned.to_csv("../data/cleaned/cleaned_SAMER_df.csv", index=False)

    print("SAMER dataset cleaned and saved successfully.")

    return samer_cleaned



