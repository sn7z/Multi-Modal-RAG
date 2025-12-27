from ingestion.pdf import load_pdf
from ingestion.web import load_website
from ingestion.text import load_txt
from ingestion.md import load_md

def ingest(files):
    documets = []
    
    for file in files:
        if file.name.endswith(".pdf"):
            text, metadata = load_pdf(file)
        elif file.name.endswith(".txt"):
            text, metadata = load_txt(file)
        elif file.name.endswith(".md"):
            text, metadata = load_md(file)
        else:
            continue  # Unsupported file type
    
    documets.append({
        "text" : text,
        "metadata" : metadata
    })
    
    return documets

def ingest_website(urls):
    documents = []
    
    for url in urls:
        text, metadata = load_website(url)
        documents.append({
            "text": text,
            "metadata": metadata
        })
    
    return documents