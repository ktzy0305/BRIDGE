from pydantic import BaseModel, Field
from typing import List, Literal

class Persona(BaseModel):    
    name: str
    age_range: str
    gender: str
    background: str
    mental_health_symptoms: str
    perspective: str
    motivations: str
    emotional_state: str
    needs: str
    conversational_stance: str
    type: Literal['Identified', 'Diversified']
    
class PersonaList(BaseModel):
    personas: List[Persona] = Field(description="List of personas")
    