import re
from models.schemas import DetectedType

# Maximum number of queries per investigation (adjustable)
MAX_QUERIES = 7


def _format_term(term: str) -> str:
    """Quote short entities (<= 3 words) to enforce exact matching; keep descriptive phrases unquoted."""
    clean = term.strip()
    words = clean.split()
    if len(words) <= 3 and not (clean.startswith('"') and clean.endswith('"')):
        return f'"{clean}"'
    return clean


def _extract_offer_phrases(text: str) -> list[str]:
    """Extract key searchable claims and phrases from long text offers."""
    phrases: list[str] = []
    lower = text.lower()

    # 1. Check for company name pattern, e.g. "at [Company]", "join [Company]"
    company_match = re.search(r"\b(?:join|at|with|by)\s+([A-Z][A-Za-z0-9\s&]{2,25})\b", text)
    if company_match:
        cand = company_match.group(1).strip()
        if not any(w in cand.lower() for w in ("our company", "our team", "home", "us", "website")):
            phrases.append(f'"{cand}" scam')
            phrases.append(f'"{cand}" complaints')

    # 2. Extract monetary amounts (e.g. ₹50,000, ₹999, ₹8 LPA)
    amounts = re.findall(r"(?:₹|\$|rs\.?|inr)?\s*[\d,]+(?:\s*(?:lpa|per\s+month|p\.?m\.?|daily))?", text, re.IGNORECASE)
    clean_amounts = [a.strip() for a in amounts if any(c.isdigit() for c in a)]

    has_wfh = "home" in lower
    has_reg_fee = any(k in lower for k in ("registration fee", "joining fee", "fee", "deposit"))
    has_guaranteed = "guaranteed" in lower
    has_no_exp = "no experience" in lower

    # 3. Generate targeted pattern queries
    if has_reg_fee and clean_amounts:
        fee_amt = clean_amounts[-1] if len(clean_amounts) > 1 else clean_amounts[0]
        phrases.append(f'{fee_amt} registration fee job scam')
    elif has_reg_fee:
        phrases.append('"registration fee" job scam complaints')

    if has_wfh and clean_amounts:
        earn_amt = clean_amounts[0]
        phrases.append(f'{earn_amt} work from home scam')
    elif has_wfh:
        phrases.append('work from home no experience scam')

    if has_guaranteed:
        phrases.append('guaranteed income work from home scam')

    if has_wfh and has_no_exp and has_reg_fee:
        phrases.append('work from home no experience registration fee')

    # Check for professional job title patterns (e.g. software engineer)
    title_match = re.search(r"\b(?:as\s+a\s+|for\s+)(software engineer|developer|manager|analyst|associate|executive|accountant)\b", text, re.IGNORECASE)
    if title_match:
        job_title = title_match.group(1).strip()
        phrases.append(f'"{job_title}" job recruitment reviews')
        phrases.append(f'"{job_title}" job recruitment scam')

    if not phrases:
        words = [w for w in text.split() if w.lower() not in ("the", "is", "a", "an", "and", "or", "in", "to", "for", "of", "with", "from", "by", "our")]
        short_clause = " ".join(words[:5])
        phrases.append(f'{short_clause} scam')
        phrases.append(f'{short_clause} complaints')

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for p in phrases:
        key = p.lower()
        if key not in seen:
            seen.add(key)
            unique.append(p)

    return unique


def _base_queries(term: str) -> list[str]:
    """Core scam-investigation queries applicable to any input."""
    if len(term.split()) > 5 or "." in term or "!" in term:
        return _extract_offer_phrases(term)
    t = _format_term(term)
    return [
        f'{t} scam',
        f'{t} fraud',
        f'{t} complaints',
        f'{t} reviews',
        f'{t} warning',
    ]


def _extract_canonical_domain(term: str) -> str:
    cleaned = term.strip().lower()
    cleaned = re.sub(r"^https?://", "", cleaned)
    cleaned = re.sub(r"^www\.", "", cleaned)
    return cleaned.split("/")[0].split(":")[0].split("?")[0].strip()


def _url_queries(term: str) -> list[str]:
    dom = _extract_canonical_domain(term)
    if not dom:
        dom = term.strip()
    return [
        f'"{dom}" scam',
        f'"{dom}" fraud',
        f'"{dom}" complaints',
        f'"{dom}" security',
        f'"{dom}" abuse',
        f'"{dom}" reviews',
    ]


def _company_queries(term: str) -> list[str]:
    if len(term.split()) > 5 or "." in term:
        return _extract_offer_phrases(term)
    queries = _base_queries(term)
    t = _format_term(term)
    queries += [
        f'{t} news',
        f'{t} fake',
    ]
    return queries


def _job_queries(term: str) -> list[str]:
    if len(term.split()) > 5 or "." in term or any(k in term.lower() for k in ("earn", "pay", "per month", "registration fee", "guaranteed")):
        return _extract_offer_phrases(term)
    queries = _base_queries(term)
    t = _format_term(term)
    queries += [
        f'{t} recruitment',
        f'{t} payment',
    ]
    return queries


def _suspicious_offer_queries(term: str) -> list[str]:
    return _extract_offer_phrases(term)


def _investment_queries(term: str) -> list[str]:
    if len(term.split()) > 5 or "." in term:
        return _extract_offer_phrases(term)
    queries = _base_queries(term)
    t = _format_term(term)
    queries += [
        f'{t} news',
        f'{t} regulatory',
    ]
    return queries


def _course_queries(term: str) -> list[str]:
    if len(term.split()) > 5 or "." in term:
        return _extract_offer_phrases(term)
    queries = _base_queries(term)
    t = _format_term(term)
    queries += [
        f'{t} refund',
        f'{t} placement',
    ]
    return queries


def _shopping_queries(term: str) -> list[str]:
    if len(term.split()) > 5 or "." in term:
        return _extract_offer_phrases(term)
    queries = _base_queries(term)
    t = _format_term(term)
    queries += [
        f'{t} refund',
        f'{t} fake',
    ]
    return queries


def generate_queries(normalized_input: str, detected_type: DetectedType) -> list[str]:
    """Generate a list of targeted search queries.

    Returns at most MAX_QUERIES unique queries.
    """
    generators = {
        DetectedType.URL: _url_queries,
        DetectedType.COMPANY: _company_queries,
        DetectedType.JOB_OFFER: _job_queries,
        DetectedType.SUSPICIOUS_OFFER: _suspicious_offer_queries,
        DetectedType.INVESTMENT: _investment_queries,
        DetectedType.COURSE: _course_queries,
        DetectedType.SHOPPING: _shopping_queries,
        DetectedType.GENERAL: _base_queries,
    }

    gen = generators.get(detected_type, _base_queries)
    queries = gen(normalized_input)

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for q in queries:
        key = q.lower()
        if key not in seen:
            seen.add(key)
            unique.append(q)

    return unique[:MAX_QUERIES]

