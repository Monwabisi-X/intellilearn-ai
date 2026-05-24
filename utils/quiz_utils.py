from utils.ai_utils import generate_ai_response


def generate_quiz(topic):

    prompt = f"""
    Generate 5 multiple-choice quiz questions about {topic}.

    Include:
    - Question
    - 4 options
    - Correct answer
    """

    return generate_ai_response(prompt)