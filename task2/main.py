import sys
import os
import requests
from dotenv import load_dotenv

load_dotenv()


API_KEY=os.getenv("OPENROUTER_API_KEY")
MODEL_NAME=os.getenv("MODEL_NAME")


if not API_KEY:
    print("Error: OPENROUTER_API_KEY not set in .env file")
    sys.exit(1)

if not MODEL_NAME:
    print("Error: MODEL_NAME not set in .env file")
    sys.exit(1)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")



def load_prompt(filename:str) -> str:
    path= os.path.join(PROMPTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    

def call_llm(prompt:str) -> str:
    payload = {
        "model": MODEL_NAME,
         "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def run_chain(customer_query:str):
    separator = "=" * 60


    # Step 1: Interpret customer intent 

    print(f"\n{separator}")
    print("STEP 1: Interpreting customer intent...")
    print(separator)

    template1=load_prompt("prompt1_interpret_intent.txt")
    prompt1 = template1.replace("{customer_query}", customer_query)
    interpreted_intent= call_llm(prompt1)
    print(interpreted_intent)


     # Step 2:  Map query to possible categories

    print(f"\n{separator}")
    print("STEP 2: Mapping query to possible categories...")
    print(separator)

    template2=load_prompt("prompt2_map_categories.txt")
    prompt2 = template2.replace("{interpreted_intent}", interpreted_intent)
    possible_categories = call_llm(prompt2)
    print(possible_categories)


    # Step 3: Choose the most appropriate category

    print(f"\n{separator}")
    print("STEP 3: Choosing the most appropriate category...")
    print(separator)

    template3 = load_prompt("prompt3_choose_category.txt")
    prompt3 = (
        template3
        .replace("{customer_query}", customer_query)
        .replace("{interpreted_intent}", interpreted_intent)
        .replace("{possible_categories}", possible_categories)
    )
    chosen_category = call_llm(prompt3)
    print(chosen_category)

     # Step 4: Extract additional details

    print(f"\n{separator}")
    print("STEP 4: Extracting additional details...")
    print(separator)

    template4 = load_prompt("prompt4_extract_details.txt")
    prompt4= (
        template4
        .replace("{customer_query}", customer_query)
        .replace("{chosen_category}", chosen_category)
    )
    extracted_details = call_llm(prompt4)
    print(extracted_details)


     # Step 5: Generate customer response 

    print(f"\n{separator}")
    print("STEP 5: Generating final customer response...")
    print(separator)

    template5 = load_prompt("prompt5_generate_response.txt")
    prompt5 = (
        template5
        .replace("{customer_query}", customer_query)
        .replace("{chosen_category}", chosen_category)
        .replace("{extracted_details}", extracted_details)
    )

    final_response = call_llm(prompt5)
    print(final_response)


    # Final output 

    print(f"\n{separator}")
    print("FINAL RESPONSE TO CUSTOMER:")
    print(separator)
    print(final_response)
    print(separator)
 



 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<customer query>\"")
        sys.exit(1)
 
    query = sys.argv[1]
    print(f"\nProcessing customer query: \"{query}\"")
    run_chain(query)
