import streamlit as st

# -----------------------------
# Imports (your modules)
# -----------------------------
from ingestion.ingest import ingest_files, ingest_url
from processing.process import process_documents
from embeddings.embedder import HFEmbedder
from vectorstore.chroma_store import ChromaVectorStore
from retriever.retriever import Retriever
from llm.hf_llm import HFRAGLLM
from utils.source_attribution import SourceAttributor
from utils.confidence import ConfidenceScorer


# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(
    page_title="Multimodal RAG (Free & Local)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark UI
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 2rem;
    }
    
    /* Card styling */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    /* Override default text colors */
    .stApp, .stApp p, .stApp span, .stApp div {
        color: #e2e8f0;
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(139, 92, 246, 0.3);
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-title h1 {
        background: linear-gradient(120deg, #a78bfa, #ec4899, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        padding: 0;
    }
    
    .subtitle {
        color: #c4b5fd;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Chat container */
    .chat-container {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 2rem;
        border: 1px solid rgba(139, 92, 246, 0.2);
        animation: fadeIn 1s ease-out;
    }
    
    /* Question/Answer cards */
    .qa-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #252540 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        border: 1px solid rgba(139, 92, 246, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: slideUp 0.5s ease-out;
    }
    
    .qa-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(139, 92, 246, 0.4);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .question-box {
        background: linear-gradient(120deg, #8b5cf6, #6366f1);
        color: #ffffff;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }
    
    .answer-box {
        background: linear-gradient(135deg, #2d2d44 0%, #1e1e2e 100%);
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #8b5cf6;
        margin-bottom: 1rem;
        line-height: 1.8;
        font-size: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    /* Confidence badge */
    .confidence-badge {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 1rem 0;
        font-size: 0.95rem;
        animation: pulse 2s infinite;
    }
    
    .confidence-high {
        background: linear-gradient(120deg, #10b981, #059669);
        color: #ffffff;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    .confidence-medium {
        background: linear-gradient(120deg, #f59e0b, #d97706);
        color: #ffffff;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }
    
    .confidence-low {
        background: linear-gradient(120deg, #ef4444, #dc2626);
        color: #ffffff;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(120deg, #8b5cf6, #6366f1);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(139, 92, 246, 0.4);
        font-size: 1rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6);
        background: linear-gradient(120deg, #7c3aed, #4f46e5);
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        background: linear-gradient(135deg, #2d2d44, #1e1e2e);
        color: #e2e8f0 !important;
        border-radius: 12px;
        border: 2px solid rgba(139, 92, 246, 0.3);
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
        background: linear-gradient(135deg, #2d2d44, #252540);
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #94a3b8 !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #2d2d44, #1e1e2e);
        border-radius: 12px;
        border: 2px dashed rgba(139, 92, 246, 0.4);
        padding: 1rem;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(120deg, #2d2d44, #252540);
        border-radius: 10px;
        font-weight: 600;
        color: #e2e8f0 !important;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    [data-testid="stExpander"] {
        background: linear-gradient(135deg, #1e1e2e, #252540);
        border-radius: 10px;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    /* Success/Warning messages */
    .stSuccess {
        background: linear-gradient(135deg, #065f46, #047857);
        color: white !important;
        border-radius: 10px;
        animation: slideUp 0.5s ease-out;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #92400e, #b45309);
        color: white !important;
        border-radius: 10px;
        animation: slideUp 0.5s ease-out;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #1e40af, #1e3a8a);
        color: white !important;
        border-radius: 10px;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #2d2d44, #1e1e2e);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #c4b5fd !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(139, 92, 246, 0.3) !important;
    }
    
    /* Caption text */
    .stCaption, em, i {
        color: #94a3b8 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown("""
    <div class="main-title">
        <h1>🚀 Multimodal RAG System</h1>
        <p class="subtitle">📄 PDF · 📝 TXT · 📋 Markdown · 🌐 Website</p>
    </div>
""", unsafe_allow_html=True)


# -----------------------------
# CACHED RESOURCES
# -----------------------------
@st.cache_resource
def load_embedder():
    return HFEmbedder()

@st.cache_resource
def load_vectorstore():
    store = ChromaVectorStore()
    collection = store.create_collection()
    return store, collection

@st.cache_resource
def load_llm():
    return HFRAGLLM()

@st.cache_resource
def load_utils():
    return SourceAttributor(), ConfidenceScorer()


# -----------------------------
# Session State
# -----------------------------
if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -----------------------------
# Sidebar – Document Ingestion
# -----------------------------
st.sidebar.markdown("### 📂 Data Ingestion")
st.sidebar.markdown("---")

uploaded_files = st.sidebar.file_uploader(
    "📤 Upload Documents",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True
)

url = st.sidebar.text_input("🔗 Add Website URL", placeholder="https://example.com")

index_button = st.sidebar.button("🔌 Index Documents", use_container_width=True)

# Sidebar stats
if st.session_state.indexed:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 System Status")
    st.sidebar.success("✅ Documents Indexed")
    st.sidebar.metric("💬 Total Conversations", len(st.session_state.chat_history))

# Clear conversation button
if st.session_state.chat_history:
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ Clear Conversations", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Clear cache/vectors button (placed after loading components)
if st.session_state.indexed:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚠️ Danger Zone")
    clear_vectors_button = st.sidebar.button("🔥 Clear Vector Database", use_container_width=True, type="secondary")

# Clear conversation button
if st.session_state.chat_history:
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ Clear Conversations", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


# -----------------------------
# Load Core Components
# -----------------------------
embedder = load_embedder()
vectorstore, collection = load_vectorstore()
llm = load_llm()
source_attributor, confidence_scorer = load_utils()


# -----------------------------
# INDEXING PIPELINE
# -----------------------------
if index_button:
    with st.spinner("🔄 Indexing documents..."):

        documents = []

        if uploaded_files:
            documents.extend(ingest_files(uploaded_files))

        if url:
            documents.extend(ingest_url(url))

        if not documents:
            st.warning("⚠️ Please upload documents or provide a URL.")
        else:
            # Chunking
            chunked_docs = process_documents(
                documents,
                chunk_size=1000,
                chunk_overlap=200
            )

            # Embeddings
            embeddings = embedder.embed_texts(
                [d["text"] for d in chunked_docs]
            )

            # Store vectors
            vectorstore.add_documents(
                collection=collection,
                docs=chunked_docs,
                embeddings=embeddings
            )

            st.session_state.indexed = True
            st.success(f"✨ Indexed {len(chunked_docs)} chunks successfully!")


# Clear vectors handler (placed after components are loaded)
if 'clear_vectors_button' in locals() and clear_vectors_button:
    vectorstore.clear_collection(collection)
    st.session_state.indexed = False
    st.session_state.chat_history = []
    st.rerun()


# -----------------------------
# Chat Interface
# -----------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown("### 💬 Ask Questions")

query = st.text_input(
    "What would you like to know?",
    placeholder="e.g. What is Retrieval Augmented Generation?",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ask_button = st.button("🚀 Ask Question", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# QUERY → RETRIEVE → GENERATE
# -----------------------------
if ask_button and query:
    if not st.session_state.indexed:
        st.warning("⚠️ Please index documents first.")
    else:
        with st.spinner("🔍 Retrieving & generating answer..."):

            # Retrieve
            retriever = Retriever(
                embedder=embedder,
                vectorstore=vectorstore,
                collection=collection
            )

            retrieved_chunks = retriever.retrieve(
                query=query,
                top_k=5
            )

            # Confidence
            confidence = confidence_scorer.compute_confidence(
                retrieved_chunks
            )

            # Generate Answer
            answer = llm.generate_answer(
                query=query,
                retrieved_chunks=retrieved_chunks
            )

            # Source Attribution
            sources = source_attributor.format_sources(
                retrieved_chunks
            )

            # Save history
            st.session_state.chat_history.append({
                "query": query,
                "answer": answer,
                "confidence": confidence,
                "sources": sources
            })


# -----------------------------
# Display Chat History
# -----------------------------
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 📜 Conversation History")
    
    for idx, chat in enumerate(reversed(st.session_state.chat_history)):
        st.markdown('<div class="qa-card">', unsafe_allow_html=True)
        
        # Question
        st.markdown(f'<div class="question-box">❓ {chat["query"]}</div>', unsafe_allow_html=True)
        
        # Answer
        st.markdown(f'<div class="answer-box">{chat["answer"]}</div>', unsafe_allow_html=True)
        
        # Confidence badge
        conf_percent = chat['confidence']['confidence_percent']
        conf_status = chat['confidence']['status'].lower()
        
        if conf_status == 'high':
            badge_class = 'confidence-high'
            emoji = '🟢'
        elif conf_status == 'medium':
            badge_class = 'confidence-medium'
            emoji = '🟡'
        else:
            badge_class = 'confidence-low'
            emoji = '🔴'
        
        st.markdown(
            f'<div class="confidence-badge {badge_class}">'
            f'{emoji} Confidence: {conf_percent} ({chat["confidence"]["status"]})'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Sources
        with st.expander("📌 View Sources"):
            for source, chunks in chat["sources"].items():
                st.markdown(f"**📄 {source}**")
                for c in chunks:
                    st.markdown(
                        f"- **Chunk {c['chunk_id']}** "
                        f"(Relevance Score: {round(c['score'], 3)})"
                    )
                    st.caption(f"_{c['text_preview']}_")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if idx < len(st.session_state.chat_history) - 1:
            st.markdown("<br>", unsafe_allow_html=True)
else:
    st.info("💡 Index some documents and start asking questions!")


# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #c4b5fd; font-size: 0.9rem;'>"
    "Powered by 🤗 Hugging Face & ChromaDB | Built with ❤️ using Streamlit"
    "</p>",
    unsafe_allow_html=True
)