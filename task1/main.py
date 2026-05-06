import os
import sys
import requests
import json
from dotenv import load_dotenv


load_dotenv()

def generate_text(prompt: str) -> str:
     """
    Sends a user prompt to an AI text generation API via OpenRouter
    and returns the generated response.
 
    Args:
        prompt: The user's input prompt
 
    Returns:
        The AI-generated text response
    """
     
     api_key = os.getenv("OPENROUTER_API_KEY")
     model_name = os.getenv("MODEL_NAME")

     if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set")

     if not model_name:
        raise ValueError("MODEL_NAME not set")

     url = "https://openrouter.ai/api/v1/chat/completions"

     headers = {
         "Authorization":f"Bearer {api_key}",
         "Content-Type": "application/json"
     }

     payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

     response = requests.post(url, headers=headers, json=payload)

     data = response.json()
    #  print(json.dumps(data, indent=2))
     return data["choices"][0]["message"]["content"]



def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<your prompt here>\"")
        sys.exit(1)


    prompt  = " ".join(sys.argv[1:])

    try:
        response = generate_text(prompt)
        print(response)
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.HTTPError as e:
        print(f"API request failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
     