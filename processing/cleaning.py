# processing/cleaner.py
import re

def clean_text(text: str) -> str:
    # Remove excessive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove multiple spaces
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Strip trailing whitespace
    text = text.strip()

    return text