
import streamlit as st
from graph_rag_chatbot import answer_question

st.set_page_config(
    page_title="Tamil Nadu Schemes AI",
    page_icon="🏛️",
    layout="centered",
)

st.title("🏛️ Tamil Nadu Schemes AI")
st.caption("Your assistant for exploring Tamil Nadu government schemes")

with st.sidebar:
    st.header("About")
    st.write(
        "Ask questions about Tamil Nadu government schemes, "
        "benefits, eligibility, and application procedures."
    )
    st.caption("Powered by Knowledge Graph RAG, ChromaDB and OpenAI.")

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("pending_question", None)
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

suggestions = [
    "Which schemes provide training to farmers?",
    "What benefits are available under Training to Farmers?",
    "What are the eligibility criteria for Training to Farmers?",
]

st.subheader("Suggested questions")

cols = st.columns(1)

for question in suggestions:
    if st.button(question, use_container_width=True):
        st.session_state.pending_question = question

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask about a government scheme...")

if question:
    st.session_state.pending_question = question

if st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching schemes and generating an answer..."):
            try:
                answer = answer_question(question)
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as error:
                st.error(f"Unable to generate an answer: {error}")
