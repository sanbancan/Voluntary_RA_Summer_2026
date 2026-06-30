import os
from .retrieval import SimpleVectorStore

def load_literature_docs(folder="data/literature"):
    docs = []
    for fn in os.listdir(folder):
        if fn.endswith(".txt"):
            path = os.path.join(folder, fn)
            with open(path, "r", encoding="utf-8") as f:
                docs.append({"text": f.read(), "meta": {"filename": fn}})
    return docs

def build_store(out_path="data/vector_store.pkl"):
    store = SimpleVectorStore()
    store.build(load_literature_docs())
    store.save(out_path)
    return out_path
