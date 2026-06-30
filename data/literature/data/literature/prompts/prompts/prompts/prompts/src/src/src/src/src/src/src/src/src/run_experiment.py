import os
import json
from tqdm import tqdm
from .config import DATA_PATH, OUTPUT_DIR
from .load_data import load_projects
from .workflow import background_step, challenge_step, methods_step, solution_step, evaluation_step
from .ingest import build_store
from .retrieval import SimpleVectorStore, rerank_by_keywords
from .scoring import extract_json, score_rows

def load_notes():
    p = "data/literature/notes.txt"
    return open(p, "r", encoding="utf-8").read() if os.path.exists(p) else ""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs("data", exist_ok=True)

    vector_store_path = build_store()
    projects = load_projects(DATA_PATH)
    store = SimpleVectorStore.load(vector_store_path)
    notes = load_notes()
    results = []

    for p in tqdm(projects):
        query = f"{p['organization']} {p['domain']} {p['summary']}"
        retrieved = store.search(query, top_k=5)
        reranked = rerank_by_keywords(query, retrieved)
        literature_notes = "\n\n".join([x["text"] for x in reranked[:3]]) + "\n\n" + notes

        bg = background_step(p, literature_notes)
        ch = challenge_step(bg)
        mt = methods_step(ch, literature_notes)
        sol = solution_step(p, bg, ch, mt)
        ev = evaluation_step(sol)
        score = extract_json(ev)

        results.append({
            "project_id": p["project_id"],
            "organization": p["organization"],
            "retrieved": reranked,
            "background": bg,
            "challenges": ch,
            "methods": mt,
            "proposal": sol,
            "evaluation": ev,
            "score": score
        })

    with open(os.path.join(OUTPUT_DIR, "proposals.jsonl"), "w", encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    df = score_rows(results)
    df.to_csv(os.path.join(OUTPUT_DIR, "scores.csv"), index=False)

if __name__ == "__main__":
    main()
