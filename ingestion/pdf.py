# ingestion/pdf_loader.py
import fitz  # PyMuPDF

def load_pdf(file, max_pages=10):
    """
    Load text from PDF file.
    """
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""

    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        text += page.get_text()

    metadata = {
        "source": file.name,
        "type": "pdf",
        "pages_used": min(len(doc), max_pages)
    }

    return text, metadata