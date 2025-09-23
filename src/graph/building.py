#building.py

from src.config import *
from itertools import combinations
import re

#gnerate lemmas from SAMER dataset
def generate_lemmas_from_samer(samer_cleaned, batch_size=1000):
    for i in range(0, len(samer_cleaned), batch_size):
        batch_end = min(i + batch_size, len(samer_cleaned))
        lemma_data = []

        for j in range(i, batch_end):
            lemma_data.append({
                "lemma": samer_cleaned.iloc[j]["lemma"],
                "pos": samer_cleaned.iloc[j]["pos"],
                "avg_readability": samer_cleaned.iloc[j]["readability (rounded average)"],
                "freq": samer_cleaned.iloc[j]["Occurrences"]
            })

        lemma_query = """
        UNWIND $lemmas AS lemma_data
        MERGE (l:Lemma {lemma: lemma_data.lemma}) 
        ON CREATE SET 
            l.pos = lemma_data.pos, 
            l.avg_readability = lemma_data.avg_readability, 
            l.freq = lemma_data.freq
        """
        execute_query(lemma_query, {"lemmas": lemma_data})
    logging.info("Finished generating lemmas from SAMER")


# Generating Sentences from the dataset
def generate_sentence_from_data_set(data_set_cleaned, samer_cleaned, batch_size=500):
    lemma_set = set(samer_cleaned['lemma'].astype(str))
    pairs_list = []

    for i in range(0, len(data_set_cleaned), batch_size):
        batch_end = min(i + batch_size, len(data_set_cleaned))
        sentence_data = []

        for j in range(i, batch_end):
            sentence = data_set_cleaned.iloc[j]["Sentence"]
            domain_type = data_set_cleaned.iloc[j]["Domain"]
            class_type = data_set_cleaned.iloc[j]["Text_Class"]

            words = re.findall(r'\b[\w]+\b', sentence)
            sentence_to_lemma = []
            for word in words:
                if word in lemma_set:
                    sentence_to_lemma.append(word)

            pairs = [list(pair) for pair in combinations(set(sentence_to_lemma), 2)]
            pairs_list.extend(pairs)

            sentence_data.append({
                "id": j + 1,
                "text": sentence,
                "domainType": domain_type,
                "classType": class_type,
                "lemmas": sentence_to_lemma
            })

        sentence_query = """
        UNWIND $sentences AS sentence_data

        MERGE (S:Sentence {id: sentence_data.id})
        ON CREATE SET S.text = sentence_data.text

        MERGE (D:Domain {type: sentence_data.domainType})
        MERGE (C:Class {type: sentence_data.classType})

        MERGE (S)-[:IN_DOMAIN]->(D)
        MERGE (S)-[:IN_CLASS]->(C)

        WITH S, sentence_data
        UNWIND sentence_data.lemmas AS lemma
        MATCH (L:Lemma {lemma: lemma})
        MERGE (S)-[r:HAS_LEMMA]->(L)
        ON CREATE SET r.count = 1
        ON MATCH SET r.count = r.count + 1
        """

        execute_query(sentence_query, {"sentences": sentence_data})

    lemmas_pairs_query = """
                UNWIND $pairs AS pair
                MATCH (l1:Lemma {lemma: pair[0]})
                MATCH (l2:Lemma {lemma: pair[1]})

                MERGE (l1)-[r1:OCCUR_WITH]->(l2)
                ON CREATE SET r1.count = 1
                ON MATCH SET r1.count = r1.count + 1

                MERGE (l2)-[r2:OCCUR_WITH]->(l1)
                ON CREATE SET r2.count = 1
                ON MATCH SET r2.count = r2.count + 1"""

    lemmas_pairs_params = {"pairs": pairs_list}

    execute_query(lemmas_pairs_query, lemmas_pairs_params)

    logging.info("Finished generating sentences from dataset")