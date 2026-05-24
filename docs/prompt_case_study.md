# Prompt Engineering Case Study — IntelliLearn AI

**Project:** IntelliLearn AI  
**Author:** CAPACITI AI Bootcamp Candidate  
**Week:** 4 — AI Solution Development

---

## Overview

This case study documents the prompt engineering strategies used across IntelliLearn AI's four AI-powered features. It demonstrates how prompt design directly shapes output quality, format reliability, and educational effectiveness.

---

## Case Study 1: Structured Quiz Generation

### Challenge
The quiz feature requires AI output in a strict, machine-readable format (JSON array). Raw LLM output is often conversational and surrounded by markdown fences, making it unreliable for direct parsing.

### Prompt Design (v1 — naive)
```
Generate 5 multiple-choice quiz questions about neural networks.
Include question, 4 options, and correct answer.
```
**Problem:** Returned free-form text. Inconsistent formatting. Options sometimes numbered, sometimes lettered. Correct answer embedded in narrative prose.

### Prompt Design (v2 — structured JSON)
```
Generate exactly 5 multiple-choice quiz questions about "neural networks" at Intermediate level.

Return ONLY a valid JSON array. No preamble, no markdown, no explanation outside the JSON.
Each element must have:
- "question": string
- "options": array of exactly 4 strings, each starting with "A. ", "B. ", "C. ", or "D. "
- "answer": single letter "A", "B", "C", or "D"
- "explanation": brief explanation (1-2 sentences) of why the answer is correct
```
**Result:** Reliable JSON output. Parseable 95%+ of the time. Fallback handling catches the remainder.

### Key Techniques
- **Negative constraints:** "No preamble, no markdown" reduces decorative wrapping
- **Exact format example:** Showing the expected JSON structure in the prompt itself acts as a template
- **Literal counts:** "exactly 5", "exactly 4 strings" reduces variance
- **Low temperature (0.3):** Reduces creative deviation for structured outputs

---

## Case Study 2: Educational AI Tutor System Prompt

### Challenge
Without a system prompt, the LLM gives generic answers. With a learning path injected, responses become contextually relevant to the student's current focus area.

### System Prompt (base)
```
You are IntelliLearn AI, a friendly and clear educational tutor. 
Always explain with: 
1) a simple explanation, 
2) a concrete example, 
3) a real-world analogy. 
Keep responses concise but thorough.
```

### System Prompt (with learning path injection)
```
You are IntelliLearn AI, a friendly and clear educational tutor. 
Always explain with: 1) a simple explanation, 2) a concrete example, 3) a real-world analogy. 
Keep responses concise but thorough.
The student is focused on: Python for Data Science — Master Python fundamentals, 
data manipulation with pandas, and visualisation.
```

### Comparison

| Prompt | Response to "What is a function?" |
|---|---|
| No system prompt | Generic CS definition |
| With learning path | Explains functions with a pandas `apply()` example, mentions reusability in data pipelines |

### Key Techniques
- **Persona definition:** "You are IntelliLearn AI" grounds the model's behaviour
- **Output structure mandate:** 3-part explanation ensures consistency
- **Dynamic context injection:** Learning path description appended programmatically
- **Conversation history:** Last 10 messages sent to maintain coherent multi-turn dialogue

---

## Case Study 3: Study Roadmap Generation

### Challenge
Roadmaps need to be week-structured, actionable, and appropriate for the student's time availability. Early attempts produced walls of text with no parseable structure.

### Prompt Iteration

**v1:** "Create a 4-week learning plan for machine learning."  
→ Returned a single paragraph. No structure.

**v2:** Added "Format as week-by-week, with bullet points."  
→ Better, but inconsistent. Some weeks had 2 bullets, others 10.

**v3 — Final JSON approach:**
```
Create a 4-week personalised study roadmap for the goal: "Learn machine learning".
The student has approximately 10 hours per week available.
The student's learning path is 'Machine Learning Foundations' covering: 
Regression, Classification, Clustering, Model evaluation, Feature engineering.

Return ONLY a valid JSON array of exactly 4 week objects...
[full JSON schema provided]
```
→ Consistent, structured output. Each week has exactly the required fields.

### Key Techniques
- **Constraint chaining:** Goal + time + learning path combine to narrow output scope
- **Schema-in-prompt:** Providing the exact JSON structure as an example
- **Fallback generation:** Code-level fallback produces generic but functional weeks if parsing fails

---

## Case Study 4: Notes Generation with Format Control

### Challenge
Students need notes in different formats for different study styles. A single prompt cannot serve all formats well.

### Approach: Format-Specific Instruction Injection

Four distinct instruction blocks are defined in code:

```python
format_instructions = {
    "Structured bullet points": "Create structured bullet-point notes with clear headings...",
    "Summary + Key Concepts": "Write a 2-3 paragraph summary, then list the top 10 key concepts...",
    "Flashcard-style Q&A": "Create 10-15 flashcard-style question-and-answer pairs...",
    "Mind map outline": "Create a hierarchical mind-map outline with indentation..."
}
```

The selected instruction is injected into the prompt dynamically, so the model receives a precise instruction for the exact format needed.

### Result
Each format produces distinctly different, appropriate output. Students can re-generate the same content in multiple formats without re-pasting.

---

## Summary: Prompt Engineering Lessons

| Lesson | Application |
|---|---|
| Use JSON schemas in prompts for structured output | Quiz Generator, Roadmap Generator |
| System prompts define persona + consistent behaviour | AI Tutor |
| Inject context dynamically (don't hardcode) | Learning path in Tutor, Notes, Roadmap |
| Use low temperature for structured tasks, higher for creative | quiz_utils: 0.3, tutor: 0.7 |
| Always add fallback parsing | Quiz and Roadmap handle malformed JSON gracefully |
| Negative constraints reduce noise | "No preamble, no markdown" in JSON prompts |
| Multi-turn context improves coherence | Last 10 messages sent in Tutor conversations |
