from typing import Any, Dict, List

import json

def load_from_json(file_path: str) -> List[Dict[str, Any]]:
    json_data = []

    with open(file_path, 'r') as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            json_data = []
    return json_data

def save_to_json(json_data: List[Dict[str, Any]], file_path: str):
    with open(file_path, 'w') as f:
        json.dump(json_data, f, indent=4)