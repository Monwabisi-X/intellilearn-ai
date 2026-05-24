import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"


def generate_ai_response(messages, system=None):
    """
    messages: list of {"role": "user"|"assistant", "content": str}
    system: optional system prompt string
    """
    api_messages = []
    if system:
        api_messages.append({"role": "system", "content": system})
    api_messages.extend(messages)

    completion = client.chat.completions.create(
        model=MODEL,
        messages=api_messages,
        temperature=0.7,
        max_tokens=1024
    )
    return completion.choices[0].message.content


def stream_ai_response(messages, system=None):
    """Generator that yields streamed response chunks."""
    api_messages = []
    if system:
        api_messages.append({"role": "system", "content": system})
    api_messages.extend(messages)

    stream = client.chat.completions.create(
        model=MODEL,
        messages=api_messages,
        temperature=0.7,
        max_tokens=1024,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def simple_prompt(prompt_text, max_tokens=2048):
    """Simple single-turn prompt for internal use."""
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt_text}],
        temperature=0.3,
        max_tokens=max_tokens
    )
    return completion.choices[0].message.content
