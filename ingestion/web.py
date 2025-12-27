# ingestion/web.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def clean_and_validate_url(url: str) -> str:
    """
    Clean, normalize, and validate a URL.
    Raises ValueError if invalid.
    """
    if not url:
        raise ValueError("Empty URL")

    # Strip whitespace and junk characters
    url = url.strip()

    # Remove trailing punctuation users often paste
    url = url.rstrip(".,;-")

    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    # Validate hostname
    if not parsed.netloc or "." not in parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")

    return url


def load_website(url, timeout=10):
    try:
        url = clean_and_validate_url(url)

        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

    except Exception as e:
        raise RuntimeError(f"Website ingestion failed: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    metadata = {
        "source": url,
        "type": "website"
    }

    return text, metadata