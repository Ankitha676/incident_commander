import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # <-- THIS WAS MISSING

def ask_llm_summary(context: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "GROQ_API_KEY not set"

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an autonomous incident commander."},
            {"role": "user", "content": context}
        ]
    )

    return response.choices[0].message.content

