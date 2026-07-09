import json
from services.document_service import safe_json_parse

PROMPT_CAREER = """You are a senior career advisor and MLOps specialist. Analyze the following candidate's resume/details to evaluate market readiness.

Return ONLY a valid JSON dictionary in this exact format:
{{
  "market_readiness_score": <int 0-100>,
  "job_matches": [
    {{"role": "<role name>", "score": <int 0-100>}}
  ],
  "skill_gaps": ["<gap1>", "<gap2>", "<gap3>"],
  "learning_roadmap": [
    {{"duration": "Month 1", "topic": "<topic>", "details": "<learning activities>"}},
    {{"duration": "Month 2", "topic": "<topic>", "details": "<learning activities>"}},
    {{"duration": "Month 3", "topic": "<topic>", "details": "<learning activities>"}}
  ],
  "strengths": ["<strength1>", "<strength2>"],
  "weaknesses": ["<weakness1>", "<weakness2>"]
}}

CANDIDATE DETAILS:
{resume_data}
"""

def generate_career_insights(resume_data: dict, llm) -> dict:
    """Generate career matches, skill gaps, and learning roadmaps."""
    data_str = json.dumps(resume_data, indent=2)
    response = llm.invoke(PROMPT_CAREER.format(resume_data=data_str))
    return safe_json_parse(response.content, {
        "market_readiness_score": 70,
        "job_matches": [
            {"role": "AI Engineer", "score": 80},
            {"role": "Software Developer", "score": 85}
        ],
        "skill_gaps": ["Docker", "Kubernetes", "MLOps"],
        "learning_roadmap": [
            {"duration": "Month 1", "topic": "Docker & Containerization", "details": "Containerize python microservices."},
            {"duration": "Month 2", "topic": "AWS & Cloud Deployments", "details": "Deploy apps to ECS/EKS."},
            {"duration": "Month 3", "topic": "MLOps Pipelines", "details": "Build training & orchestration pipelines."}
        ],
        "strengths": ["Core Python programming skills", "Project execution"],
        "weaknesses": ["Lack of deployment experience", "No cloud engineering records"]
    })
