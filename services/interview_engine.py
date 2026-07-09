import json
from services.document_service import safe_json_parse

PROMPT_GEN_QUESTIONS = """You are a senior technical interviewer. Review this candidate's resume/profile details and generate exactly 4 interview questions:
1. Technical Question: Testing their core coding or analytical knowledge.
2. Behavioral Question: Testing collaboration, adaptability, or leadership.
3. Project-based Question: Asking about a specific project they listed.
4. Skill-based Question: Challenging them on a tool/technology mentioned.

Return ONLY a valid JSON dictionary in this exact format:
{{
  "technical": "<question>",
  "behavioral": "<question>",
  "project": "<question>",
  "skill": "<question>"
}}

CANDIDATE DETAILS:
{resume_data}
"""

PROMPT_EVAL_ANSWER = """You are a senior tech interviewer evaluating a candidate's response.
Evaluate this answer to the following question.

QUESTION: {question}
CANDIDATE'S ANSWER: {answer}

Provide feedback, scoring each of the following categories from 0 to 100:
- Technical Depth
- Communication
- Problem Solving
- Confidence
- Clarity

Return ONLY a valid JSON dictionary in this exact format:
{{
  "scores": {{
    "technical_depth": <int>,
    "communication": <int>,
    "problem_solving": <int>,
    "confidence": <int>,
    "clarity": <int>
  }},
  "feedback": "<2-3 sentence overall evaluation summary>",
  "suggestions": ["<suggestion1>", "<suggestion2>"]
}}
"""

def generate_interview_questions(resume_data: dict, llm) -> dict:
    """Generate structured questions based on candidate profile."""
    data_str = json.dumps(resume_data, indent=2)
    response = llm.invoke(PROMPT_GEN_QUESTIONS.format(resume_data=data_str))
    return safe_json_parse(response.content, {
        "technical": "Explain your approach to software architecture.",
        "behavioral": "Describe a time you solved a conflict within a team.",
        "project": "Walk me through one of your featured projects.",
        "skill": "How do you keep up-to-date with new technologies?"
    })

def evaluate_interview_answer(question: str, answer: str, llm) -> dict:
    """Evaluate candidate answer and score performance."""
    response = llm.invoke(PROMPT_EVAL_ANSWER.format(question=question, answer=answer))
    return safe_json_parse(response.content, {
        "scores": {
            "technical_depth": 50,
            "communication": 50,
            "problem_solving": 50,
            "confidence": 50,
            "clarity": 50
        },
        "feedback": "Could not parse evaluation details.",
        "suggestions": ["Elaborate further on technical components."]
    })
