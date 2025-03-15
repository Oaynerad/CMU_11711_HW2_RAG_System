# 11711 NLP HW2 RAG System

Daren Yao, Jinsong Yuan, Ruike Chen

# RAG Project

This GitHub repository contains our Retrieval-Augmented Generation (RAG) project designed to perform Question and Answering tasks. Below is a detailed explanation of the repository structure and usage instructions.

## Usage

To execute the main RAG program, run the following command in your terminal:

```bash
python main.py
```

## Explanation of Contents

### QA Directory

This directory stores our annotated question-and-answer data categorized into multiple JSON files according to their types:

- **`definition_QA.json`**: Definition-type questions
- **`how_QA.json`**: Questions about "how" scenarios
- **`location_QA.json`**: Location-based questions
- **`other_QA.json`**: Miscellaneous category
- **`person_QA.json`**: Questions specifically related to people
- **`quantity_QA.json`**: Numeric and quantity-related questions
- **`time_QA.json`**: Time-related questions

Additionally, specialized files such as **`QA_info_history_events.json`** and **`QA_music_culture_food_sports.json`** contain thematic QA pairs for more targeted querying.

### Data Directory

The `data/` directory contains raw data collected through scraping, utilized as input sources for our RAG model.

### Scrapers

- **`scrape_daren/`**: Data scraping scripts implemented by Daren.
- **`scrape_ruike/`**: Data scraping scripts implemented by Ruike.

Each team member developed dedicated scraping modules responsible for collecting diverse datasets needed for our QA tasks.

### Main RAG File (`main.py`)

This file integrates retrieval and generation techniques. It leverages the QA datasets and scraped data to generate answers dynamically to input questions using our RAG methodology.

### Contributions (`contributions.md`)

Records detailing individual contributions made by each team member throughout the project development.

## Team Contributions

Please refer to the `contributions.md` document for detailed insights into each team member's roles and tasks completed during the project lifecycle.
