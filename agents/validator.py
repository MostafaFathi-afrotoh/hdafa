"""Deterministic Validator — Agent 3 of HDAFA pipeline.
Zero LLM involvement. Pure algorithmic checks."""

import re


# ---------- Structural checks (10) ----------
def structural_checks(code: str) -> dict:
    """10 deterministic structural checks."""
    c = code.lower() if code else ""
    checks = {
        "doctype":     "<!doctype" in c,
        "lang_ar":     'lang="ar"' in c,
        "rtl":         'dir="rtl"' in c,
        "has_style":   "<style" in c,
        "responsive":  "@media" in c or "grid" in c,
        "arabic":      bool(re.search(r"[\u0600-\u06FF]", code)) if code else False,
        "div_balance": c.count("<div") == c.count("</div>") and c.count("<div") > 0,
        "title":       "<title>" in c,
        "viewport":    "viewport" in c,
        "body":        "<body" in c and "</body>" in c,
    }
    passed = sum(checks.values())
    total = len(checks)
    return {
        "verdict": "PASS" if passed == total else "FAIL",
        "score": f"{passed}/{total}",
        "failed": [k for k, v in checks.items() if not v],
    }


# ---------- Section coverage ----------
SECTION_SYNONYMS = {
    "navbar":      ["nav", "header", "شريط", "تنقل", "ترويسة"],
    "hero":        ["hero", "banner", "واجهة", "رئيسي"],
    "products":    ["product", "item", "card", "منتج", "منتجات", "بطاقة"],
    "services":    ["service", "خدم", "خدمات"],
    "cart":        ["cart", "basket", "سلة", "عربة", "مشتريات"],
    "contact":     ["contact", "form", "تواصل", "اتصال", "نموذج"],
    "footer":      ["footer", "تذييل", "أسفل"],
    "about":       ["about", "story", "عن ", "قصت", "من نحن"],
    "menu":        ["menu", "قائمة", "أطباق"],
    "reservation": ["reserv", "booking", "حجز", "احجز", "موعد"],
    "filter":      ["filter", "sort", "فلترة", "تصفية"],
    "gallery":     ["gallery", "معرض", "صور", "أعمال"],
    "portfolio":   ["portfolio", "أعمال", "مشاريع", "معرض"],
    "team":        ["team", "فريق", "أطباء"],
    "pricing":     ["pricing", "أسعار", "خطط", "باقات"],
    "features":    ["feature", "مميزات", "خصائص", "ميزات"],
}


def _find_keywords(section_id: str, section_name: str) -> list:
    keywords = []
    sid = section_id.lower().replace("_section", "").replace("_", " ").strip()
    sname = (section_name or "").strip()
    for concept, syns in SECTION_SYNONYMS.items():
        if concept in sid or concept in sname.lower():
            keywords.extend(syns)
    for w in sid.split():
        if len(w) > 3:
            keywords.append(w)
    if sname:
        keywords.append(sname)
        for w in sname.split():
            if len(w) > 2:
                keywords.append(w)
    return list(set(keywords))


def section_coverage(code: str, schema: dict) -> dict:
    """% of schema-defined sections present in generated HTML."""
    if not schema or not code:
        return {"found": 0, "total": 0, "percent": 0.0}
    c = code.lower()
    sections = schema.get("sections", [])
    if not sections:
        return {"found": 0, "total": 0, "percent": 0.0}
    found = 0
    for sec in sections:
        sid = sec.get("id", "").lower()
        sname = sec.get("name", "")
        keywords = _find_keywords(sid, sname)
        if not keywords:
            found += 1
            continue
        if any(kw.lower() in c for kw in keywords):
            found += 1
    return {
        "found": found,
        "total": len(sections),
        "percent": round(found / len(sections) * 100, 1),
    }
