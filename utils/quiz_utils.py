import json
from utils.ai_utils import simple_prompt


def generate_quiz_structured(topic, num_questions=5, difficulty="Intermediate"):
    """
    Generate structured quiz questions as a list of dicts.
    Each dict: {question, options: [A.., B.., C.., D..], answer: "A"|"B"|"C"|"D", explanation}
    """
    prompt = f"""Generate exactly {num_questions} multiple-choice quiz questions about "{topic}" at {difficulty} level.

Return ONLY a valid JSON array. No preamble, no markdown, no explanation outside the JSON.
Each element must have:
- "question": string
- "options": array of exactly 4 strings, each starting with "A. ", "B. ", "C. ", or "D. "
- "answer": single letter "A", "B", "C", or "D"
- "explanation": brief explanation (1-2 sentences) of why the answer is correct

Example format:
[
  {{
    "question": "What is X?",
    "options": ["A. First option", "B. Second option", "C. Third option", "D. Fourth option"],
    "answer": "B",
    "explanation": "Because Y is the reason..."
  }}
]

Topic: {topic}
Difficulty: {difficulty}
Number of questions: {num_questions}"""

    raw = simple_prompt(prompt, max_tokens=2000)

    # Strip markdown fences if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("```").strip()

    try:
        data = json.loads(raw)
        # Validate structure
        validated = []
        for item in data:
            if all(k in item for k in ["question", "options", "answer"]):
                validated.append({
                    "question": item["question"],
                    "options": item["options"][:4],
                    "answer": item.get("answer", "A"),
                    "explanation": item.get("explanation", "")
                })
        return validated
    except (json.JSONDecodeError, KeyError, TypeError):
        # Fallback: return empty so UI shows error gracefully
        return []
