from components.conversation_generation.prompts import TURN_BASED_CONVERSATION_PROMPT
from langchain_core.prompts.chat import ChatPromptTemplate
from schemas.conversation import Conversation


turn_based_conversation_generation_prompt_template = ChatPromptTemplate.from_messages([
    ("system", TURN_BASED_CONVERSATION_PROMPT)
])

def create_turn_based_conversation_generation_chain(llm): 
    return turn_based_conversation_generation_prompt_template | llm.with_structured_output(Conversation).with_retry()