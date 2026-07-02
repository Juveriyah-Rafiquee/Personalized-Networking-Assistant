# app/services/event_analyzer.py

from transformers import pipeline
from app.config import MODEL_NAMES

classifier = pipeline("zero-shot-classification", model=MODEL_NAMES["event_analysis"])

CANDIDATE_LABELS = [
    "artificial intelligence", "healthcare", "blockchain", "education",
    "sustainability", "finance", "technology", "leadership",
    "entrepreneurship", "climate change"
]

def extract_event_themes(description: str, candidate_labels=None):
    if candidate_labels is None:
        candidate_labels = CANDIDATE_LABELS
    result = classifier(description, candidate_labels)
    return result["labels"][:3]  # top 3 themes
