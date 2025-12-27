# vectorstore/chroma_store.py
import chromadb
import uuid
from chromadb.config import Settings

class ChromaVectorStore:
    def __init__(self, persist_dir="/tmp/chroma"):
        self.client = chromadb.Client(
            Settings(
                persist_directory=persist_dir,
                anonymized_telemetry=False
            )
        )

    def create_collection(self, name="rag_collection"):
        return self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, collection, docs, embeddings):
        collection.add(
            documents=[d["text"] for d in docs],
            metadatas=[d["metadata"] for d in docs],
            ids=[str(uuid.uuid4()) for _ in range(len(docs))],
            embeddings=embeddings
        )

    def similarity_search(self, collection, query_embedding, k=5):
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results