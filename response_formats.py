persona_response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "persona_response",
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age_range": {"type": "string"},
                "gender": {"type": "string"},
                "background": {"type": "string"},
                "mental_health_symptoms": {"type": "string"},
                "perspective": {"type": "string"},
                "motivations": {"type": "string"},
                "emotional_state": {"type": "string"},
                "needs": {"type": "string"},
                "conversational_stance": {"type": "string"},
                "type": {
                    "type": "string",
                    "enum": ["Identified", "Diversified"]
                }
            },
            "required": [
                "name",
                "age_range",
                "gender",
                "background",
                "mental_health_symptoms",
                "perspective",
                "motivations",
                "emotional_state",
                "needs",
                "conversational_stance",
                "type"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}