"""Evidence extractor for ScamShield.

Performs:
1. Accurate source type classification (Government/Regulatory, News, Company, Review, Blog/Forum, Other)
   derived strictly from domain properties, never inferred from keywords.
2. Contextual relationship disambiguation (DIRECT, IMPERSONATION_TARGET, GENERAL_WARNING, etc.).
3. Strict regulatory warning criteria: Only authoritative government/regulatory domains can be
   classified as REGULATORY_WARNING, and only when the action specifically targets the entity.
4. Canonical URL deduplication and content-similarity clustering.
"""

from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from models.schemas import (
    EvidenceCategory,
    EvidenceItem,
    EvidenceRelationship,
    EvidenceStrength,
    SourceItem,
    SourceTrust,
    SourceType,
)

# ── Domain Authority & Categorization Dictionaries ─────────────────────────────

_GOVERNMENT_REGULATORY_DOMAINS = [
    # Top level domains & ccTLD government prefixes
    ".gov", ".gov.in", ".gov.uk", ".gov.au", ".gov.sg", ".gc.ca", ".mil", ".police.uk",
    # Specific regulatory & enforcement agency domains
    "fca.org.uk", "sec.gov", "ftc.gov", "cisa.gov", "consumerfinance.gov",
    "finra.org", "interpol.int", "ic3.gov", "asic.gov.au", "mas.gov.sg",
    "osc.ca", "rbi.org.in", "sebi.gov.in", "mca.gov.in", "police.uk",
    "actionfraud.police.uk", "scamwatch.gov.au", "dfpi.ca.gov", "bafin.de",
    "finma.ch", "amf-france.org", "consob.it", "cnmv.es", "fsma.be", "sfc.hk",
    "cftc.gov", "justice.gov",
]

_NEWS_DOMAINS = [
    "reuters.com", "bbc.com", "bbc.co.uk", "nytimes.com", "theguardian.com",
    "washingtonpost.com", "apnews.com", "cnbc.com", "bloomberg.com", "forbes.com",
    "wsj.com", "techcrunch.com", "wired.com", "arstechnica.com", "theverge.com",
    "bleepingcomputer.com", "cnn.com", "foxnews.com", "economictimes.com",
    "timesofindia.indiatimes.com", "ndtv.com", "hindustantimes.com", "thehindu.com",
    "livemint.com", "news18.com", "moneycontrol.com", "axios.com", "politico.com",
    "cnet.com", "zdnet.com", "marketwatch.com", "businessinsider.com", "usatoday.com",
    "huffpost.com", "yahoo.com", "dailymail.co.uk", "independent.co.uk", "telegraph.co.uk",
    "latimes.com", "newsweek.com", "engadget.com", "gizmodo.com", "tomshardware.com",
    "pcworld.com", "infosecurity-magazine.com", "krebsonsecurity.com", "darkreading.com",
]

_REVIEW_DOMAINS = [
    "trustpilot.com", "bbb.org", "glassdoor.com", "indeed.com", "sitejabber.com",
    "consumeraffairs.com", "ambitionbox.com", "mouthshut.com", "scamadviser.com",
    "scamvoid.net", "islegitsite.com", "productreview.com.au", "yelp.com",
    "complaintsboard.com", "pissedconsumer.com", "ripoffreport.com", "g2.com",
    "capterra.com", "tripadvisor.com", "scam-detector.com", "who-called.co.uk",
    "shouldianswer.com", "findwhocallsme.com",
]

_BLOG_FORUM_DOMAINS = [
    "reddit.com", "quora.com", "medium.com", "wordpress.com", "blogspot.com",
    "substack.com", "tumblr.com", "discussions.apple.com", "answers.microsoft.com",
    "stackexchange.com", "stackoverflow.com", "groups.google.com", "github.com",
    "malwaretips.com",
]


# ── Keyword Dictionaries ────────────────────────────────────────────────────────

# 1. Consumer Dissatisfaction (product quality, customer support, bugs, refund delays)
# These represent non-fraudulent commercial friction and contribute 0 scam risk.
_DISSATISFACTION_KEYWORDS = [
    # Customer support
    "poor service", "bad service", "poor customer service", "bad customer service",
    "customer support", "support ticket", "ticket escalating", "escalating ticket",
    "unhelpful support", "rude support", "rude staff", "unresponsive support",
    "slow support", "ticket ignored", "wait times", "hold time", "help desk",
    "call center", "customer care", "support representative", "bad support",
    "poor communication", "support agent",
    # Software bugs / technical glitches
    "software bug", "software bugs", "software issues", "technical glitch",
    "glitch", "glitches", "app crashed", "crashes", "system crash", "outage",
    "service outage", "downtime", "update broke", "broken update", "slow performance",
    "performance issues", "sync issue", "login issue", "server down", "headaches",
    "buggy", "workaround", "workarounds", "bug fix", "issue with update",
    # Refund dissatisfaction / commercial billing disputes
    "refund dissatisfaction", "refund delay", "refund request", "refund denied",
    "cancellation policy", "cancel subscription", "subscription cancellation",
    "billing dispute", "auto-renew", "cancellation fee", "overcharged on bill",
    "disputed charge", "return policy", "delay in refund", "difficulty cancelling",
    "refund issues",
    # Product quality / hardware
    "product quality", "poor quality", "defective product", "defective item",
    "hardware issue", "hardware defect", "battery drain", "overpriced",
    "disappointing product", "buyer remorse", "build quality", "poor build",
    "cheap material", "failed after",
]

# 2. Fraud & Scam Allegations
_FRAUD_ALLEGATION_KEYWORDS = [
    "scam", "fraud", "scammer", "fraudulent", "ponzi", "pyramid scheme",
    "swindle", "con artist", "deceptive practices", "bogus", "cheated",
    "cheated out of", "fake recruitment", "fake job", "ghost job scam",
    "interview scam", "task scam", "fake offer", "stole my money", "stole money",
    "defrauded", "financial loss", "lost life savings", "lost savings",
    "scammed me", "robbed", "deception", "stolen funds", "confidence trick",
    "extortion", "ripped off by scam", "fraudulent actor",
]

# 3. Payment Fraud & Advance Fee
_PAYMENT_FRAUD_KEYWORDS = [
    "payment fraud", "credit card fraud", "unauthorized charge", "unauthorized charges",
    "unauthorized transaction", "stolen card", "card drained", "bank fraud",
    "wire fraud", "payment deception", "upfront fee", "registration fee",
    "advance fee", "pay before", "processing fee", "deposit required",
    "equipment fee", "training fee", "deposit scam", "frozen withdrawal",
    "frozen account", "refusal to withdraw", "withhold funds", "pay to withdraw",
    "ransom", "extortion payment",
]

# 4. Impersonation & Brand Spoofing Keywords
_IMPERSONATION_KEYWORDS = [
    "impersonat", "spoof", "pretending to be", "posing as", "fake support",
    "fake tech support", "tech support scam", "fake representative",
    "fake recruiter", "scammers claiming to be", "fraudsters claiming to be",
    "victims of tech support scams", "victims of scam", "victims of scams",
    "scam callers", "phishing claiming to be", "bogus support",
    "impersonating our brand", "scam using company name",
]

# Generic complaint / review indicators
_COMPLAINT_KEYWORDS = [
    "complaint", "complain", "bad experience", "unresponsive", "never received",
    "not delivered", "poor service",
]

_PAYMENT_KEYWORDS = [
    "upfront fee", "registration fee", "advance payment", "pay before",
    "money transfer", "wire transfer", "pay first", "processing fee",
    "deposit required", "advance fee", "equipment fee", "training fee",
]

_NEGATIVE_REVIEW_KEYWORDS = [
    "1 star", "one star", "do not recommend", "avoid", "beware",
    "stay away", "not worth", "waste of money", "disappointing",
]

_POSITIVE_KEYWORDS = [
    "legitimate", "trusted", "verified", "accredited", "established",
    "certified", "reliable", "reputable", "official site", "official website",
    "corporate headquarters", "sec filing", "annual report", "publicly traded",
]

# 5. Security & Abuse Keywords (Requirement 4 & 5: Separate security information from scam evidence)
_SECURITY_KEYWORDS = [
    "dns complaint", "dns configuration", "dns issue", "dns record",
    "nameserver", "mx record", "ssl certificate", "tls certificate",
    "certificate expired", "ssl issue", "ssl test", "vulnerability scan",
    "malware scan", "sitecheck", "virustotal", "safe browsing",
    "security report", "security rating", "cve-", "open port",
    "blacklist check", "dns check", "domain security", "security score",
    "ssl/tls", "security vulnerability",
]

_ABUSE_KEYWORDS = [
    "abuse report", "abuse complaint", "abuse contact", "spamhaus",
    "abuseipdb", "registrar abuse", "dmca complaint", "spam complaint",
    "abuse notice", "network abuse", "botnet activity", "spam listing",
    "domain abuse", "abuse desk",
]


# ── Canonical URL & Domain helpers ──────────────────────────────────────────────

def _extract_canonical_domain(input_str: str) -> str | None:
    """Extract clean domain from input if it represents a website, domain, or URL."""
    cleaned = input_str.strip().lower()
    cleaned = re.sub(r"^https?://", "", cleaned)
    cleaned = re.sub(r"^www\.", "", cleaned)
    host = cleaned.split("/")[0].split(":")[0].split("?")[0].strip()
    if "." in host and not any(c in host for c in (" ", "\n", "\t")):
        parts = host.split(".")
        if len(parts) >= 2 and len(parts[-1]) >= 2:
            return host
    return None


def _is_result_relevant_for_domain(
    target_domain: str,
    raw_url: str,
    title: str,
    snippet: str,
) -> tuple[bool, str]:
    """Check whether a search result is genuinely relevant to the investigated domain."""
    res_domain = _extract_domain(raw_url).lower()
    res_path = urlparse(raw_url).path.lower()
    title_lower = title.lower()
    snippet_lower = snippet.lower()
    target_lower = target_domain.lower()

    # 1. Target's own domain or subdomains
    if res_domain == target_lower or res_domain.endswith("." + target_lower):
        return True, "own_domain"

    # 2. Check if target_domain appears as a whole domain name
    target_pattern = rf"(^|[^\w\.\-]|\b){re.escape(target_lower)}([^\w\.\-]|\b|$)"
    in_title = bool(re.search(target_pattern, title_lower))
    in_path = bool(re.search(target_pattern, res_path))

    # 3. Check for generic tax, DMV, and state revenue pages (IRS, Nebraska DMV, etc.)
    unrelated_hosts = ("irs.gov", "revenue.", "tax.", "dmv.", "motorvehicles.", "dor.")
    unrelated_title_patterns = (
        "where's my refund", "wheres my refund", "tax refund", "income tax return",
        "state tax", "driver's license", "vehicle registration", "forms & instructions",
        "file your taxes", "internal revenue service", "department of revenue",
        "taxpayer advocate", "refund status", "check your refund", "motor vehicles"
    )
    if any(h in res_domain for h in unrelated_hosts) or any(p in title_lower for p in unrelated_title_patterns):
        if not in_title:
            return False, "unrelated_tax_or_dmv"

    # 4. Check if target_domain appears in title or URL path
    if in_title or in_path:
        return True, "mentioned_in_title_or_path"

    # 5. Check if target_domain appears in snippet (excluding incidental email address placeholders)
    if re.search(target_pattern, snippet_lower):
        incidental_email_patterns = [
            rf"\b[a-zA-Z0-9_\.\-]+@{re.escape(target_lower)}\b",
            rf"e\.?g\.?,?\s*[a-zA-Z0-9_\.\-]+@{re.escape(target_lower)}",
            rf"example:\s*[a-zA-Z0-9_\.\-]+@{re.escape(target_lower)}",
        ]
        cleaned_snippet = snippet_lower
        for pat in incidental_email_patterns:
            cleaned_snippet = re.sub(pat, "", cleaned_snippet)

        if re.search(target_pattern, cleaned_snippet):
            # Also ensure not in an unrelated topic (job scams, grant program)
            if any(k in title_lower for k in ("job scam", "crypto scam", "grant program", "highway")):
                return False, "incidental_mention_in_unrelated_topic"
            return True, "discussed_in_snippet"
        else:
            return False, "incidental_email_placeholder"

    # 6. Neither title, path, nor snippet meaningfully discusses target_domain
    return False, "target_domain_not_mentioned"


def _extract_domain(url: str) -> str:
    """Extract clean domain without www or ports."""
    try:
        parsed = urlparse(url)
        host = parsed.netloc or parsed.path.split("/")[0]
        host = host.split(":")[0]
        return host.lower().removeprefix("www.")
    except Exception:
        return url.strip().lower()


def _canonical_url(url: str) -> str:
    """Remove tracking parameters, anchors, and standardize URL for deduplication."""
    try:
        parsed = urlparse(url)
        clean_path = parsed.path.rstrip("/")
        query_params = parse_qsl(parsed.query)
        filtered = [
            (k, v) for k, v in query_params
            if not (k.startswith("utm_") or k in ("ref", "fbclid", "gclid", "source", "ref_src", "mc_cid", "mc_eid", "amp"))
        ]
        clean_query = urlencode(filtered)
        clean_host = (parsed.netloc or "").lower().removeprefix("www.")
        return urlunparse(("https", clean_host, clean_path, "", clean_query, ""))
    except Exception:
        return url.strip().lower()


def _classify_source_type_and_trust(domain: str, normalized_input: str) -> tuple[str, SourceTrust]:
    """Classify the exact source type strictly from the publishing domain.
    
    Categories:
    - Government / Regulatory
    - News
    - Company
    - Review
    - Blog / Forum
    - Other
    
    Never infer source type from words in the article snippet.
    """
    domain_lower = domain.lower()
    core_entity = _extract_core_entity_name(normalized_input).lower()

    # 1. Government / Regulatory Authority
    # Strict domain check: ends with .gov, .mil, has .gov., or in explicit regulator list
    is_gov = False
    if domain_lower.endswith(".gov") or domain_lower.endswith(".mil") or ".gov." in domain_lower:
        is_gov = True
    elif domain_lower.endswith(".gc.ca") or domain_lower.endswith(".police.uk"):
        is_gov = True
    else:
        for gov in _GOVERNMENT_REGULATORY_DOMAINS:
            if domain_lower == gov or domain_lower.endswith("." + gov):
                is_gov = True
                break

    if is_gov:
        return SourceType.GOVERNMENT_REGULATORY.value, SourceTrust.HIGHER

    # 2. Blog / Forum (Check community/forum subdomains before company matching)
    # E.g. answers.microsoft.com, discussions.apple.com, community.zoom.com, reddit.com
    for bf in _BLOG_FORUM_DOMAINS:
        if domain_lower == bf or domain_lower.endswith("." + bf):
            return SourceType.BLOG_FORUM.value, SourceTrust.LOWER

    if any(k in domain_lower for k in ("forum.", "forums.", "community.", "discussions.", "board.", "discussion")):
        return SourceType.BLOG_FORUM.value, SourceTrust.LOWER

    if any(k in domain_lower for k in ("reddit", "quora", "medium.com", "blogspot", "wordpress", "substack")):
        return SourceType.BLOG_FORUM.value, SourceTrust.LOWER

    # 3. Investigated Entity's Own Domain / Company Website
    # (e.g. microsoft.com, support.microsoft.com, example.com)
    is_company = False
    if "." in normalized_input and "/" not in normalized_input:
        input_dom = _extract_domain(normalized_input)
        if domain_lower == input_dom or domain_lower.endswith("." + input_dom):
            is_company = True
    elif core_entity and len(core_entity) >= 3:
        parts = domain_lower.split(".")
        if len(parts) >= 2 and (parts[-2] == core_entity or parts[0] == core_entity):
            is_company = True

    if is_company:
        return SourceType.COMPANY.value, SourceTrust.HIGHER

    # 4. Established News Media
    for nd in _NEWS_DOMAINS:
        if domain_lower == nd or domain_lower.endswith("." + nd):
            return SourceType.NEWS.value, SourceTrust.HIGHER

    if any(k in domain_lower for k in ("news.", "-news.", ".news", "tribune", "chronicle", "gazette")):
        return SourceType.NEWS.value, SourceTrust.HIGHER

    # 5. Review / Complaint Platforms
    for rd in _REVIEW_DOMAINS:
        if domain_lower == rd or domain_lower.endswith("." + rd):
            return SourceType.REVIEW.value, SourceTrust.MEDIUM

    if any(k in domain_lower for k in ("review", "rating", "trustscore", "complaint", "scamadviser", "scamvoid")):
        return SourceType.REVIEW.value, SourceTrust.MEDIUM

    # 6. Other Web Result
    return SourceType.OTHER.value, SourceTrust.LOWER


# ── Entity Analysis & Relationship Classification ───────────────────────────────

def _extract_core_entity_name(raw_name: str) -> str:
    """Extract clean entity name removing corporate suffixes and URL prefixes."""
    cleaned = raw_name.strip()
    if "://" in cleaned or "." in cleaned:
        try:
            parsed = urlparse(cleaned if "://" in cleaned else f"https://{cleaned}")
            netloc = (parsed.netloc or parsed.path).lower().removeprefix("www.")
            cleaned = netloc.split(".")[0]
        except Exception:
            pass

    cleaned = re.sub(
        r"\b(inc|incorporated|ltd|limited|corp|corporation|llc|co|company|group|technologies|systems|agency)\b",
        "",
        cleaned,
        flags=re.IGNORECASE,
    ).strip()
    return cleaned if cleaned else raw_name.strip()


def _is_entity_mentioned(entity_name: str, text: str) -> bool:
    """Check if the entity name is meaningfully mentioned in text."""
    if not entity_name:
        return True
    pattern = rf"\b{re.escape(entity_name)}\b"
    return bool(re.search(pattern, text, re.IGNORECASE))


def _classify_relationship_and_category(
    title: str,
    snippet: str,
    domain: str,
    source_type: str,
    source_trust: SourceTrust,
    normalized_input: str,
    raw_url: str = "",
) -> tuple[EvidenceRelationship, EvidenceCategory, EvidenceStrength, str | None]:
    """Determine the relationship, category, severity, and complaint type.

    Distinguishes between:
    1. FRAUD_ALLEGATION (fake job, fraud, ponzi, swindle, deception)
    2. SCAM_REPORT (scam report on consumer protection / review sites)
    3. SECURITY_REPORT (DNS, SSL, malware, vulnerability technical findings)
    4. ABUSE_REPORT (abuse report, Spamhaus, AbuseIPDB, registrar abuse complaint)
    5. CONSUMER_DISSATISFACTION (poor support, software bugs, refund disputes -> 0 scam risk)
    6. DIRECT_COMPLAINT (delivery delay, commercial dispute without fraud allegation)
    7. REGULATORY_WARNING (official enforcement action / penalty by authorities)
    8. GENERAL_ADVISORY (educational guide, general security bulletin)
    9. IMPERSONATION_TARGET (scammers posing as brand, fake support)
    10. NEUTRAL_PROFILE (directory listing, corporate profile, WHOIS, reserved domain)
    11. VERIFICATION_SIGNAL (official company presence, SEC filing, verified registry)
    12. UNRELATED (off-topic, incidental placeholders, generic tax/DMV pages)
    """
    combined = f"{title} {snippet}".strip()
    combined_lower = combined.lower()
    core_entity = _extract_core_entity_name(normalized_input)
    core_entity_lower = core_entity.lower()
    is_gov = (source_type == SourceType.GOVERNMENT_REGULATORY.value)

    # 0. Entity Relevance Filter for URL / domain investigations (Requirement 1 & 3)
    target_domain = _extract_canonical_domain(normalized_input)
    if target_domain:
        is_relevant, _ = _is_result_relevant_for_domain(target_domain, raw_url, title, snippet)
        if not is_relevant:
            return (
                EvidenceRelationship.UNRELATED,
                EvidenceCategory.UNRELATED,
                EvidenceStrength.LOW,
                None,
            )

    # 1. Official Company Domain
    if source_type == SourceType.COMPANY.value:
        if any(w in combined_lower for w in ["protect yourself", "security guidance", "report scam", "avoid phishing", "fraud alert", "impersonation"]):
            return (
                EvidenceRelationship.IMPERSONATION_TARGET,
                EvidenceCategory.IMPERSONATION_TARGET,
                EvidenceStrength.LOW,
                "impersonation",
            )
        return (
            EvidenceRelationship.POSITIVE_SIGNAL,
            EvidenceCategory.VERIFICATION_SIGNAL,
            EvidenceStrength.LOW,
            None,
        )

    # 2. Impersonation Target Patterns (Entity is the brand being spoofed/attacked by third parties)
    impersonation_patterns = [
        rf"\b(impersonat\w*|spoof\w*|pos\w+\s+as|pretend\w*\s+to\s+be|claim\w*\s+to\s+be)\s+(from\s+|as\s+)?(the\s+)?{re.escape(core_entity_lower)}",
        rf"{re.escape(core_entity_lower)}\s+(impersonat\w*|spoof\w*|tech\s+support\s+scam|phishing\s+scam|fake\s+support|phone\s+scam|call\s+scam|warning\s+alert\s+scam|support\s+scam|defender\s+scam|alert\s+scam|important\s+alert)",
        rf"\b(scam\w*|fraudster\w*|phisher\w*|attacker\w*|criminal\w*)\s+(are\s+|is\s+)?(using|leveraging|exploiting|abusing)\s+.*{re.escape(core_entity_lower)}",
        rf"\b(fake|fraudulent|bogus|malicious)\s+{re.escape(core_entity_lower)}\s+(support|technician|rep|agent|email|invoice|alert|notification|website|site|portal|job|pop-?up|call|audit|survey|recruitment|offer|drive|hiring|letter|department|security\s+scan)",
        rf"\b(beware of|watch out for|protect yourself from|avoid)\s+(fake\s+|scams?\s+claiming to be\s+|scammers?\s+pretending to be\s+)?{re.escape(core_entity_lower)}",
        rf"{re.escape(core_entity_lower)}\s+(warns|advises|alerts|cautions|urges|guidance|security bulletin|delivers\s+.*warning)\s+.*(scam|fraud|phish|threat|cybercrime)",
        rf"{re.escape(core_entity_lower)}.*(sends?|issues?|posts?).*(warning|alert).*(scam|fraud|phish|victim)",
        rf"(ftc|fbi|cisa|police|sec|regulator|consumer alert|bbb)\s+.*(scam|fraud|call)\s+(impersonat\w*|pretend\w*|claim\w* to be)\s+.*{re.escape(core_entity_lower)}",
        rf"(victims? of\s+.*(tech support|phishing|phone|impersonation|gift card)\s+scams?)\b",
        rf"{re.escape(core_entity_lower)}.*(receives?|reported).*(complaints? from victims?|reports? of scams?)",
        rf"\b(scams?|attackers?|fraudsters?)\s+targets?\s+{re.escape(core_entity_lower)}",
        rf"\b(thought was|supposedly)\s+(the\s+)?{re.escape(core_entity_lower)}\s+(fraud|support)",
        rf"\b(fake\s+{re.escape(core_entity_lower)}\s+(site|emails?|account|app))\b",
        rf"\b(pop-?up\s+scam|tech\s+support\s+scams?)\b",
    ]
    for pat in impersonation_patterns:
        if re.search(pat, combined_lower):
            return (
                EvidenceRelationship.IMPERSONATION_TARGET,
                EvidenceCategory.IMPERSONATION_TARGET,
                EvidenceStrength.HIGH,
                "impersonation",
            )

    if any(k in combined_lower for k in ("tech support scam", "fake tech support", "phone scam pretending", "pop-up scam")) and _is_entity_mentioned(core_entity, combined):
        return (
            EvidenceRelationship.IMPERSONATION_TARGET,
            EvidenceCategory.IMPERSONATION_TARGET,
            EvidenceStrength.HIGH,
            "impersonation",
        )

    # 2b. Generic directory indexes (e.g. BBB profile directory landing pages)
    if "bbb.org" in domain.lower() and "view complaints of" in combined_lower and "helps resolve disputes" in combined_lower:
        return (
            EvidenceRelationship.NEUTRAL,
            EvidenceCategory.NEUTRAL_PROFILE,
            EvidenceStrength.LOW,
            None,
        )

    # 3. Government / Regulatory Source
    if is_gov:
        direct_regulatory_action_patterns = [
            rf"(fined|charged|sued|sanctioned|ordered to pay|barred|banned|enforcement action against|settles with|indicted)\s+.*{re.escape(core_entity_lower)}",
            rf"{re.escape(core_entity_lower)}\s+(fined|charged|sued|ordered to|agrees to pay|faces lawsuit|faces penalty|shut down by)",
            rf"(warning against|caution list|unauthorized firm|unregistered firm)\s+.*{re.escape(core_entity_lower)}",
        ]
        for pat in direct_regulatory_action_patterns:
            if re.search(pat, combined_lower):
                return (
                    EvidenceRelationship.DIRECT,
                    EvidenceCategory.REGULATORY_WARNING,
                    EvidenceStrength.HIGH,
                    "regulatory_action",
                )

        is_gov_scam_advisory = any(k in combined_lower for k in (
            "scam", "fraud", "phish", "cybercrime", "consumer protection",
            "identity theft", "fake job", "advance fee", "caution", "alert", "warning",
            "security advisory", "protect yourself", "bad actor", "complaint"
        ))
        if is_gov_scam_advisory:
            return (
                EvidenceRelationship.GENERAL_ADVISORY,
                EvidenceCategory.GENERAL_ADVISORY,
                EvidenceStrength.LOW,
                None,
            )

        return (
            EvidenceRelationship.UNRELATED,
            EvidenceCategory.UNRELATED,
            EvidenceStrength.LOW,
            None,
        )

    # 4. News reporting formal legal enforcement or lawsuits directly against entity
    if source_type == SourceType.NEWS.value:
        legal_news_patterns = [
            rf"(lawsuit|sued|indicted|charged|regulator fines|court orders)\s+.*{re.escape(core_entity_lower)}",
            rf"{re.escape(core_entity_lower)}\s+(faces lawsuit|settles charges|penalized by regulator)",
        ]
        for pat in legal_news_patterns:
            if re.search(pat, combined_lower):
                is_scam_or_fraud_legal = any(w in combined_lower for w in (
                    "fraud", "scam", "deceptive", "deception", "misleading", "ponzi",
                    "pyramid", "defrauded", "embezzle", "consumer protection",
                    "advance fee", "fake", "stole", "theft", "unauthorized charges"
                ))
                is_ip_or_commercial = any(w in combined_lower for w in (
                    "copyright", "patent", "trademark infringement", "antitrust", "royalt"
                ))
                if is_scam_or_fraud_legal and not is_ip_or_commercial:
                    return (
                        EvidenceRelationship.DIRECT,
                        EvidenceCategory.REGULATORY_WARNING,
                        EvidenceStrength.HIGH,
                        "regulatory_action",
                    )
                return (
                    EvidenceRelationship.NEUTRAL,
                    EvidenceCategory.NEUTRAL_PROFILE,
                    EvidenceStrength.LOW,
                    None,
                )

    # 5. Technical Security & Abuse Reports (Requirement 4 & 5: Separate security/abuse reports from scam)
    # E.g. "DNS Complaint - example.com", SSL tests, VirusTotal, AbuseIPDB, Spamhaus
    has_security_kw = any(kw in combined_lower for kw in _SECURITY_KEYWORDS)
    has_abuse_kw = any(kw in combined_lower for kw in _ABUSE_KEYWORDS)
    if (has_security_kw or has_abuse_kw) and _is_entity_mentioned(core_entity, combined):
        if has_abuse_kw:
            return (
                EvidenceRelationship.SECURITY_ABUSE,
                EvidenceCategory.ABUSE_REPORT,
                EvidenceStrength.LOW,
                "abuse_report",
            )
        return (
            EvidenceRelationship.SECURITY_ABUSE,
            EvidenceCategory.SECURITY_REPORT,
            EvidenceStrength.LOW,
            "security_report",
        )

    # 6. Payment Fraud / Advance Fee Demands directly linked to entity
    if any(kw in combined_lower for kw in _PAYMENT_FRAUD_KEYWORDS) and _is_entity_mentioned(core_entity, combined):
        return (
            EvidenceRelationship.DIRECT,
            EvidenceCategory.PAYMENT_FRAUD,
            EvidenceStrength.HIGH,
            "payment_fraud",
        )

    # 7. Direct Scam / Fraud Allegations directly accusing entity
    direct_scam_patterns = [
        rf"{re.escape(core_entity_lower)}\s+(is\s+(a\s+)?(scam|fraud|fake|ponzi|pyramid|scammer|swindle)|scammed|stole|cheated|ripped\s+off|defrauded)",
        rf"(scam|fraud|fake recruitment|employment scam|fake job|ghost job scam|swindle|theft|deception)\s+(committed\s+by|by|from|at)\s+{re.escape(core_entity_lower)}",
        rf"(complaint|allegation|lawsuit)\s+accusing\s+{re.escape(core_entity_lower)}\s+of\s+(fraud|scam|deception|theft)",
        rf"(lost\s+(money|savings|funds)|stole\s+(my\s+)?(money|savings)|financial\s+loss)\s+(to|from|by)\s+{re.escape(core_entity_lower)}",
        rf"accuses?\s+{re.escape(core_entity_lower)}\s+of\s+(fraud|scam|deception)",
    ]
    for pat in direct_scam_patterns:
        if re.search(pat, combined_lower):
            return (
                EvidenceRelationship.DIRECT,
                EvidenceCategory.FRAUD_ALLEGATION,
                EvidenceStrength.HIGH if source_trust in (SourceTrust.HIGHER, SourceTrust.MEDIUM) else EvidenceStrength.MEDIUM,
                "fraud_scam_allegation",
            )

    if any(w in combined_lower for w in ("flagged as scam", "scam alert", "fake website", "confirmed scam")) and _is_entity_mentioned(core_entity, combined):
        return (
            EvidenceRelationship.DIRECT,
            EvidenceCategory.SCAM_REPORT,
            EvidenceStrength.HIGH if source_trust in (SourceTrust.HIGHER, SourceTrust.MEDIUM) else EvidenceStrength.MEDIUM,
            "scam_report",
        )

    # 8. Direct Consumer Dissatisfaction (poor customer support, software bugs, refund dissatisfaction, product quality)
    has_dissatisfaction_kw = any(kw in combined_lower for kw in _DISSATISFACTION_KEYWORDS)
    if has_dissatisfaction_kw and _is_entity_mentioned(core_entity, combined):
        return (
            EvidenceRelationship.NEGATIVE_MENTION,
            EvidenceCategory.CONSUMER_DISSATISFACTION,
            EvidenceStrength.LOW,
            "consumer_dissatisfaction",
        )

    # 9. Other Legitimate Complaints & Negative Reviews
    if any(kw in combined_lower for kw in _COMPLAINT_KEYWORDS) and _is_entity_mentioned(core_entity, combined):
        return (
            EvidenceRelationship.NEGATIVE_MENTION,
            EvidenceCategory.DIRECT_COMPLAINT,
            EvidenceStrength.LOW,
            "direct_complaint",
        )

    if any(kw in combined_lower for kw in _NEGATIVE_REVIEW_KEYWORDS) and _is_entity_mentioned(core_entity, combined):
        return (
            EvidenceRelationship.NEGATIVE_MENTION,
            EvidenceCategory.DIRECT_COMPLAINT,
            EvidenceStrength.LOW,
            "direct_complaint",
        )

    # Inquiries ("Is X a scam?", "Is X legit?")
    inquiry_patterns = [
        rf"is\s+{re.escape(core_entity_lower)}\s+(a\s+)?(scam|legit|fraud|safe)",
        rf"{re.escape(core_entity_lower)}\s+reviews\s+and\s+complaints",
    ]
    for pat in inquiry_patterns:
        if re.search(pat, combined_lower):
            return (
                EvidenceRelationship.NEGATIVE_MENTION,
                EvidenceCategory.DIRECT_COMPLAINT,
                EvidenceStrength.LOW,
                "direct_complaint",
            )

    # 10. General Scam Warnings / Educational Guides / Security Advisories
    if any(kw in combined_lower for kw in ("warning", "alert", "advisory", "consumer protection", "scam guide", "avoid scams", "stay safe")):
        return (
            EvidenceRelationship.GENERAL_ADVISORY,
            EvidenceCategory.GENERAL_ADVISORY,
            EvidenceStrength.LOW,
            None,
        )

    # 11. Positive Verification Signals
    if any(kw in combined_lower for kw in _POSITIVE_KEYWORDS) and _is_entity_mentioned(core_entity, combined):
        return (
            EvidenceRelationship.POSITIVE_SIGNAL,
            EvidenceCategory.VERIFICATION_SIGNAL,
            EvidenceStrength.LOW,
            None,
        )

    # 12. Neutral Directory / Profile / Reserved Domain Documentation
    if _is_entity_mentioned(core_entity, combined):
        return (
            EvidenceRelationship.NEUTRAL,
            EvidenceCategory.NEUTRAL_PROFILE,
            EvidenceStrength.LOW,
            None,
        )

    # 13. Unrelated / Off-topic
    return (
        EvidenceRelationship.UNRELATED,
        EvidenceCategory.UNRELATED,
        EvidenceStrength.LOW,
        None,
    )


# ── Public API ──────────────────────────────────────────────────────────────────

def extract_evidence(
    all_results: list[dict],
    normalized_input: str,
) -> tuple[list[EvidenceItem], list[SourceItem], int, int, int, list[SourceItem]]:
    """Process raw SerpApi results into structured evidence and sources with deduplication.

    Returns:
        (evidence_items, source_items, unique_sources_count, duplicate_results_removed, filtered_unrelated_count, filtered_unrelated_items)
    """
    seen_canonical_urls: set[str] = set()
    seen_content_signatures: set[str] = set()
    evidence_items: list[EvidenceItem] = []
    source_items: list[SourceItem] = []
    filtered_unrelated_items: list[SourceItem] = []
    duplicate_results_removed = 0

    for result in all_results:
        raw_url = result.get("link", "").strip()
        if not raw_url:
            continue

        canon_url = _canonical_url(raw_url)
        title = result.get("title", "").strip()
        snippet = result.get("snippet", "").strip()

        # Content fingerprint (first 15 alphanumeric tokens of title + snippet)
        raw_tokens = re.findall(r"\w+", f"{title} {snippet}".lower())[:15]
        content_sig = " ".join(raw_tokens)

        # Deduplication check
        if canon_url in seen_canonical_urls or (content_sig and content_sig in seen_content_signatures):
            duplicate_results_removed += 1
            continue

        seen_canonical_urls.add(canon_url)
        if content_sig:
            seen_content_signatures.add(content_sig)

        displayed_link = result.get("displayed_link", raw_url)
        position = result.get("position")
        domain = _extract_domain(raw_url)

        # Strictly derive source type from domain
        source_type_label, source_trust = _classify_source_type_and_trust(domain, normalized_input)

        relationship, category, strength, complaint_type = _classify_relationship_and_category(
            title=title,
            snippet=snippet,
            domain=domain,
            source_type=source_type_label,
            source_trust=source_trust,
            normalized_input=normalized_input,
            raw_url=raw_url,
        )

        # Filter out completely UNRELATED items from main evidence and sources
        if relationship == EvidenceRelationship.UNRELATED or category == EvidenceCategory.UNRELATED:
            filtered_unrelated_items.append(
                SourceItem(
                    title=title,
                    domain=domain,
                    url=raw_url,
                    snippet=snippet,
                    evidence_category=EvidenceCategory.UNRELATED,
                    evidence_strength=EvidenceStrength.LOW,
                    source_type=source_type_label,
                    source_trust=source_trust,
                    position=position,
                    relationship=EvidenceRelationship.UNRELATED,
                    complaint_type="unrelated",
                )
            )
            continue

        summary = snippet[:300] if snippet else title
        is_imp = (relationship == EvidenceRelationship.IMPERSONATION_TARGET)

        evidence_items.append(
            EvidenceItem(
                category=category,
                severity=strength,
                title=title,
                summary=summary,
                source=displayed_link or domain,
                url=raw_url,
                snippet=snippet,
                evidence_strength=strength,
                source_type=source_type_label,
                source_trust=source_trust,
                relationship=relationship,
                risk_contribution=0,  # Computed subsequently by risk_engine
                is_impersonation_target=is_imp,
                complaint_type=complaint_type,
            )
        )

        source_items.append(
            SourceItem(
                title=title,
                domain=domain,
                url=raw_url,
                snippet=snippet,
                evidence_category=category,
                evidence_strength=strength,
                source_type=source_type_label,
                source_trust=source_trust,
                position=position,
                relationship=relationship,
                complaint_type=complaint_type,
            )
        )

    unique_domains = {s.domain for s in source_items if s.domain}
    return (
        evidence_items,
        source_items,
        len(unique_domains),
        duplicate_results_removed,
        len(filtered_unrelated_items),
        filtered_unrelated_items,
    )


def detect_contradictions(evidence: list[EvidenceItem], normalized_input: str) -> list[dict]:
    """Find genuine contradictions in evidence.

    Only flags contradictions where DIRECT negative evidence contradicts positive claims,
    NOT where impersonation warnings coexist with legitimate company profiles.
    """
    contradictions: list[dict] = []

    direct_negative = [
        e for e in evidence
        if e.relationship == EvidenceRelationship.DIRECT
        and e.category in (
            EvidenceCategory.REGULATORY_WARNING,
            EvidenceCategory.FRAUD_ALLEGATION,
            EvidenceCategory.SCAM_REPORT,
            EvidenceCategory.FRAUD_SCAM_ALLEGATION,
            EvidenceCategory.DIRECT_NEGATIVE_REPORT,
            EvidenceCategory.SCAM_FRAUD,
            EvidenceCategory.PAYMENT_FRAUD,
            EvidenceCategory.PAYMENT_REQUEST,
        )
    ]
    positive = [
        e for e in evidence
        if e.relationship in (EvidenceRelationship.POSITIVE_SIGNAL, EvidenceRelationship.POSITIVE)
        or e.category in (EvidenceCategory.VERIFICATION_SIGNAL, EvidenceCategory.POSITIVE_SIGNAL)
    ]

    if direct_negative and positive:
        contradictions.append({
            "type": "positive_vs_negative",
            "description": (
                f"Some verified sources describe '{normalized_input}' with positive or legitimate credentials, "
                f"while other independent sources contain direct fraud or regulatory allegations against the entity."
            ),
            "positive_source": {
                "title": positive[0].title,
                "url": positive[0].url,
                "snippet": positive[0].snippet[:200],
            },
            "negative_source": {
                "title": direct_negative[0].title,
                "url": direct_negative[0].url,
                "snippet": direct_negative[0].snippet[:200],
            },
        })

    payment_evidence = [
        e for e in evidence
        if e.relationship == EvidenceRelationship.DIRECT
        and e.category == EvidenceCategory.PAYMENT_REQUEST
    ]
    no_fee_evidence = [
        e for e in evidence
        if any(phrase in e.snippet.lower() for phrase in ["no fee", "100% free", "no charge", "no cost", "never ask for money"])
    ]

    if payment_evidence and no_fee_evidence:
        contradictions.append({
            "type": "payment_contradiction",
            "description": (
                f"Claims state services or placement are free with no fees, but direct applicant reports "
                f"document compulsory upfront payment requests."
            ),
            "claim_source": {
                "title": no_fee_evidence[0].title,
                "url": no_fee_evidence[0].url,
                "snippet": no_fee_evidence[0].snippet[:200],
            },
            "counter_source": {
                "title": payment_evidence[0].title,
                "url": payment_evidence[0].url,
                "snippet": payment_evidence[0].snippet[:200],
            },
        })

    return contradictions
