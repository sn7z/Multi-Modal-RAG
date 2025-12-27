# processing/processor.py
from processing.cleaning import clean_text
from processing.chunker import chunk_text

# Convert ingested documents into chunked documents.
def process_documents(documents: list, chunk_size: int = 1000, chunk_overlap: int = 200):
    
    processed_docs = []

    for doc in documents:
        cleaned_text = clean_text(doc["text"])
        chunks = chunk_text(
            cleaned_text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for i, chunk in enumerate(chunks):
            processed_docs.append({
                "text": chunk,
                "metadata": {
                    **doc["metadata"],
                    "chunk_id": i
                }
            })
            
    return processed_docs