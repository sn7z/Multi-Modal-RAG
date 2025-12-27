# ingestion/web_loader.py
import requests
from bs4 import BeautifulSoup

def load_website(url, timeout=10):
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    metadata = {
        "source": url,
        "type": "website"
    }

    return text, metadata