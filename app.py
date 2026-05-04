import streamlit as st
from parser.document_parser import extract_text
from utils.text_cleaner import clean_text, split_text
from utils.history_manager import save_chat, load_chat
from vectorstore.faiss_store import create_vector_store, search_vector_store
from rag.rag_pipeline import generate_answer

st.set_page_config(page_title="DocuMind AI", layout="wide")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.chat-box {padding:10px;border-radius:10px;margin-bottom:10px;}
.user {background-color:#DCF8C6;}
.bot {background-color:#F1F0F0;}
</style>
""", unsafe_allow_html=True)

st.title("📄 DocuMind AI")

# ---------------- SESSION ----------------
if "documents" not in st.session_state:
    st.session_state.documents = {}

# ---------------- SIDEBAR ----------------
st.sidebar.title("📂 Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload documents",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

# ---------------- PROCESS FILES ----------------
if uploaded_files:
    for file in uploaded_files:

        if file.name not in st.session_state.documents:

            raw_text = extract_text(file)
            clean = clean_text(raw_text)

            chunks = split_text(clean)
            chunks = [c for c in chunks if len(c.split()) > 10]

            index, stored_chunks = create_vector_store(chunks)

            st.session_state.documents[file.name] = {
                "index": index,
                "chunks": stored_chunks,
                "chat": load_chat(file.name)
            }

# ---------------- SELECT DOCUMENT ----------------
if st.session_state.documents:

    selected_doc = st.sidebar.selectbox(
        "Select document",
        list(st.session_state.documents.keys())
    )

    doc_data = st.session_state.documents[selected_doc]

    st.subheader(f"📄 {selected_doc}")

    # ---------------- QUERY ----------------
    query = st.text_input("💬 Ask something")

    if query:
        results = search_vector_store(
            query,
            doc_data["index"],
            doc_data["chunks"]
        )

        with st.spinner("Thinking..."):
            answer = generate_answer(query, results)

        doc_data["chat"].append({
            "question": query,
            "answer": answer
        })

        save_chat(selected_doc, doc_data["chat"])

    # ---------------- CHAT ----------------
    st.subheader("💬 Conversation")

    for chat in reversed(doc_data["chat"]):

        st.markdown(
            f"<div class='chat-box user'><b>You:</b> {chat['question']}</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div class='chat-box bot'><b>DocuMind:</b> {chat['answer']}</div>",
            unsafe_allow_html=True
        )

    # ---------------- CLEAR ----------------
    if st.button("🧹 Clear Chat"):
        doc_data["chat"] = []
        save_chat(selected_doc, [])

else:
    st.info("Upload documents to begin.")