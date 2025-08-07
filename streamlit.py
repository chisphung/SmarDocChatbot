import os
import streamlit as st
from src.rag.vectorstore import VectorDB
from src.base.llm_model import get_llm
from src.rag.main import build_rag_chain
from src.rag.file_loader import Loader
from src.rag.main import InputQA
import uuid
# --- Disable parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"
session_id = st.session_state.get("session_id", str(uuid.uuid4()))
st.session_state["session_id"] = session_id

# --- Config
st.set_page_config(page_title="SmartDocChatbot", page_icon="📚")
st.title("💬 SmartDoc Chatbot")
st.markdown("Chat with your uploaded documents using RAG and LLM 🔥")

# --- File uploader
uploaded_files = st.file_uploader(
    "📁 Upload documents (PDF, TXT, etc.)",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True
)

data_folder = "./data_source/generative_ai"
os.makedirs(data_folder, exist_ok=True)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")

    sources = []
    for file in uploaded_files:
        file_path = os.path.join(data_folder, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        sources.append(file_path)

    with st.spinner("🔍 Processing documents..."):
        loader = Loader(split_kwargs={"chunk_size": 300, "chunk_overlap": 0})
        docs = loader.load(sources, workers=7)

    st.success("📚 Documents processed and embedded!")

    # Build chain with retriever
    llm = get_llm("deepseek-chat", temperature=0.3)
    rag_chain = build_rag_chain(llm, data_dir=data_folder)

    # Chat interface
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Type your question about the docs...")

    if user_input:
        with st.spinner("💬 Generating answer..."):
            input_qa = InputQA(human_input=user_input)
            # response = rag_chain.invoke(input_qa)
                        
            response = rag_chain.invoke(
                {"human_input": input_qa.human_input},
                config={"configurable": {"session_id": session_id}}
            )

            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", response))

    for role, msg in st.session_state.chat_history:
        with st.chat_message("🧑‍💻" if role == "user" else "🤖"):
            st.markdown(msg)

else:
    st.info("📝 Upload some documents to start chatting.")
