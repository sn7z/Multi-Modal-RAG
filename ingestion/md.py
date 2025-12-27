# ingestion/md_loader.py
import markdown
from bs4 import BeautifulSoup

def load_md(file):
    raw_md = file.read().decode("utf-8")
    html = markdown.markdown(raw_md)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    metadata = {
        "source": file.name,
        "type": "markdown"
    }

    return text, metadata