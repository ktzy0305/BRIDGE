from typing import Any, Dict, List

def create_linear_thread_string(data: List[Dict[str, Any]]) -> str:
    output = ""
    for idx, row in enumerate(data):
        if idx == 0:
            # Add the topic
            output += f"Topic: {row['topic']}\n"
            output += f"Subcategory: {row['subcategory']}\n\n"
            
        output += f"Post Number: {idx + 1}\n"   
        output += f"Username: {row['username'] + (' (Help Seeker)' if row['username'] == data[0]['username'] else ' (Professional)' if row['user_role'] == 'Professional' else ' (User)')}\n"
        output += f"Post ID: {row['post_id']}\n{row['post_content']}\n\n"
    
    return output