# Bareq Shared Task

A project for processing Arabic text data using Neo4j graph database and natural language processing techniques.

## Project Structure
```
├── data/
│   ├── cleaned/         # Cleaned datasets
│   ├── json/           # Generated JSON files
│   └── raw/            # Raw input data
├── src/
│   ├── config.py       # Configuration settings
│   ├── main.py         # Main entry point
│   ├── data_processing/
│   │   └── data_cleaning.py
│   ├── graph/
│   │   ├── building.py
│   │   └── retrieving.py
│   └── utils/
├── environment.yml      # Conda environment file
├── .env                # Environment variables
└── Bareq_Shared_Task.ipynb  # Jupyter notebook with development code
```

## Requirements

- Python 3.9+
- Neo4j Database
- Required Python packages:
  - neo4j
  - pandas
  - datasets
  - python-dotenv
  - camel-tools

## Setup

1. Clone the repository
2. Create conda environment from environment.yml:
```bash
conda env create -f environment.yml
```

3. Create a `.env` file with Neo4j credentials:
```
NEO4J_URI=bolt://localhost:7687
USERNAME=neo4j
PASSWORD=your_password
```

## Usage

Run the main script:
```bash
python src/main.py
```

This will:
1. Load and clean the datasets
2. Generate graph nodes and relationships
3. Retrieve and save graph data as JSON files

## Data Processing Pipeline

1. Data Cleaning
   - Removes unwanted columns
   - Removes duplicate rows
   - Cleans Arabic text by removing diacritics

2. Graph Building
   - Creates Lemma nodes with properties (POS, readability, frequency)
   - Creates Sentence nodes with text content
   - Creates relationships between nodes:
     - Sentence-Lemma (HAS_LEMMA)
     - Sentence-Domain (IN_DOMAIN)
     - Sentence-Class (IN_CLASS)
     - Lemma-Lemma (OCCUR_WITH)

3. Data Retrieval
   - Retrieves graph data and saves as JSON files
   - Generated files:
     - lemmas.json
     - sentences.json
     - sentence_lemma.json
     - lemma_lemma.json
     - sentence_domain.json
     - sentence_class.json
