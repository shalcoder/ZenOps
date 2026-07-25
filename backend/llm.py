import os
import json
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

# Example models: 'openai/gpt-4o', 'gemini/gemini-1.5-pro'
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gemini/gemini-1.5-pro")

def call_llm(messages: list, response_format=None, model: str = None) -> str:
    """
    Calls the LLM via litellm.
    messages: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    response_format: If passing a pydantic schema, you can set response_format={"type": "json_object"}
    """
    selected_model = model or DEFAULT_MODEL
    
    try:
        response = completion(
            model=selected_model,
            messages=messages,
            response_format=response_format
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM Call failed: {e}")
        # Return empty JSON string if we expect json_object, else return error message
        if response_format and response_format.get("type") == "json_object":
            return "{}"
        return f"Error: {str(e)}"
