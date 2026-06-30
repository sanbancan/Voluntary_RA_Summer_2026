import json
import re
import pandas as pd

def extract_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {"raw": text}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {"raw": text}

def score_rows(rows):
    out = []
    for r in rows:
        s = r.get("score", {})
        out.append({
            "project_id": r.get("project_id"),
            "organization": r.get("organization"),
            "appropriateness": s.get("appropriateness"),
            "thoroughness": s.get("thoroughness"),
            "feasibility": s.get("feasibility"),
            "expected_effectiveness": s.get("expected_effectiveness"),
        })
    return pd.DataFrame(out)
