from components.conversational_subtopic.identification.prompt import CONVERSATIONAL_SUBTOPIC_IDENTIFICATION_PROMPT
from langchain_core.prompts.chat import ChatPromptTemplate
from schemas.conversational_subtopic import ConversationalSubtopics

conversational_subtopic_identification_prompt_template = ChatPromptTemplate.from_messages([
    ("system", CONVERSATIONAL_SUBTOPIC_IDENTIFICATION_PROMPT)
])

def create_conversational_subtopic_identification_chain(llm):
    return conversational_subtopic_identification_prompt_template | llm.with_structured_output(ConversationalSubtopics).with_retry()