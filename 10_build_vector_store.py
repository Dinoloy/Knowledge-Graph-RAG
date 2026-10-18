
import json
import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

load_dotenv()

INPUT_FILE = "rag_documents.json"
VECTOR_STORE_DIR = "chroma_db"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    records = json.load(file)

documents = []

for record in records:
    documents.append(
        Document(
            page_content=record["content"],
            metadata={
                "scheme_name": record["scheme_name"],
                "source": record["source"],
                "id": record["id"],
            },
        )
    )

print(f"Loaded {len(documents)} scheme documents.")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory=VECTOR_STORE_DIR,
    collection_name="tn_government_schemes",
)

print("Vector store created successfully!")
print(f"Stored documents: {len(documents)}")
print(f"Vector store directory: {VECTOR_STORE_DIR}")
