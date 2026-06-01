import requests

CF_BASE = "https://codeforces.com/api"

def get_user_info(handle: str) -> dict:
    r = requests.get(f"{CF_BASE}/user.info?handles={handle}", timeout=10)
    r.raise_for_status()
    data = r.json()
    if data["status"] != "OK":
        raise ValueError(f"CF API error: {data.get('comment')}")
    return data["result"][0]

def get_submissions(handle: str, count: int = 500) -> list:
    r = requests.get(f"{CF_BASE}/user.status?handle={handle}&count={count}", timeout=15)
    r.raise_for_status()
    data = r.json()
    if data["status"] != "OK":
        raise ValueError(f"CF API error: {data.get('comment')}")
    return data["result"]

def get_rating_history(handle: str) -> list:
    r = requests.get(f"{CF_BASE}/user.rating?handle={handle}", timeout=10)
    r.raise_for_status()
    data = r.json()
    if data["status"] != "OK":
        raise ValueError(f"CF API error: {data.get('comment')}")
    return data["result"]