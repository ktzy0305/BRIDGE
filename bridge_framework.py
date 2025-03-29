from components.conversation_generation.chain import create_turn_based_conversation_generation_chain
from components.conversation_generation.prompts import PERSONA_B_INFORMATION
from components.conversational_subtopic.diversification.chain import create_conversational_subtopic_diversification_chain
from components.conversational_subtopic.identification.chain import create_conversational_subtopic_identification_chain
from components.persona.diversification.chain import create_persona_diversification_chain
from components.persona.identification.chain import create_persona_identification_chain

from db.queries import fetch_all_posts_in_topic

from llm import gpt_4o

from pathlib import Path

from schemas.conversation import ConversationTurn
from schemas.persona import Persona

from tqdm import tqdm
from typing import List

from utils.data_processing import save_to_json
from utils.dialogue import create_linear_thread_string
from utils.metrics import calculate_help_seeker_interactivity, determine_turn_count

# Chains
conversational_subtopic_diversification_chain = create_conversational_subtopic_diversification_chain(gpt_4o)
conversational_subtopic_identification_chain = create_conversational_subtopic_identification_chain(gpt_4o)
persona_diversification_chain = create_persona_diversification_chain(gpt_4o)
persona_identification_chain = create_persona_identification_chain(gpt_4o)
turn_based_conversation_generation_chain = create_turn_based_conversation_generation_chain(gpt_4o)

# Requests For LangChain Batching

def generate_persona_requests(help_seeker_posts):
    persona_requests = []

    for idx, nodes in tqdm(enumerate(help_seeker_posts), total=len(help_seeker_posts), desc="Generating Persona Requests"):
        
        (post_node, user_node, wrote_rel, topic_node, belongs_rel) = nodes
        
        persona_request = { 
            'topic': topic_node.topic,
            'username': user_node.username,
            'post': post_node.post_content
        }
        
        persona_requests.append(persona_request)
        
    return persona_requests

def generate_conversational_subtopic_requests(n_subtopics: int, help_seeker_posts):
    conversational_subtopics_requests = []

    for idx, nodes in tqdm(enumerate(help_seeker_posts), total=len(help_seeker_posts), desc="Generating Conversational Subtopic Requests"):
        
        (post_node, user_node, wrote_rel, topic_node, belongs_rel) = nodes
        
        conversational_subtopics_request = {
            'topic': topic_node.topic,
            'username': user_node.username,
            'forum_topic_thread': create_linear_thread_string(fetch_all_posts_in_topic(topic_id=topic_node.topic_id)),
            'n' : n_subtopics
        }
        
        conversational_subtopics_requests.append(conversational_subtopics_request)
        
    return conversational_subtopics_requests
        
def generate_diversified_personas_requests(
    n_personas: int, 
    help_seeker_posts,
    personas_by_topic, 
    conversational_subtopics_by_topic
):
    diversified_personas_requests = []

    for idx, nodes in tqdm(enumerate(help_seeker_posts), total=len(help_seeker_posts), desc="Generating Diversified Persona Requests"):
        
        (post_node, user_node, wrote_rel, topic_node, belongs_rel) = nodes    
        
        diversified_personas_input = {
            'topic_id': topic_node.topic_id,
            'conversational_subtopics': [cs.model_dump() for cs in conversational_subtopics_by_topic[idx].conversational_subtopics],
            'original_persona': personas_by_topic[idx].model_dump(),
            'post': post_node.post_content,
            'n': n_personas
        }
        
        diversified_personas_requests.append(diversified_personas_input)
        
    return diversified_personas_requests

def generate_diversified_conversational_subtopics_requests(
    n_conversational_subtopics: int,
    help_seeker_posts,
    personas_by_topic, 
    conversational_subtopics_by_topic
    
):
    diversified_conversational_subtopics_requests = []

    for idx, nodes in tqdm(enumerate(help_seeker_posts), total=len(help_seeker_posts), desc="Generating Diversified Conversation Subtopic Requests"):
        
        (post_node, user_node, wrote_rel, topic_node, belongs_rel) = nodes
        
        diversified_conversational_subtopics_input = {
            'conversational_subtopics': [cs.model_dump() for cs in conversational_subtopics_by_topic[idx].conversational_subtopics],
            'persona': personas_by_topic[idx].model_dump(),
            'topic': topic_node.topic,
            'forum_topic_thread': create_linear_thread_string(fetch_all_posts_in_topic(topic_id = topic_node.topic_id)),
            'n': n_conversational_subtopics
        }
        
        diversified_conversational_subtopics_requests.append(diversified_conversational_subtopics_input)
        
    return diversified_conversational_subtopics_requests
        
# Calculate Batch Size

def get_batch_indices(num, batch_size):
    start_indices = list(range(0, num, batch_size))
    end_indices = [min(start + batch_size - 1, num - 1) for start in start_indices]
    batch_numbers = list(range(1, len(start_indices) + 1))
    return start_indices, end_indices, batch_numbers

# Dialogue Generation

def dialogue_generation(
    help_seeker_posts,
    output_path: str,
    num_conversational_subtopics = 2,
    num_diversified_personas = 2,
    num_diversified_conversational_subtopics = 2,
    max_turn_count = 42,
    batch_size = 50
):
    persona_requests = generate_persona_requests(help_seeker_posts)
    personas_by_topic = persona_identification_chain.batch(persona_requests)

    conversational_subtopics_requests = generate_conversational_subtopic_requests(
        n_subtopics=num_conversational_subtopics,
        help_seeker_posts = help_seeker_posts
    )
    
    conversational_subtopics_by_topic = conversational_subtopic_identification_chain.batch(
        conversational_subtopics_requests
    )
    
    diversified_personas_requests = generate_diversified_personas_requests(
        n_personas=num_diversified_personas,
        help_seeker_posts=help_seeker_posts,
        personas_by_topic = personas_by_topic,
        conversational_subtopics_by_topic=conversational_subtopics_by_topic
    )
    
    diversified_personas_by_topic = persona_diversification_chain.batch(
        diversified_personas_requests
    )
    
    diversified_conversational_subtopics_requests = generate_diversified_conversational_subtopics_requests(
        n_conversational_subtopics=num_diversified_conversational_subtopics,
        help_seeker_posts=help_seeker_posts,
        personas_by_topic=personas_by_topic,
        conversational_subtopics_by_topic=conversational_subtopics_by_topic
    )

    diversified_conversational_subtopics_by_topic = conversational_subtopic_diversification_chain.batch(
        diversified_conversational_subtopics_requests
    )
    
    start_indices, end_indices, batch_nums = get_batch_indices(len(help_seeker_posts), batch_size)
    
    for start_idx, end_idx, batch_no in zip(start_indices, end_indices, batch_nums):
        json_data = []

        for index in tqdm(
            range(start_idx, end_idx + 1), 
            total=len(range(start_idx, end_idx + 1)), 
            desc=f"Generating Conversation Requests: Batch {batch_no} of {len(batch_nums)}"
        ):
            (post_node, user_node, wrote_rel, topic_node, belongs_rel) = help_seeker_posts[index]
            all_personas: List[Persona] = []
            all_conversational_subtopics: List[str] = []

            persona_input = { 
                'topic': topic_node.topic,
                'username': user_node.username,
                'post': post_node.post_content
            }

            conversational_subtopics_input = {
                'topic': topic_node.topic,
                'username': user_node.username,
                'forum_topic_thread': create_linear_thread_string(fetch_all_posts_in_topic(topic_id=topic_node.topic_id)),
                'n' : num_conversational_subtopics
            }

            diversified_personas_input = {
                'conversational_subtopics' : [cs.model_dump() for cs in conversational_subtopics_by_topic[index].conversational_subtopics],
                'original_persona': personas_by_topic[index].model_dump(),
                'post': post_node.post_content,
                'n': num_diversified_personas
            }

            diversified_conversational_subtopics_input = {
                'conversational_subtopics' : [cs.model_dump() for cs in conversational_subtopics_by_topic[index].conversational_subtopics],
                'persona': personas_by_topic[index].model_dump(),
                'topic': topic_node.topic,
                'forum_topic_thread': create_linear_thread_string(fetch_all_posts_in_topic(topic_id = topic_node.topic_id)),
                'n': num_diversified_conversational_subtopics
            } 

            interactivity_metrics = calculate_help_seeker_interactivity(fetch_all_posts_in_topic(topic_id = topic_node.topic_id))
            turn_count = determine_turn_count(interactivity_metrics, max_turn_count)
            
            topic_structure = {
                "topic_id" : topic_node.topic_id,
                "topic" : topic_node.topic,
                "help_seeker_post" : post_node.post_content,
                "interactivity_metrics" : interactivity_metrics,
                "determined_conversation_turns" : turn_count,
                "llm_inputs" : {
                    "persona" : persona_input,
                    "conversational_subtopics" : conversational_subtopics_input,
                    "diversified_personas" : diversified_personas_input,
                    "diversified_conversational_subtopics" : diversified_conversational_subtopics_input
                },
                "conversations" : []
            }
            
            all_personas.append(personas_by_topic[index])
            all_personas.extend(diversified_personas_by_topic[index].personas)
            all_conversational_subtopics.extend(conversational_subtopics_by_topic[index].conversational_subtopics)
            all_conversational_subtopics.extend(diversified_conversational_subtopics_by_topic[index].conversational_subtopics)

            
            conversation_inputs_by_topic = []
            conversation_requests_by_topic = []
            
            for conversational_subtopic in all_conversational_subtopics:
                for persona in all_personas:
                    
                    conversation_inputs = {
                        "persona_a": persona.model_dump(),
                        "persona_b": PERSONA_B_INFORMATION,
                        "conversational_subtopic": conversational_subtopic.model_dump(),
                        "forum_topic_thread": create_linear_thread_string(fetch_all_posts_in_topic(topic_id = topic_node.topic_id)),
                        "n": turn_count
                    }
                    
                    conversation_request = {
                        "persona_a": persona.model_dump(),
                        "persona_b": PERSONA_B_INFORMATION,
                        "conversational_subtopic": conversational_subtopic.subtopic,
                        "forum_topic_thread": create_linear_thread_string(fetch_all_posts_in_topic(topic_id = topic_node.topic_id)),
                        "n": turn_count
                    }
                    
                    conversation_inputs_by_topic.append(conversation_inputs)
                    conversation_requests_by_topic.append(conversation_request)
                    
            conversations_by_topic = turn_based_conversation_generation_chain.batch(conversation_requests_by_topic)

            for idx, conversation in enumerate(conversations_by_topic):
                conversation_inputs = conversation_inputs_by_topic[idx]
                
                conversation_structure = {
                    "conversation_id" : f"T-{topic_node.topic_id}-C-{idx + 1}", 
                    "conversation_inputs" : conversation_inputs,
                    "dialogue" : []
                }
                    
                for conversation_turn in conversations_by_topic[idx].conversation_turns:
                    c: ConversationTurn = conversation_turn
                    conversation_structure["dialogue"].append({
                        "turn_number": c.turn_number,
                        "speaker_name": c.speaker_name,
                        "utterance": c.utterance,
                        "utterance_source": c.utterance_source.source,
                        "referenced_post_id": c.utterance_source.post_id,
                        "referenced_user": c.utterance_source.username,
                        "referenced_sentence": c.utterance_source.sentence,
                        "reason_for_utterance_generation": c.utterance_source.reason
                    })
            
                topic_structure["conversations"].append(conversation_structure)
            
            json_data.append(topic_structure)
            
        output_path = Path(output_path)
        filename = f'{output_path.stem}_batch_{batch_no}_of_{len(batch_nums)}.json'
        save_path = output_path.with_name(filename)
        save_to_json(json_data=json_data, file_path=save_path)

        print(f"Data saved in {save_path}")