# config.py

from dotenv import load_dotenv
from neo4j import GraphDatabase
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
import os
import logging

load_dotenv()

#loggin configuration
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='app.log'
)

# Database configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def execute_query(query, parameters=None):
    with neo4j_driver.session() as session:
        result = session.run(query, parameters or {})
        return [record for record in result]

# Test connection to Neo4j
try:
    test_query = "CALL db.info()"
    execute_query(test_query)
    print("Connected to Neo4j successfully.")
except Exception as e:
    print(f"Error connecting to Neo4j: {e}")

# Morphology Analyzer configuration
db = MorphologyDB.builtin_db()
analyzer = Analyzer(db)

