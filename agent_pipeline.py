# ============================================================
# HDAFA — Hyper-Deterministic Atomic Agentic Architecture
# A 3-agent pipeline: Analyzer → Coder → Validator
# ============================================================
import os, re, json, time
from google.colab import userdata
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = userdata.get('GEMINI_API_KEY')
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
MODEL = genai.GenerativeModel("gemini-3.5-flash-lite")


def call_model(system: str, user: str, max_tokens: int = 8000) -> str:
    """Call Gemini with retry logic."""
    for attempt in range(3):
        try:
            r = MODEL.generate_content(
                f"{system}\n\n{user}",
                generation_config={"temperature": 0.0, "max_output_tokens": max_tokens}
            )
            return r.text.strip()
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                time.sleep(15 * (attempt + 1))
            else:
                raise
    raise Exception("Failed after 3 attempts")


# ---------- Agent 1: Requirements Analyzer ----------
P1 = """You are "Requirements Analyzer" — an atomic agent specialized in web requirements analysis.
Your task: convert a project description into a structured JSON schema.
Rules: output pure JSON only. Define 4-6 precise sections."""

T1 = """Input: project description
Output: JSON:
{
  "page_id": "...",
  "page_title": "...",
  "sections": [{"id": "...", "name": "...", "components": ["..."], "purpose": "..."}],
  "constraints": {"rtl": true, "responsive": true, "language": "ar", "max_lines": 1000}
}

Task: {task}
Output JSON only."""


def agent_1(task: str) -> dict:
    prompt = T1.replace("{task}", task)
    raw = call_model(P1, prompt, 3000)
    s, e = raw.find("{"), raw.rfind("}") + 1
    return json.loads(raw[s:e])


# ---------- Agent 2: HTML/CSS Coder ----------
P2 = """You are "HTML/CSS Coder" — an atomic agent specialized in writing HTML pages.
Your task: convert a JSON schema into complete HTML.
Rules: code inside ```html```, DOCTYPE, dir="rtl", @media, warm colors, real Arabic text."""


def agent_2(schema: dict) -> str:
    user = f"Input:\n{json.dumps(schema, ensure_ascii=False)}\n\nOutput code only."
    raw = call_model(P2, user, 8000)
    if "```html" in raw:
        s = raw.find("```html") + 7
        e = raw.find("```", s)
        return raw[s:e].strip()
    return raw


# ---------- Agent 3: Deterministic Validator ----------
def agent_3(code: str, schema: dict) -> dict:
    """15 deterministic checks — no AI involved."""
    c = code.lower()
    checks = {
        "doctype": "<!doctype" in c,
        "lang_ar": 'lang="ar"' in c,
        "rtl": 'dir="rtl"' in c,
        "has_style": "<style" in c,
        "responsive": "@media" in c or "grid" in c,
        "navbar": "nav" in c,
        "hero": "hero" in c or "رئيسي" in code,
        "products": "product" in c or "منتج" in code,
        "cart": "cart" in c or "سلة" in code,
        "contact": "form" in c and "input" in c,
        "arabic": bool(re.search(r"[\u0600-\u06FF]", code)),
        "div_balance": c.count("<div") == c.count("</div>"),
        "line_count": len([l for l in code.split("\n") if l.strip()]) <= schema.get("constraints", {}).get("max_lines", 1000),
        "title": "<title>" in c,
        "viewport": "viewport" in c,
    }
    passed = sum(checks.values())
    return {
        "verdict": "PASS" if passed == 15 else "FAIL",
        "score": f"{passed}/15",
        "checks": checks,
        "failed": [k for k, v in checks.items() if not v],
    }


def run_pipeline(task: str) -> dict:
    """Execute the full pipeline."""
    schema = agent_1(task)
    html = agent_2(schema)
    report = agent_3(html, schema)
    return {"schema": schema, "html": html, "report": report}


if __name__ == "__main__":
    task = "Design a complete coffee shop page with navbar, products, cart, and contact section"
    result = run_pipeline(task)
    print(json.dumps(result["report"], ensure_ascii=False, indent=2))