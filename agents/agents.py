"""HTML/CSS Coder — Agent 2 of HDAFA pipeline."""
import json
import re


CODER_SYSTEM_PROMPT = """You are "HTML/CSS Coder" — an atomic agent specialized in writing HTML pages.
Your task: convert a JSON schema into complete HTML.

Rules:
- Output code only, inside ```html``` code fences.
- Must include <!DOCTYPE html>.
- Must include <html lang="ar" dir="rtl">.
- Must include viewport meta tag.
- Must use @media or grid/flex for responsiveness.
- Must use warm, professional colors.
- Must use real Arabic text (no Lorem Ipsum).
- No JavaScript.
- Include ALL sections listed in the schema."""


def extract_html(raw: str) -> str:
    """Extract HTML content from ```html``` block, or return raw."""
    if not raw:
        return ""
    if "```html" in raw:
        s = raw.find("```html") + 7
        e = raw.find("```", s)
        return raw[s:e].strip()
    if "```" in raw:
        s = raw.find("```") + 3
        e = raw.find("```", s)
        return raw[s:e].strip()
    return raw


def _dynamic_max_tokens(schema: dict, base: int = 2000,
                        per_section: int = 800, cap: int = 8192) -> int:
    """Scale max_tokens with number of sections to avoid truncation."""
    n = len(schema.get("sections", [])) if schema else 4
    return min(per_section * n + base, cap)


def code(schema: dict, call_llm) -> str:
    """Run the Coder agent with dynamic token budget."""
    user = f"Input:\n{json.dumps(schema, ensure_ascii=False)}\n\nOutput code only."
    max_tokens = _dynamic_max_tokens(schema)
    raw = call_llm(CODER_SYSTEM_PROMPT, user, max_tokens)
    return extract_html(raw)
