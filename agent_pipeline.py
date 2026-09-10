
# ============================================================
# HDAFA — Hyper-Deterministic Atomic Agentic Architecture
# A 3-agent system: Analyzer → Coder → Validator
# ============================================================
import os, re, json, time
from google.colab import userdata
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = userdata.get('GEMINI_API_KEY')
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
MODEL = genai.GenerativeModel("gemini-3.5-flash-lite")

def call_model(system, user, max_tokens=8000):
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
  raise Exception("failed")

# ---- Agent 1: Analyzer ----
P1 = """أنت "Requirements Analyzer". مهمتك: تحويل وصف إلى JSON.
قواعد: أخرج JSON نقي فقط، 4-6 أقسام دقيقة."""

T1 = """المدخل: وصف مشروع
المخرج: JSON:
{
"page_id": "...",
"page_title": "...",
"sections": [{"id": "...", "name": "...", "components": ["..."], "purpose": "..."}],
"constraints": {"rtl": true, "responsive": true, "language": "ar", "max_lines": 1000}
}

المهمة: {task}
أخرج JSON فقط."""

def agent_1(task):
  prompt = T1.replace("{task}", task)
  raw = call_model(P1, prompt, 3000)
  s, e = raw.find("{"), raw.rfind("}") + 1
  return json.loads(raw[s:e])

# ---- Agent 2: Coder ----
P2 = """أنت "HTML/CSS Coder". مهمتك: تحويل JSON إلى HTML.
قواعد: كود داخل ```html```، DOCTYPE، dir="rtl"، @media، ألوان دافئة، عربي حقيقي."""

def agent_2(schema):
  user = f"المدخل:\n{json.dumps(schema, ensure_ascii=False)}\n\nأخرج الكود فقط."
  raw = call_model(P2, user, 8000)
  if "```html" in raw:
      s = raw.find("```html") + 7
      e = raw.find("```", s)
      return raw[s:e].strip()
  return raw

# ---- Agent 3: Validator ----
def agent_3(code, schema):
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

def run_pipeline(task):
  schema = agent_1(task)
  html = agent_2(schema)
  report = agent_3(html, schema)
  return {"schema": schema, "html": html, "report": report}

if __name__ == "__main__":
  task = "صمم صفحة بن كاملة مع شريط تنقل، منتجات، سلة، وتواصل"
  result = run_pipeline(task)
  print(result["report"])
