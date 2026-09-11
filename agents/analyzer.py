"""Requirements Analyzer — Agent 1 of HDAFA pipeline."""
import json


ANALYZER_SYSTEM_PROMPT = """You are "Requirements Analyzer" — an atomic agent specialized in web requirements analysis.
Your task: convert a project description into a structured JSON schema.
Rules:
- Output pure JSON only, no explanations.
- Define 4-6 precise sections.
- Each section must have: id, name, components, purpose."""

ANALYZER_USER_TEMPLATE = """Input: project description
Output JSON:
{{
  "page_id": "...",
  "page_title": "...",
  "sections": [
    {{"id": "...", "name": "...", "components": ["..."], "purpose": "..."}}
  ],
  "constraints": {{"rtl": true, "responsive": true, "language": "ar", "max_lines": 1000}}
}}

Task: {task}
Output JSON only."""


def safe_json_parse(raw: str):
    """Extract and parse the first JSON object from raw text."""
    if not raw:
        return None
    try:
        s, e = raw.find("{"), raw.rfind("}") + 1
        return json.loads(raw[s:e])
    except Exception:
        return None


def analyze(task: str, call_llm) -> dict | None:
    """
    Run the Analyzer agent.
    `call_llm` is a function(system, user, max_tokens) -> str.
    """
    prompt = ANALYZER_USER_TEMPLATE.format(task=task)
    raw = call_llm(ANALYZER_SYSTEM_PROMPT, prompt, 2000)
    return safe_json_parse(raw)
