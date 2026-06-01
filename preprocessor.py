import pandas as pd
from collections import defaultdict

def process_submissions(submissions: list) -> pd.DataFrame:
    records = []
    for sub in submissions:
        if "problem" not in sub:
            continue
        prob = sub["problem"]
        records.append({
            "verdict": sub.get("verdict", "UNKNOWN"),
            "rating": prob.get("rating", 0),
            "tags": prob.get("tags", []),
            "time_consumed": sub.get("timeConsumedMillis", 0),
            "lang": sub.get("programmingLanguage", ""),
        })
    return pd.DataFrame(records)

def compute_tag_stats(df: pd.DataFrame) -> dict:
    tag_data = defaultdict(lambda: {"attempts": 0, "solved": 0, "ratings": []})
    for _, row in df.iterrows():
        for tag in row["tags"]:
            tag_data[tag]["attempts"] += 1
            if row["verdict"] == "OK":
                tag_data[tag]["solved"] += 1
            if row["rating"] > 0:
                tag_data[tag]["ratings"].append(row["rating"])
    stats = {}
    for tag, d in tag_data.items():
        attempts = d["attempts"]
        solved = d["solved"]
        avg_rating = sum(d["ratings"]) / len(d["ratings"]) if d["ratings"] else 0
        stats[tag] = {
            "attempts": attempts,
            "solved": solved,
            "success_rate": round(solved / attempts, 3) if attempts > 0 else 0,
            "avg_problem_rating": round(avg_rating),
        }
    return stats