import numpy as np

def predict_weak_topics(tag_stats: dict, user_rating: int) -> list:
    results = []
    for tag, stats in tag_stats.items():
        score = _weakness_score(stats, user_rating)
        results.append({
            "tag": tag,
            "weakness_score": round(score, 3),
            "attempts": stats["attempts"],
            "solved": stats["solved"],
            "success_rate": stats["success_rate"],
            "avg_problem_rating": stats["avg_problem_rating"],
            "recommendation": _get_recommendation(score),
        })
    results.sort(key=lambda x: x["weakness_score"], reverse=True)
    return results

def _weakness_score(stats: dict, user_rating: int) -> float:
    sr = stats["success_rate"]
    attempts = min(stats["attempts"], 50)
    avg_r = stats["avg_problem_rating"]
    attempt_weight = np.log1p(attempts) / np.log1p(50)
    difficulty_factor = 1.0
    if avg_r > 0 and user_rating > 0:
        relative = avg_r / user_rating
        if relative < 0.7:
            difficulty_factor = 1.5
        elif relative > 1.3:
            difficulty_factor = 0.8
    return min((1 - sr) * attempt_weight * difficulty_factor, 1.0)

def _get_recommendation(score: float) -> str:
    if score > 0.7:
        return "Critical — Daily practice needed"
    elif score > 0.4:
        return "Needs work — Practice 3x/week"
    elif score > 0.2:
        return "Moderate — Review concepts"
    return "Strong — Keep it up"