import re
from dataclasses import dataclass
from typing import Any


@dataclass
class ATSResult:
    score: float                    # 0–100
    keyword_coverage: float         # % of JD keywords found in resume
    matched_keywords: list[str]
    missing_keywords: list[str]
    formatting_score: float
    length_ok: bool
    recommendations: list[str]


def _extract_keywords(text: str) -> set[str]:
    text = text.lower()
    # Remove punctuation, split to words
    words = re.findall(r'\b[a-z][a-z0-9+#.\-]{1,30}\b', text)
    # Common stopwords
    stopwords = {
        "and", "the", "for", "with", "our", "you", "your", "will", "have",
        "this", "that", "are", "not", "from", "work", "team", "role",
        "strong", "good", "great", "able", "experience", "skills", "using",
        "may", "can", "use", "etc", "also", "must", "should", "would",
    }
    return {w for w in words if w not in stopwords and len(w) > 2}


def _extract_tech_phrases(text: str) -> set[str]:
    """Extract multi-word technical phrases that ATS systems look for."""
    patterns = [
        r'apache\s+spark', r'azure\s+data\s+factory', r'azure\s+synapse',
        r'azure\s+databricks', r'amazon\s+s3', r'amazon\s+redshift',
        r'google\s+bigquery', r'big\s+query', r'apache\s+kafka',
        r'apache\s+airflow', r'dbt\s+core', r'delta\s+lake',
        r'data\s+lakehouse', r'data\s+warehouse', r'data\s+lake',
        r'data\s+pipeline', r'etl\s+pipeline', r'elt\s+pipeline',
        r'real.time\s+streaming', r'batch\s+processing',
        r'machine\s+learning', r'deep\s+learning', r'power\s+bi',
        r'microsoft\s+fabric', r'unity\s+catalog', r'medallion\s+architecture',
        r'star\s+schema', r'snowflake\s+schema', r'ci.?cd',
        r'infrastructure\s+as\s+code',
    ]
    text_lower = text.lower()
    found = set()
    for pattern in patterns:
        if re.search(pattern, text_lower):
            found.add(re.sub(r'\s+', ' ', re.sub(r'[.?]', ' ', pattern)).strip())
    return found


def score_ats(
    resume_text: str,
    job_description: str,
    resume_content: dict[str, Any] | None = None,
) -> ATSResult:
    jd_keywords = _extract_keywords(job_description)
    jd_phrases = _extract_tech_phrases(job_description)
    resume_keywords = _extract_keywords(resume_text)
    resume_phrases = _extract_tech_phrases(resume_text)

    all_jd_terms = jd_keywords | jd_phrases
    all_resume_terms = resume_keywords | resume_phrases

    matched = all_jd_terms & all_resume_terms
    missing = all_jd_terms - all_resume_terms

    # Keyword coverage score
    keyword_coverage = (len(matched) / len(all_jd_terms) * 100) if all_jd_terms else 0.0

    # Formatting score (basic heuristics)
    formatting_score = 100.0
    recommendations = []

    word_count = len(resume_text.split())
    length_ok = 300 <= word_count <= 800
    if word_count < 300:
        formatting_score -= 15
        recommendations.append("Resume is too short — add more detail to experience sections.")
    elif word_count > 800:
        formatting_score -= 10
        recommendations.append("Resume exceeds 2-page target — trim less relevant sections.")

    if not re.search(r'(linkedin\.com|github\.com)', resume_text, re.IGNORECASE):
        formatting_score -= 5
        recommendations.append("Add LinkedIn and GitHub profile URLs.")

    if not re.search(r'\b\d{4}\b', resume_text):
        formatting_score -= 10
        recommendations.append("Include date ranges for all experience entries.")

    # Top missing keywords to surface
    top_missing = sorted(missing)[:15]
    if top_missing:
        recommendations.append(f"Consider adding: {', '.join(top_missing[:8])}")

    # Composite score: 70% keyword coverage + 30% formatting
    score = (keyword_coverage * 0.70) + (formatting_score * 0.30)
    score = max(0.0, min(100.0, score))

    return ATSResult(
        score=round(score, 1),
        keyword_coverage=round(keyword_coverage, 1),
        matched_keywords=sorted(matched)[:30],
        missing_keywords=top_missing,
        formatting_score=round(formatting_score, 1),
        length_ok=length_ok,
        recommendations=recommendations,
    )
