from components.persona.identification.prompt import PERSONA_INDENTIFICATION_PROMPT
from response_formats import persona_response_format
from typing import Any, Dict, List, Literal

import json

def generate_persona_prompt_messages(inputs: Dict[str, Any]):
    content = [{
        "role" : "system",
        "content": PERSONA_INDENTIFICATION_PROMPT.format_map(inputs)
    }]
    
    return content

def create_request_body(messages: List[Dict[str, Any]], model:str="gpt-4o"):
    return {
        "model": model,
        "messages": messages,
        "response_format": persona_response_format
    }

def generate_batch_requests(help_seeker_posts):
    batch_requests = []
    
    for idx, nodes in enumerate(help_seeker_posts):
        (post_node, user_node, wrote_rel, topic_node, belongs_rel) = nodes
        messages = generate_persona_prompt_messages({
            'topic': topic_node.topic,
            'username': user_node.username,
            'post': post_node.post_content
        })
        body = create_request_body(messages)
        batch_requests.append({
            "custom_id" : f"persona-{idx + 1}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": body,
        })
    return batch_requests

def file_response_to_jsonl(file_response):
    jsonl_objects = []
    for line in file_response.text.strip().splitlines():
        try:
            json_obj = json.loads(line)  # Parse the JSON object
            jsonl_objects.append(json_obj)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON line: {line}")
            print(e)
    return jsonl_objects

def save_as_jsonl(requests, file_path):
    with open(file_path, "w") as f:
        for req in requests:
            f.write(json.dumps(req) + '\n')
