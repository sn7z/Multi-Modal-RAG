# ingestion/txt_loader.py

def load_txt(file):
    text = file.read().decode("utf-8")

    metadata = {
        "source": file.name,
        "type": "txt"
    }

    return text, metadata