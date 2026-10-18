
import networkx as nx
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

GRAPH_FILE = "schemes_knowledge_graph.graphml"
VECTOR_STORE_DIR = "chroma_db"

# Load embeddings and ChromaDB
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    collection_name="tn_government_schemes",
    persist_directory=VECTOR_STORE_DIR,
    embedding_function=embeddings,
)

# Load the knowledge graph
graph = nx.read_graphml(GRAPH_FILE)

# Load the chat model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def find_graph_context(question):
    """Find graph relationships relevant to the question."""
    question_lower = question.lower()
    matches = []

    # Search scheme nodes by name
    for node_id, data in graph.nodes(data=True):
        if data.get("type") != "Scheme":
            continue

        scheme_name = data.get("name", "")

        if (
            scheme_name
            and any(
                word in scheme_name.lower()
                for word in question_lower.split()
                if len(word) > 3
            )
        ):
            details = [f"Scheme: {scheme_name}"]

            for _, target, edge_data in graph.out_edges(
                node_id, data=True
            ):
                relation = edge_data.get("relation", "related_to")
                target_data = graph.nodes[target]
                target_name = target_data.get("name", target)

                details.append(f"{relation}: {target_name}")

            matches.append("\n".join(details))

    return "\n\n".join(matches[:5])


def answer_question(question):
    # Step 1: Semantic retrieval
    documents = vector_store.similarity_search(question, k=4)

    retrieved_context = "\n\n".join(
        f"Scheme: {doc.metadata.get('scheme_name', 'Unknown')}\n"
        f"{doc.page_content}\n"
        f"Source: {doc.metadata.get('source', '')}"
        for doc in documents
    )

    # Step 2: Knowledge graph lookup
    graph_context = find_graph_context(question)

    # Step 3: Combine evidence and generate an answer
    prompt = f"""
You are an assistant for Tamil Nadu government schemes.

Answer using the retrieved scheme documents and graph relationships.
Treat scheme documents as the primary evidence for amounts, eligibility,
descriptions and application instructions. Use graph relationships to
clarify departments, beneficiaries and benefit types.

Rules:
- Do not invent missing details.
- If sources are incomplete, state what is missing.
- Do not treat a related scheme as an exact match without explaining why.
- Include source URLs from the retrieved documents.
- If the graph does not contain a relevant relationship, do not invent one.

Retrieved scheme documents:
{retrieved_context}

Knowledge graph relationships:
{graph_context if graph_context else "No matching graph relationships found."}

User question:
{question}
"""

    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    print("Tamil Nadu Government Knowledge Graph RAG Chatbot")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Chatbot stopped.")
            break

        if not question:
            continue

        try:
            print("\nAssistant:\n")
            print(answer_question(question))
            print()
        except Exception as error:
            print(f"Error: {error}")
