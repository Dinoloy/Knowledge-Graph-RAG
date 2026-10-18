
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = Chroma(
    collection_name="tn_government_schemes",
    persist_directory="chroma_db",
    embedding_function=embeddings,
)

query = "Which scheme provides training or financial assistance to farmers?"

results = vector_store.similarity_search_with_score(
    query,
    k=3,
)

print("\nUser question:")
print(query)

print("\nTop 3 relevant schemes:\n")

for rank, (document, score) in enumerate(results, start=1):
    print(f"--- Result {rank} ---")
    print(f"Scheme: {document.metadata.get('scheme_name', 'Unknown')}")
    print(f"Distance: {score:.4f}")
    print(f"Source: {document.metadata.get('source', '')}")
    print(f"Content:\n{document.page_content[:700]}")
    print()
