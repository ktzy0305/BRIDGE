from pydantic import BaseModel, Field
from typing import List, Literal

class ConversationalSubtopic(BaseModel):
    subtopic: str
    type: Literal['Identified', 'Diversified']

class ConversationalSubtopics(BaseModel):
    conversational_subtopics: List[ConversationalSubtopic] = Field(
        description="Generated conversational subtopics from an input post and topic."
    )
