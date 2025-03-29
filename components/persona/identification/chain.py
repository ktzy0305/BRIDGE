from components.persona.identification.prompt import PERSONA_INDENTIFICATION_PROMPT
from langchain_core.prompts.chat import ChatPromptTemplate
from schemas.persona import Persona

persona_indentification_prompt_template = ChatPromptTemplate.from_messages([
    ("system", PERSONA_INDENTIFICATION_PROMPT)
])

def create_persona_identification_chain(llm):
    return persona_indentification_prompt_template | llm.with_structured_output(Persona).with_retry()