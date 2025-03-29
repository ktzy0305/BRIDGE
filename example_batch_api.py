from db.schema import Post
from openai import OpenAI
from openai_batch_api_helper import file_response_to_jsonl, generate_batch_requests, save_as_jsonl
from schemas.persona import Persona

import time

help_seeker_posts = [node for node in Post.nodes.fetch_relations("written_by", "belongs_to").filter(post_order = 1)]
client = OpenAI()

# Example for Persona Identification
def convert_jsonl_to_persona(jsonl_objects):
    personas = []
    for request_obj in jsonl_objects:
        persona = Persona.model_validate_json(request_obj["response"]["body"]["choices"][0]["message"]["content"])
        personas.append(persona.model_dump())
    return personas

def wait_for_batch_completion(batch_id, timeout=600, poll_interval=10):
    """
    Wait for an OpenAI batch job to complete.
    Args:
        batch_id (str): ID of the OpenAI batch.
        timeout (int): Max time to wait in seconds.
        poll_interval (int): Interval between polls.
    Returns:
        The batch object when completed or failed.
    """
    start_time = time.time()
    while True:
        batch = client.batches.retrieve(batch_id)
        status = batch.status
        print(f"Batch status: {status}")
        
        if status in ["completed", "failed", "expired", "cancelled"]:
            return batch

        if time.time() - start_time > timeout:
            raise TimeoutError("Batch processing timed out.")

        time.sleep(poll_interval)

if __name__ == "__main__":
    # Step 1: Prepare and upload request file
    batch_requests = generate_batch_requests(help_seeker_posts)
    save_as_jsonl(batch_requests, "./data/openai_batch_requests/persona_requests.jsonl")
    
    with open("./data/openai_batch_requests/persona_requests.jsonl", "rb") as f:
        batch_input_file = client.files.create(file=f, purpose="batch")
    
    # Step 2: Submit batch request
    batch_input_file_id = batch_input_file.id
    batch_object = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": "Create personas batched"}
    )

    # Step 3: Wait until batch completes
    batch = wait_for_batch_completion(batch_object.id)
    
    # Step 4: Process output if completed
    if batch.status == "completed" and batch.output_file_id:
        file_response = client.files.content(batch.output_file_id)
        jsonl_objects = file_response_to_jsonl(file_response)
        personas = convert_jsonl_to_persona(jsonl_objects)
        save_as_jsonl(personas, "./data/openai_batch_responses/personas.jsonl")
    else:
        print(f"Batch status: {batch.status}, no output file yet.")