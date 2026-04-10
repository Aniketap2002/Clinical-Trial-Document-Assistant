# Clinical Trial Document Assistant 🏥

An AI-powered RAG (Retrieval Augmented Generation) application that helps biostatisticians, medical writers, and clinical data managers query large clinical trial documents in plain English — with exact page citations for every answer.

---

## The Problem

Clinical trial reports are massive. A single Clinical Study Report (CSR) can be 500-1000+ pages long. Biostatisticians and medical writers spend hours manually searching through these documents to find specific data points, adverse event summaries, endpoint results, or protocol details.

**The current painful process:**
```
Biostatistician receives 891-page trial report
        ↓
Manually searches through document
        ↓
Ctrl+F for specific terms
        ↓
Reads surrounding context to verify
        ↓
Copies data into summary report
        ↓
2-3 days of work for one report 😤
```

---

## The Solution

**Clinical Trial Document Assistant** turns any clinical trial PDF into an intelligent, conversational knowledge base.

```
Upload 891-page clinical trial PDF
        ↓
Ask questions in plain English
        ↓
Get precise answers in seconds
with exact page citations ✅
        ↓
Verify on the cited page
        ↓
2-3 hours instead of days 🔥
```

---

## How It Works — Architecture

```
PDF/DOCX Upload
      ↓
Document Loader (PyMuPDF)
→ Reads and extracts text from PDF
→ Preserves page metadata for citations
      ↓
Text Splitter (RecursiveCharacterTextSplitter)
→ Splits document into 1000 char chunks
→ 250 char overlap to preserve context
      ↓
Embeddings (HuggingFace all-MiniLM-L6-v2)
→ Converts each chunk to 384-dimensional vector
→ Runs locally — no API key needed
      ↓
Vector Store (FAISS)
→ Stores all vectors for fast similarity search
→ Retrieves top 8 most relevant chunks per query
      ↓
RAG Chain (LangChain LCEL)
→ User question → FAISS search → relevant chunks
→ Chunks + question + chat history → Groq LLM
→ LLM answers with page citations
      ↓
Streamlit UI
→ Chat interface with conversation memory
→ Answers with [Source: page X] citations
```

---

## Key Features

- **Plain English Queries** — Ask questions naturally, no special syntax needed
- **Page Citations** — Every answer includes `[Source: page X]` so you can verify
- **Conversation Memory** — Follow-up questions use previous context
- **Large Document Support** — Tested on 891-page FDA clinical trial reports
- **Strict Hallucination Control** — LLM only answers from document context
- **Supports PDF and DOCX** — Upload either format

---

## Example Queries

```
"What drug is being studied in this trial?"
→ Apalutamide (JNJ-56021927) [Source: page 1]

"What is medical resource utilization in this study?"
→ MRU data were collected on Day 1 of Cycle 1 to 6...
  Results will be presented in a separate report. [Source: page 39]

"Who are the principal investigators?"
→ Matthew Raymond Smith, MD, PhD — Massachusetts General Hospital
  Eric Small, MD — University of California San Francisco [Source: page 1]

"What was the primary endpoint?"
→ Metastasis-Free Survival (MFS) in men with high-risk 
  non-metastatic castration-resistant prostate cancer [Source: page 20]
```

---

## Tech Stack

| Component                |           Technology                           | 
-------------------------------------------------------------------------------
| LLM                      |           Groq — Llama 3.1 8B Instant          |
| Embeddings               |           HuggingFace all-MiniLM-L6-v2 (local) |
| Vector Database          |           FAISS                                |
| Framework                |           LangChain LCEL                       |
| UI                       |           Streamlit                            |
| Document Loading         |           PyMuPDF                              |

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Aniketap2002/Clinical-Trial-Document-Assistant.git
cd Clinical-Trial-Document-Assistant
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

**4. Run the app**
```bash
streamlit run app.py
```

**5. Upload any clinical trial PDF and start asking questions!**

---

## Why This Matters for Healthcare AI

Clinical trial data is some of the most complex and high-stakes text in the world. A wrong answer or hallucinated data point could lead to incorrect conclusions about drug safety or efficacy.

This application addresses that with:

- **RAG over pure LLM generation** — answers grounded in actual document content
- **Strict prompt engineering** — LLM instructed to say "Not found in document" rather than guess
- **Page citations** — every answer traceable to a specific page for human verification
- **Temperature = 0.7** — balanced between creativity and factual precision

---

## Future Improvements

- Adaptive RAG — classify question type and retrieve optimal number of chunks
- Multi-document support — query across multiple trial reports simultaneously
- DeepEval integration — automated faithfulness and relevancy testing
- Export conversation as Word report
- HIPAA compliant deployment with Pinecone vector store

---

## Author

**Aniket Prajapati** — Product Developer | GenAI Explorer

- Portfolio: [aniketap2002.github.io](https://aniketap2002.github.io)
- GitHub: [github.com/Aniketap2002](https://github.com/Aniketap2002)
- LinkedIn: [linkedin.com/in/aniket-prajapati-b16704221](https://www.linkedin.com/in/aniket-prajapati-b16704221)
