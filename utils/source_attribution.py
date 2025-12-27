# utils/source_attribution.py

from collections import defaultdict

class SourceAttributor:
    def __init__(self):
        pass

    def format_sources(self, retrieved_chunks: list):
        
        sources = defaultdict(list)

        for chunk in retrieved_chunks:
            metadata = chunk.get("metadata", {})
            source_name = metadata.get("source", "unknown")
            chunk_id = metadata.get("chunk_id", -1)
            score = chunk.get("score", None)

            sources[source_name].append({
                "chunk_id": chunk_id,
                "score": score,
                "text_preview": chunk["text"][:300]
            })

        return dict(sources)

    def get_flat_sources(self, retrieved_chunks: list):
        #Returns a simple flat list of sources (for citations).
        
        unique_sources = set()

        for chunk in retrieved_chunks:
            metadata = chunk.get("metadata", {})
            source_name = metadata.get("source", None)
            if source_name:
                unique_sources.add(source_name)

        return list(unique_sources)