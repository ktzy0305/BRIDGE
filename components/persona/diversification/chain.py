from components.persona.diversification.prompt import PERSONA_DIVERSIFICATION_PROMPT
from langchain_core.prompts.chat import ChatPromptTemplate
from schemas.persona import PersonaList

persona_diversification_prompt_template = ChatPromptTemplate.from_messages([
    ("system", PERSONA_DIVERSIFICATION_PROMPT)
])

def create_persona_diversification_chain(llm):
    return persona_diversification_prompt_template | llm.with_structured_output(PersonaList).with_retry()