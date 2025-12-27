# processing/chunker.py
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Chunk text into smaller pieces for better processing.
def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    return splitter.split_text(text)