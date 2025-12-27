

Multimodal RAG System (Streamlit)
====================================

A **fully-functional, Multimodal Retrieval-Augmented Generation (RAG) application** built with **Streamlit**, supporting **PDF, TXT, Markdown, and Website URLs**, using **free & open-source models**.

This project demonstrates a **complete RAG pipeline** — from ingestion to retrieval, generation, explainability, performance optimization, and vector lifecycle management.

🚀 Features
-----------

### 🔹 Document Ingestion

*   Upload **PDF**, **TXT**, **Markdown** files
    
*   Ingest **Website URLs**
    
*   Robust URL validation & normalization
    
*   Safe handling of invalid inputs
    

### 🔹 RAG Pipeline

*   Text cleaning & chunking
    
*   Semantic embeddings using **Hugging Face**
    
*   Vector storage with **ChromaDB**
    
*   Similarity-based retrieval
    
*   Context-aware answer generation
    

### 🔹 Explainability & Trust

*   **Source attribution** (document + chunk level)
    
*   **Confidence scoring** based on retrieval similarity
    
*   Hallucination-reduction via strict RAG prompting
    

### 🔹 Performance Optimized

*   Cached models & vector store
    
*   Batched embeddings
    
*   Context trimming to respect model limits
    
*   Controlled top-K retrieval
    

### 🔹 Vector Lifecycle Management

*   Clear vector database on demand
    
*   Reset chat & indexing state
    
*   Prevents old documents leaking into new answers
    

### 🔹 Deployment Ready

*   Works on **Streamlit Community Cloud**
    
*   No paid APIs
    
*   CPU-only compatible
    
*   Python 3.10+
    

🧠 Architecture Overview
------------------------
```bash
User
 ↓
Streamlit UI
 ↓
Ingestion (PDF / TXT / MD / Web)
 ↓
Processing (cleaning + chunking)
 ↓
Embeddings (Hugging Face)
 ↓
Vector Store (ChromaDB)
 ↓
Retriever (similarity search)
 ↓
LLM (Hugging Face – RAG prompt)
 ↓
Answer + Confidence + Sources
```

🛠️ Tech Stack
--------------

| Layer       | Technology                        |
| ----------- | --------------------------------- |
| Frontend    | Streamlit                         |
| Language    | Python                            |
| Embeddings  | sentence-transformers             |
| Vector DB   | ChromaDB                          |
| LLM         | Hugging Face (FLAN-T5 by default) |
| Chunking    | LangChain text splitters          |
| PDF Parsing | PyMuPDF                           |
| Web Parsing | Requests + BeautifulSoup          |

📁 Project Structure
--------------------
```bash
.
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── ingestion/
│   ├── ingest.py
│   ├── pdf.py
│   ├── txt.py
│   ├── md.py
│   └── web.py
│
├── processing/
│   ├── cleaner.py
│   ├── chunker.py
│   └── processor.py
│
├── embeddings/
│   └── embedder.py
│
├── vectorstore/
│   └── chroma_store.py
│
├── retriever/
│   └── retriever.py
│
├── llm/
│   └── hf_llm.py
│
├── utils/
│   ├── source_attribution.py
│   └── confidence.py
```
⚙️ Installation & Setup
-----------------------

### 1️⃣ Clone the Repository

```bash   
git clone https://github.com/your-username/multimodal-rag-streamlit.git  cd multimodal-rag-streamlit   
```

### 2️⃣ Create & Activate Virtual Environment

```bash
  python -m venv venv  venv\Scripts\activate    # Windows   # source venv/bin/activate -  Linux / Mac 
```

### 3️⃣ Install Dependencies

``` bash
  pip install -r requirements.txt
```

### 4️⃣ Run the App

```bash   
python -m streamlit run app.py
            or
streamlit run app.py          
```

📦 Requirements
---------------

All dependencies are listed in requirements.txt.
    

> ⚠️ **Do NOT install fitz directly**. Always use pymupdf.

🧪 How to Use
-------------

1.  Upload documents or paste a website URL
    
2.  Click **Index Documents**
    
3.  Ask questions in the chat box
    
4.  View:
    
    *   Generated answer
        
    *   Confidence score
        
    *   Source documents & chunks
        
5.  Use **Clear Vector Store** to reset documents
    

🔐 Safety & Robustness
----------------------

*   Invalid URLs fail safely (no crashes)
    
*   Long contexts are trimmed automatically
    
*   Token limits respected
    
*   Vector store reset prevents stale data usage
    

📈 Performance Optimizations Used
---------------------------------

*   Model & vector store caching
    
*   Batched embedding computation
    
*   Top-K retrieval control
    
*   Context length trimming
    
*   Explicit indexing control
    

🚀 Future Enhancements
----------------------

*   Multi-dataset support
    
*   Dataset selector UI
    
*   Persistent vector storage
    
*   Multi-user isolation
    
*   RAG evaluation metrics
    
*   Advanced reranking

----------------------
