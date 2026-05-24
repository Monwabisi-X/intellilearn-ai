import json
from utils.ai_utils import simple_prompt


def generate_roadmap_structured(goal, weeks=4, hours_per_week=10, learning_path=None):
    """
    Generate a structured week-by-week roadmap.
    Returns list of week dicts: {theme, description, milestones: [...], project, resources: [...]}
    """
    path_context = ""
    if learning_path and learning_path.get("topics"):
        path_context = f"\nThe student's learning path is '{learning_path['name']}' covering: {', '.join(learning_path['topics'])}."

    prompt = f"""Create a {weeks}-week personalised study roadmap for the goal: "{goal}".
The student has approximately {hours_per_week} hours per week available.{path_context}

Return ONLY a valid JSON array of exactly {weeks} week objects. No markdown, no preamble.
Each week object must have:
- "theme": short week title (e.g. "Python Fundamentals")
- "description": 1-2 sentences about what the week covers
- "milestones": array of 4-6 specific, actionable tasks (strings)
- "project": a short mini-project description (1 sentence)
- "resources": array of 2-3 recommended resource types (e.g. "Official Python docs", "Kaggle micro-courses")

Example:
[
  {{
    "theme": "Week Theme",
    "description": "What this week covers.",
    "milestones": ["Task one", "Task two", "Task three"],
    "project": "Build a mini project",
    "resources": ["Resource 1", "Resource 2"]
  }}
]"""

    raw = simple_prompt(prompt, max_tokens=3000)

    # Strip markdown
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("```").strip()

    try:
        data = json.loads(raw)
        validated = []
        for w in data[:weeks]:
            validated.append({
                "theme": w.get("theme", f"Week {len(validated)+1}"),
                "description": w.get("description", ""),
                "milestones": w.get("milestones", [])[:6],
                "project": w.get("project", ""),
                "resources": w.get("resources", [])
            })
        return validated
    except (json.JSONDecodeError, KeyError):
        # Fallback: return minimal structure
        return [{"theme": f"Week {i+1}", "description": "Plan your study sessions.", "milestones": ["Study core concepts", "Complete exercises", "Review and revise"], "project": "Apply what you've learned", "resources": ["Official documentation", "YouTube tutorials"]} for i in range(weeks)]
