# retriever/retriever.py

class Retriever:
    def __init__(self, embedder, vectorstore, collection):
        self.embedder = embedder
        self.vectorstore = vectorstore
        self.collection = collection

    def retrieve(self, query: str, top_k: int = 4):
        
        query_embedding = self.embedder.embed_query(query)

        results = self.vectorstore.similarity_search(
            collection=self.collection,
            query_embedding=query_embedding,
            k=top_k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved = []

        for doc, meta, score in zip(documents, metadatas, distances):
            retrieved.append({
                "text": doc,
                "metadata": meta,
                "score": score
            })

        return retrieved