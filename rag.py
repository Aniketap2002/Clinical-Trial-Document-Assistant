from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os

load_dotenv()

#formatting the output to include source pages/mets data

def format_docs(docs):
    return "\n\n".join(
        f"[Page {doc.metadata.get('page', 'unknown')}] \n {doc.page_content}" 
        for doc in docs)

def create_rag_chain(file_path):
    model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)

    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyMuPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    else:        
        raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=250)
    texts = text_splitter.split_documents(documents=document)

    for i, doc in enumerate(texts):
        if ext == ".pdf":
            doc.metadata["page"] = doc.metadata.get("page", i + 1)  # bcoz for pdf, page number is already in metadata, but for docx we need to add section number.
        elif ext == ".docx":
            doc.metadata["page"] = f"section {i + 1}" # for docx, we don't have page number, so we can use section number instead.

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_stores = FAISS.from_documents(documents=texts, embedding=embeddings)

    retriever = vector_stores.as_retriever(search_kwargs={"k": 8})

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a clinical trial document assistant.
    Use the context below to answer the question accurately.

    Rules:
    1. Only answer from the provided context
    2. If not in context say 'Not found in document'
    3. Always end with all the source pages used to answer the question in the format: [source pages: x, y, z]
    4. Never make up information
    5. Be precise

    Previous conversation:
    {chat_history}

    Context: {context}"""),
    ("human", "{question}")
    ])


    parser = StrOutputParser()

    # ✅ chain now accepts dict with question + chat_history
    chain = (
        {
            "context": lambda x: format_docs(retriever.invoke(x["question"])),
            "question": lambda x: x["question"],
            "chat_history": lambda x: x.get("chat_history", "")
        }
        | prompt
        | model
        | parser
    )

    return chain


#if __name__ == "__main__":
#    chain = create_rag_chain("test_report-1.pdf")
#    result = chain.invoke({"question": "What drug is being studied?", "chat_history": ""})
#    print(result)
