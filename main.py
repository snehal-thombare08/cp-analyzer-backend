from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fetcher import get_user_info, get_submissions, get_rating_history
from preprocessor import process_submissions, compute_tag_stats
from model import predict_weak_topics

app = FastAPI(title="CP Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/user/{handle}")
async def user_profile(handle: str):
    try:
        return get_user_info(handle)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/analyze/{handle}")
async def analyze(handle: str, count: int = 500):
    try:
        user = get_user_info(handle)
        subs = get_submissions(handle, count)
        df = process_submissions(subs)
        tag_stats = compute_tag_stats(df)
        weaknesses = predict_weak_topics(tag_stats, user.get("rating", 1200))
        return {
            "handle": handle,
            "rating": user.get("rating"),
            "rank": user.get("rank"),
            "total_submissions": len(subs),
            "weaknesses": weaknesses[:15],
            "tag_stats": tag_stats,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rating-history/{handle}")
async def rating_history(handle: str):
    try:
        return get_rating_history(handle)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
