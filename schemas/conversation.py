from pydantic import BaseModel, Field
from typing import List, Optional

class UtteranceSource(BaseModel):
    source: str = Field(description="Either 'Forum' or 'AI Generated'.")
    post_id: Optional[int] = Field(description="Which post_id does the utterance reference from the forum? Fill this if the source is 'Forum'")
    username: Optional[str] = Field(description="Which username does the utterance reference from the forum? Fill this if the source is 'Forum'")
    sentence: Optional[str] = Field(description="What sentence does the utterance reference from the forum? Fill this if the source is 'Forum'")
    reason: Optional[str] = Field(description="Reason for generating the utterance")

class ConversationTurn(BaseModel):
    turn_number: int = Field(description="Conversation Turn Number")
    speaker_name: str = Field(description="Who is speaking which is either Persona A or Persona B")
    utterance: str = Field(description="The dialogue spoken by the speaker")
    utterance_source: UtteranceSource = Field(description="Information source for the speaker's utterance")
    
class Conversation(BaseModel):
    conversation_turns: List[ConversationTurn] = Field(description="Consists a list of conversation turns in numerical order.")
    
## Unused
    
class ExplainableConversationTurn(ConversationTurn):
    utterance_source: UtteranceSource = Field(description="Information source for the speaker's utterance")

class SimpleConversation(BaseModel):
    conversation_turns: List[ConversationTurn] = Field(description="Consists a list of conversation turns in numerical order.")