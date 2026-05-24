from utils.ai_utils import generate_ai_response


def generate_roadmap(goal):

    prompt = f"""
    Create a personalized learning roadmap for:

    {goal}

    Include:
    - weekly milestones
    - recommended topics
    - practical projects
    - revision strategy
    """

    return generate_ai_response(prompt)