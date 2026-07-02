# app/routers/conversation.py

from fastapi import APIRouter
from app.models.schemas import (
    EventInput, ConversationRequest, FactCheckRequest,
    ConversationResponse, FactCheckResponse
)
from app.services import event_analyzer, topic_generator, fact_checker, history_logger, feedback_logger

router = APIRouter()


@router.post("/analyze-event")
def analyze_event(data: EventInput):
    themes = event_analyzer.extract_event_themes(data.description)
    return {"topics": themes}


@router.post("/fact-check", response_model=FactCheckResponse)
def fact_check(data: FactCheckRequest):
    # Standalone quick fact-check — independent of starter generation
    summary = fact_checker.fact_check(data.query)
    return FactCheckResponse(summary=summary)


@router.post("/generate-conversation", response_model=ConversationResponse)
def generate_conversation(data: ConversationRequest):
    # 1. Extract themes from the event description
    themes = event_analyzer.extract_event_themes(data.description)

    # 2. Fetch verified facts for those themes BEFORE generating —
    #    this is the grounding step, so the starter is fact-checked
    #    by construction rather than verified after the fact
    facts = fact_checker.fact_check_many(themes)

    # 3. Generate starters using themes + interests + facts as context
    suggestions = topic_generator.generate_topics(themes, data.interests, facts)

    # 4. Log the full session
    history_logger.log_conversation({
        "description": data.description,
        "interests": data.interests,
        "topics": themes,
        "facts": facts,
        "suggestions": suggestions
    })

    return ConversationResponse(topics=themes, facts=facts, suggestions=suggestions)


@router.post("/feedback")
def submit_feedback(suggestion: str, action: str):
    feedback_logger.log_feedback(suggestion, action)
    return {"status": "recorded"}
