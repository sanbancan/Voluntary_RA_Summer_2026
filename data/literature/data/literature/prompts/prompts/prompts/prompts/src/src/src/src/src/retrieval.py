import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .claude_client import client

def chunk_text(text, chunk_size=900, overlap=150):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + chunk_size]))
        i += max(1, chunk_size - overlap)
    return chunks

def embed_texts(texts):
    resp = client.embeddings.create(
        model="text-embedding-3-large",
        input=texts
    )
    return np.array([x.embedding for x in resp.data])

class SimpleVectorStore:
    def __init__(self):
        self.chunks = []
        self.embeddings = None

    def build(self, docs):
        self.chunks = []
        texts = []
        for doc in docs:
            text = doc.get("text", "")
            meta = doc.get("meta", {})
            for chunk in chunk_text(text):
                self.chunks.append({"text": chunk, "meta": meta})
                texts.append(chunk)
        self.embeddings = embed_texts(texts) if texts else np.zeros((0, 1))

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump({"chunks": self.chunks, "embeddings": self.embeddings}, f)

    @classmethod
    def load(cls, path):
        with open(path, "rb") as f:
            obj = pickle.load(f)
        s = cls()
        s.chunks = obj["chunks"]
        s.embeddings = obj["embeddings"]
        return s

    def search(self, query, top_k=5):
        if self.embeddings is None or len(self.chunks) == 0:
            return []
        q_emb = embed_texts([query])
        sims = cosine_similarity(q_emb, self.embeddings)[0]
        idxs = np.argsort(-sims)[:top_k]
        return [
            {"text": self.chunks[i]["text"], "meta": self.chunks[i]["meta"], "score": float(sims[i])}
            for i in idxs
        ]

def rerank_by_keywords(query, candidates):
    q_terms = set(query.lower().split())
    scored = []
    for c in candidates:
        t_terms = set(c["text"].lower().split())
        lexical = len(q_terms & t_terms)
        score = 0.7 * c["score"] + 0.3 * lexical
        scored.append({**c, "rerank_score": score})
    return sorted(scored, key=lambda x: x["rerank_score"], reverse=True)
