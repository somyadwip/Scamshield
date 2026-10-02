"""Input normalization and type detection utilities."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from models.schemas import DetectedType, InputCategory


# ── Keywords for auto-detection ─────────────────────────────────────────────────

_JOB_KEYWORDS = [
    "job", "hiring", "recruit", "vacancy", "career", "position",
    "employment", "work from home", "from home", "wfh", "apply now", "openings",
    "salary", "internship", "placement", "per month", "per day", "lpa",
    "no experience", "registration fee", "joining fee", "earn", "daily income",
    "software engineer", "developer", "typist", "data entry", "remote work",
]

_SUSPICIOUS_OFFER_KEYWORDS = [
    "registration fee", "joining fee", "guaranteed income", "guaranteed salary",
    "guaranteed profit", "guaranteed returns", "pay before", "pay to start",
    "no experience required", "double your money", "risk-free returns",
    "send money first", "pay ₹", "pay $", "refundable deposit",
]

_INVESTMENT_KEYWORDS = [
    "invest", "trading", "forex", "crypto", "bitcoin", "returns",
    "profit", "dividend", "scheme", "mlm", "pyramid", "ponzi",
    "guaranteed returns", "passive income", "doubling",
]

_SHOPPING_KEYWORDS = [
    "shop", "buy", "store", "deal", "discount", "sale", "order",
    "cart", "checkout", "price", "offer", "coupon", "ecommerce",
    "e-commerce", "marketplace",
]

_COURSE_KEYWORDS = [
    "course", "training", "certification", "bootcamp", "class",
    "program", "workshop", "tutorial", "academy", "institute",
    "placement guarantee", "learn", "coaching",
]


def _looks_like_url(text: str) -> bool:
    """Heuristic check for URL-like input."""
    if text.startswith(("http://", "https://", "www.")):
        return True
    # patterns like example.com, example.co.in etc.
    if re.match(r"^[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}", text):
        return True
    try:
        parsed = urlparse(text)
        return bool(parsed.scheme and parsed.netloc)
    except Exception:
        return False


def _has_keywords(text: str, keywords: list[str]) -> int:
    """Return count of keywords found (case-insensitive)."""
    lower = text.lower()
    return sum(1 for kw in keywords if kw in lower)


def detect_input_type(raw_input: str, category: InputCategory) -> DetectedType:
    """Detect the type of input. If a manual category is given (non-auto), use it."""
    if category != InputCategory.AUTO:
        mapping = {
            InputCategory.WEBSITE: DetectedType.URL,
            InputCategory.COMPANY: DetectedType.COMPANY,
            InputCategory.JOB_OFFER: DetectedType.JOB_OFFER,
            InputCategory.SHOPPING: DetectedType.SHOPPING,
            InputCategory.INVESTMENT: DetectedType.INVESTMENT,
            InputCategory.COURSE: DetectedType.COURSE,
            InputCategory.OTHER: DetectedType.GENERAL,
        }
        return mapping.get(category, DetectedType.GENERAL)

    text = raw_input.strip()
    lower = text.lower()
    words = text.split()

    # 1. URL?
    if _looks_like_url(text):
        return DetectedType.URL

    # 2. Suspicious offer markers take precedence for multi-phrase claims
    if any(k in lower for k in _SUSPICIOUS_OFFER_KEYWORDS):
        if any(j in lower for j in ("job", "work", "home", "earn", "salary", "hiring", "recruit", "typing", "entry")):
            return DetectedType.JOB_OFFER
        return DetectedType.SUSPICIOUS_OFFER

    # 3. Active job offer patterns (sentences, salary, recruitment calls, role descriptions)
    _active_job_offer_signals = (
        "apply", "hiring", "hire", "vacancy", "vacancies", "salary", "lpa",
        "per month", "per day", "join our", "work from home", "wfh",
        "remote work", "no experience", "immediate joining", "internship",
        "software engineer", "developer", "data entry", "typist",
    )
    has_active_job_signal = any(sig in lower for sig in _active_job_offer_signals)
    has_sentence_structure = "." in text or "!" in text or len(words) > 6

    if has_active_job_signal and (has_sentence_structure or any(w in lower for w in ("apply", "hiring", "salary", "lpa", "join"))):
        return DetectedType.JOB_OFFER

    # 4. Keyword scoring for other categories
    scores = {
        DetectedType.INVESTMENT: _has_keywords(text, _INVESTMENT_KEYWORDS),
        DetectedType.SHOPPING: _has_keywords(text, _SHOPPING_KEYWORDS),
        DetectedType.COURSE: _has_keywords(text, _COURSE_KEYWORDS),
    }

    best = max(scores, key=scores.get)  # type: ignore[arg-type]
    if scores[best] >= 1:
        return best

    # 5. Long sentences or multi-clause messages should NOT be classified as companies
    if len(words) > 6 or "." in text or "!" in text or "?" in text or any(v in lower for v in ("earn", "pay", "join", "apply")):
        return DetectedType.GENERAL

    # 6. Default for short input (company, brand, or entity name, e.g. 'Microsoft', 'XYZ Super Mega Careers 928374')
    return DetectedType.COMPANY


def normalize_input(raw_input: str) -> str:
    """Clean up user input for search queries."""
    text = raw_input.strip()
    # Remove leading protocol noise for display
    text = re.sub(r"^https?://", "", text)
    text = re.sub(r"^www\.", "", text)
    # Remove trailing slashes
    text = text.rstrip("/")
    return text


def extract_domain(raw_input: str) -> str | None:
    """Extract domain from a URL-like input."""
    text = raw_input.strip()
    if not text.startswith(("http://", "https://")):
        text = "https://" + text
    try:
        parsed = urlparse(text)
        if parsed.netloc:
            return parsed.netloc.lower().removeprefix("www.")
    except Exception:
        pass
    return None
