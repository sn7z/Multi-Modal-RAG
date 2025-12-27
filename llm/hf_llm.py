# llm/hf_llm.py

from transformers import pipeline

class HFRAGLLM:
    def __init__(self, model_name: str = "google/flan-t5-base", max_new_tokens: int = 256, temperature: float = 0.2):
        self.generator = pipeline(
            "text2text-generation",
            model=model_name,
            tokenizer=model_name,
            device=-1
        )
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature

    def _build_prompt(self, context: str, question: str) -> str:
        
        prompt = f""" You are an intelligent assistant answering questions strictly using the provided context.
If the answer is not present in the context, say:
"I could not find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
        return prompt.strip()

    def generate_answer(self, query: str, retrieved_chunks: list):
        
        #Generate an answer using retrieved RAG context.
        context = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
        # Optional safety trim
        context = context[:2500]

        prompt = self._build_prompt(context, query)

        response = self.generator(
            prompt,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            do_sample=False
        )

        return response[0]["generated_text"]