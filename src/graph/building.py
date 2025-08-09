#building.py

from config import *
from itertools import combinations
import re

#gnerate lemmas from SAMER dataset
def generate_lemmas_from_samer(samer_cleaned):
    for i in range(len(samer_cleaned)):
        lemma = samer_cleaned.iloc[i]["lemma"]
        pos = samer_cleaned.iloc[i]["pos"]
        avg_readability = samer_cleaned.iloc[i]["readability (rounded average)"]
        freq = samer_cleaned.iloc[i]["Occurrences"]

        lemma_query = """MERGE (l:Lemma {lemma: $lemma}) ON CREATE SET l.pos = $pos, l.avg_readability = $avg_readability, l.freq = $freq"""

        lemma_params = {"lemma": lemma, "pos": pos, "avg_readability": avg_readability, "freq": freq}

        execute_query(lemma_query, lemma_params)
    print("Finished generating lemmas from SAMER")


# Generating Sentences from the dataset
def generate_sentence_from_data_set(data_set_cleaned, samer_cleaned):
    lemma_set = set(samer_cleaned[ 'lemma'].astype(str))
    pairs_list = []

    for i in range(len(data_set_cleaned)):
        sentence = data_set_cleaned.iloc[i]["Sentence"]
        domain_type = data_set_cleaned.iloc[i]["Domain"]
        class_type = data_set_cleaned.iloc[i]["Text_Class"]

        words = re.findall(r'\b[\w]+\b', sentence)
        sentence_to_lemma = []
        for word in words:
            if word in lemma_set:
                sentence_to_lemma.append(word)

        pairs = [list(pair) for pair in combinations(set(sentence_to_lemma), 2)]
        pairs_list.extend(pairs)

        sentence_query = """
    		MERGE (S:Sentence {id: $id})
    		ON CREATE SET S.text = $text

    		WITH S
    		MERGE (D:Domain {type: $domainType})
    		MERGE (C:Class {type: $classType})
    		MERGE (S)-[:IN_DOMAIN]->(D)
    		MERGE (S)-[:IN_CLASS]->(C)

    		WITH S
    		UNWIND $lemmas AS lemma
    		MATCH (L:Lemma {lemma: lemma})
    		MERGE (S)-[r:HAS_LEMMA]->(L)
    		ON CREATE SET r.count = 1
    		ON MATCH SET r.count = r.count + 1
    	"""

        sentence_params = {"id": i + 1, "text": sentence, "domainType": domain_type, "classType": class_type, "lemmas": sentence_to_lemma}

        execute_query(sentence_query, sentence_params)

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

    print("Finished generating sentences from dataset")