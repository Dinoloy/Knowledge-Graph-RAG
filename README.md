

\# Tamil Nadu Government Schemes — Knowledge Graph RAG Chatbot



\## Overview

A Python-based chatbot that answers questions about Tamil Nadu Government schemes using Retrieval-Augmented Generation (RAG), a NetworkX knowledge graph, ChromaDB vector search, LangChain, OpenAI, and Streamlit.



\## Features

\- Extracts scheme information from the Tamil Nadu Government website.

\- Builds a knowledge graph using NetworkX.

\- Stores scheme documents in ChromaDB for semantic retrieval.

\- Generates answers using OpenAI.

\- Provides a Streamlit chat interface.

\- Includes source URLs in answers where available.



\## Technology Stack

\- Python

\- LangChain

\- OpenAI

\- NetworkX

\- ChromaDB

\- Streamlit

\- BeautifulSoup

\- Requests



\## Setup



1\. Clone this repository.

2\. Create and activate a Python virtual environment.

3\. Install the dependencies:



&#x20;  ```bash

&#x20;  pip install -r requirements.txt

&#x20;  ```



4\. Create a `.env` file and configure your OpenAI API key:



&#x20;  ```text

&#x20;  OPENAI\_API\_KEY=your\_openai\_api\_key

&#x20;  ```



5\. Run the chatbot UI:



&#x20;  ```bash

&#x20;  python -m streamlit run 20\_chatbot\_ui.py

&#x20;  ```



\## Data and Artifacts

The repository includes extracted scheme data, RAG documents, and the knowledge graph. The local ChromaDB vector store is not included; it may need to be built using the provided scripts.



\## Disclaimer

This is an educational assignment. Verify scheme eligibility, benefits, and application procedures with official government sources.



\## Source

\[Tamil Nadu Government Schemes](https://www.tn.gov.in/scheme\_list.php?dep\_id=Mg==)



