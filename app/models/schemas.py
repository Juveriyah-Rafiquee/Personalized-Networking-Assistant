# app/models/schemas.py

from pydantic import BaseModel
from typing import List

class EventInput(BaseModel):
    description: str

class UserInterests(BaseModel):
    interests: List[str]

class ConversationRequest(BaseModel):
    description: str
    interests: List[str]
    bio: str

class ConversationResponse(BaseModel):
    topics: List[str]
    facts: List[str]
    suggestions: List[str]

class FactCheckRequest(BaseModel):
    query: str

class FactCheckResponse(BaseModel):
    summary: str
