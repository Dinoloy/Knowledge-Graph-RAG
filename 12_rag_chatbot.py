
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# Load the embedding model and existing vector store
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = Chroma(
    collection_name="tn_government_schemes",
    persist_directory="chroma_db",
    embedding_function=embeddings,
)

# Configure the language model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

def answer_question(question):
    results = vector_store.similarity_search(
        question,
        k=4,
    )

    if not results:
        return "I could not find a relevant scheme in the available data."

    context_parts = []

    for doc in results:
        context_parts.append(
            f"Scheme: {doc.metadata.get('scheme_name', 'Unknown')}\n"
            f"Source: {doc.metadata.get('source', '')}\n"
            f"Details:\n{doc.page_content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are a helpful assistant for Tamil Nadu government schemes.

Answer the user's question using only the scheme information in the
provided context.

Rules:
1. Do not invent eligibility rules, benefits, amounts, or application steps.
2. If the context does not contain enough information, say so clearly.
3. Distinguish between different schemes with similar names.
4. Include the source URL for each scheme discussed.
5. Use simple, clear language.

Retrieved scheme information:
{context}

User question:
{question}
"""

    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    print("Tamil Nadu Government Schemes RAG Chatbot")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Chatbot stopped.")
            break

        if not question:
            continue

        try:
            answer = answer_question(question)
            print(f"\nAssistant:\n{answer}\n")
        except Exception as error:
            print(f"\nError: {error}\n")
