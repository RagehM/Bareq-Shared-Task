#retrieving.py

from config import execute_query
from config import logging
import json

# Retrieving sentences from the database and saving them to a JSON file
def retrieve_sentences():
    sentence_query = """MATCH (s:Sentence) RETURN s AS Sentence"""
    sentence_records = execute_query(sentence_query)

    sentence_nodes = []
    for record in sentence_records:
        lemma_node = record['Sentence']
        sentence = {
            "sentence_text": record['Sentence']["text"],
        }
        sentence_nodes.append(sentence)

    with open("data/json/sentences.json", "w", encoding="utf-8") as f:
        json.dump(sentence_nodes, f, ensure_ascii=False, indent=2)

    logging.info("Sentences retrieved and saved to data/json/sentences.json")


# Retrieving lemmas from the database and saving them to a JSON file
def retrieve_lemmas():
    lemmas_query = """MATCH (l:Lemma) RETURN l AS Lemma"""
    lemma_records = execute_query(lemmas_query)

    lemma_nodes = []
    for record in lemma_records:
        lemma_node = record['Lemma']
        lemma = {
            "lemma": lemma_node["lemma"],
            "pos": lemma_node["pos"],
            "avg_readability": lemma_node["avg_readability"],
            "freq": lemma_node["freq"]
        }
        lemma_nodes.append(lemma)

    with open("data/json/lemmas.json", "w", encoding="utf-8") as f:
        json.dump(lemma_nodes, f, ensure_ascii=False, indent=2)

    logging.info("Lemmas retrieved and saved to data/json/lemmas.json")


def retrieve_sentence_lemma():
    sentence_lemma_query = """MATCH (s:Sentence)-[r:HAS_LEMMA]->(l:Lemma) RETURN s AS sentence, r AS relation, l AS lemma"""
    sentence_lemma_records = execute_query(sentence_lemma_query)

    sentence_lemma_nodes = []
    for record in sentence_lemma_records:
        sentence_part = record["sentence"]
        relation_part = record["relation"]
        lemma_part = record["lemma"]
        sentence_lemma = {
            "sentence_text": sentence_part["text"],
            "relation": relation_part.type,
            "lemma": lemma_part["lemma"]
        }
        sentence_lemma_nodes.append(sentence_lemma)

    with open("data/json/sentence_lemma.json", "w", encoding="utf-8") as f:
        json.dump(sentence_lemma_nodes, f, ensure_ascii=False, indent=2)

    logging.info("Sentence-Lemma relationships retrieved and saved to data/json/sentence_lemma.json")


def retrieve_lemma_lemma():
    lemma_lemma_query = """MATCH (l1:Lemma)-[r:OCCUR_WITH]->(l2:Lemma)
    WHERE l1.lemma < l2.lemma 
    RETURN l1 AS lemma1, r AS relation, l2 AS lemma2"""
    lemma_lemma_records = execute_query(lemma_lemma_query)

    lemma_lemma_nodes = []
    for record in lemma_lemma_records:
        lemma1_part = record["lemma1"]
        relation_part = record["relation"]
        lemma2_part = record["lemma2"]
        lemma_lemma = {
            "lemma1": lemma1_part["lemma"],
            "relation": relation_part.type,
            "count": relation_part["count"],
            "lemma2": lemma2_part["lemma"]
        }
        lemma_lemma_nodes.append(lemma_lemma)

    with open("data/json/lemma_lemma.json", "w", encoding="utf-8") as f:
        json.dump(lemma_lemma_nodes, f, ensure_ascii=False, indent=2)

    logging.info("Lemma-Lemma relationships retrieved and saved to data/json/lemma_lemma.json")

def retrieve_sentence_class():
    sentence_class_query = """MATCH (s:Sentence)-[r:IN_CLASS]->(c:Class) RETURN s AS sentence, r AS relation, c AS class"""
    sentence_class_records = execute_query(sentence_class_query)

    sentence_class_nodes = []
    for record in sentence_class_records:
        sentence_part = record["sentence"]
        relation_part = record["relation"]
        class_part = record["class"]
        sentence_class = {
            "sentence_text": sentence_part["text"],
            "relation": relation_part.type,
            "class_type": class_part["type"]
        }
        sentence_class_nodes.append(sentence_class)

    with open("sentence_class.json", "w", encoding="utf-8") as f:
        json.dump(sentence_class_nodes, f, ensure_ascii=False, indent=2)

    logging.info("Sentence-Class relationships retrieved and saved to data/json/sentence_class.json")


def retrieve_sentence_domain():
    sentence_domain_query = """MATCH (s:Sentence)-[r:IN_DOMAIN]->(d:Domain) RETURN s AS sentence, r AS relation, d AS domain"""
    sentence_domain_records = execute_query(sentence_domain_query)

    sentence_domain_nodes = []
    for record in sentence_domain_records:
        sentence_part = record["sentence"]
        relation_part = record["relation"]
        domain_part = record["domain"]
        sentence_domain = {
            "sentence_text": sentence_part["text"],
            "relation": relation_part.type,
            "domain_type": domain_part["type"]
        }
        sentence_domain_nodes.append(sentence_domain)

    with open("sentence_domain.json", "w", encoding="utf-8") as f:
        json.dump(sentence_domain_nodes, f, ensure_ascii=False, indent=2)

    logging.info("Sentence-Domain relationships retrieved and saved to data/json/sentence_domain.json")

