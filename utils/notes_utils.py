from utils.ai_utils import simple_prompt


def generate_notes(text, format_choice="Structured bullet points", learning_path=None):
    """Generate study notes from pasted content."""

    path_context = ""
    if learning_path:
        path_context = f"\nThe student is studying: {learning_path['name']}. Tailor examples accordingly."

    format_instructions = {
        "Structured bullet points": "Create structured bullet-point notes with clear headings, key concepts highlighted, and sub-bullets for details.",
        "Summary + Key Concepts": "Write a 2-3 paragraph summary, then list the top 10 key concepts with brief definitions.",
        "Flashcard-style Q&A": "Create 10-15 flashcard-style question-and-answer pairs that test the most important ideas.",
        "Mind map outline": "Create a hierarchical mind-map outline with a central topic, main branches, and sub-branches. Use indentation to show hierarchy."
    }

    instructions = format_instructions.get(format_choice, format_instructions["Structured bullet points"])

    prompt = f"""You are an expert study notes generator.{path_context}

{instructions}

Focus on:
- The most important concepts
- Definitions of key terms
- Relationships between ideas
- Anything likely to appear in an exam

Content to process:
---
{text[:4000]}
---

Generate the study notes now in clean Markdown format:"""

    return simple_prompt(prompt, max_tokens=1500)
