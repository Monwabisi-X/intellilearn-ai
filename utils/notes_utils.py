from utils.ai_utils import generate_ai_response


def generate_notes(text):

    prompt = f"""
    Summarize the following into study notes:

    {text}

    Format:
    - bullet points
    - key concepts
    - concise explanations
    """

    return generate_ai_response(prompt)