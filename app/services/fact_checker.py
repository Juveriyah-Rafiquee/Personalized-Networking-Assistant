# app/services/fact_checker.py

import requests
from urllib.parse import quote
from app.config import FACT_CHECK_API

HEADERS = {"User-Agent": "PersonalizedNetworkingAssistant/1.0 (student capstone project)"}

def fact_check(query: str) -> str:
    try:
        url = f"{FACT_CHECK_API}/{quote(query)}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return "No summary found."
        data = response.json()
        return data.get("extract", "No summary found.")
    except Exception:
        return "Fact-checking failed."

def fact_check_many(queries: list[str]) -> list[str]:
    return [fact_check(q) for q in queries]