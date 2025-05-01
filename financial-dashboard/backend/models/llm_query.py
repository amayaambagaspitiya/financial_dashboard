import os
import json
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load JSON dataset
with open("src/data/processed_dataset.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

df = pd.json_normalize(raw_data)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert rows to text
texts = df.apply(lambda row: f"{row.to_dict()}", axis=1).tolist()
embeddings = model.encode(texts, convert_to_numpy=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Semantic search
def search_context(query, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    results = [texts[i] for i in indices[0]]
    print("Top context retrieved:")
    for i, chunk in enumerate(results, 1):
        print(f"\n--- Result {i} ---\n{chunk}")
    return results

# LLM-powered answer
def answer_query(query, _df):
    top_chunks = search_context(query, top_k=5)
    context = "\n---\n".join(top_chunks)

    prompt = f"""You are a financial analyst. Use the following financial data rows to answer the question.

Data:
{context}

Question: {query}

Answer:"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300,
            timeout=20
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI call failed:", e)
        return f"OpenAI request failed:\n\n{e}"
