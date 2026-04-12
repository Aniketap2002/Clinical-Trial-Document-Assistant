import streamlit as st
from rag import create_rag_chain
import tempfile
import os

st.title("Clinical Trial Document Assistant 🏥")

uploaded_file = st.file_uploader(
    "\n"
    "Upload a clinical trial document (PDF or DOCX).", 
    type=["pdf", "docx"]
)

if uploaded_file is not None:
    # ✅ save with correct extension
    ext = ".pdf" if uploaded_file.name.endswith(".pdf") else ".docx"
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    # ✅ create chain only once
    if "rag_chain" not in st.session_state:
        with st.spinner("Loading document... this may take a moment for large files!"):
            st.session_state.rag_chain = create_rag_chain(tmp_file_path)
        st.success("Document loaded! Ask your questions below.")

    # ✅ initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ✅ show previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # ✅ chat input
    question = st.chat_input("Ask a question about the clinical trial...")

    if question:
        # show user message
        with st.chat_message("user"):
            st.write(question)
        st.session_state.messages.append({"role": "user", "content": question})

        # build chat history string from previous messages
        chat_history = "\n".join([
            f"{m['role'].upper()}: {m['content']}"
            for m in st.session_state.messages[:-1]  # exclude current question
        ])

        # get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.rag_chain.invoke({
                        "question": question,
                        "chat_history": chat_history
                    })
                    st.write(response)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response
                    })
                except Exception as e:
                    error = str(e).lower()
                    if "rate limit" in error or "429" in error:
                        st.warning("⚠️ API limit reached! Please wait a moment.")
                    else:
                        st.error("Something went wrong. Please try again!")