"""Risk engine – Contextual, evidence-relationship-based risk scoring.

Calculates a 0-100 evidence-based risk score with source independence,
domain-level caps, and dynamic contextual explanations that distinguish
between investigated entities and the impersonation attacks targeting them.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from urllib.parse import urlparse

from models.schemas import (
    Confidence,
    ContentSignal,
    ContentSignalCategory,
    EvidenceCategory,
    EvidenceItem,
    EvidenceRelationship,
    EvidenceStrength,
    RiskIndicator,
    RiskLevel,
    SourceTrust,
)

# ── Base Weights by Category (Applies ONLY to DIRECT / NEGATIVE_MENTION) ────────

_DIRECT_CATEGORY_BASE: dict[EvidenceCategory, int] = {
    EvidenceCategory.REGULATORY_WARNING:        18,
    EvidenceCategory.FRAUD_ALLEGATION:          16,
    EvidenceCategory.SCAM_REPORT:               16,
    EvidenceCategory.FRAUD_SCAM_ALLEGATION:     16,
    EvidenceCategory.DIRECT_NEGATIVE_REPORT:    16,
    EvidenceCategory.PAYMENT_FRAUD:             16,
    EvidenceCategory.LEGAL_NEWS:                16,
    EvidenceCategory.PAYMENT_REQUEST:           16,
    EvidenceCategory.SCAM_FRAUD:                15,
    EvidenceCategory.DIRECT_COMPLAINT:           3,  # Other legitimate complaints - low impact
    EvidenceCategory.COMPLAINT:                  3,
    EvidenceCategory.NEGATIVE_REVIEW:            2,
    EvidenceCategory.SECURITY_REPORT:            0,  # Technical security findings: 0 scam points
    EvidenceCategory.ABUSE_REPORT:               0,  # Abuse reports: 0 scam points
    EvidenceCategory.CONSUMER_DISSATISFACTION:   0,  # Ordinary dissatisfaction: 0 scam risk points!
    EvidenceCategory.MISSING_INFO:               3,
    EvidenceCategory.IMPERSONATION_TARGET:       0,
    EvidenceCategory.FAKE_IMPERSONATION:         0,
    EvidenceCategory.GENERAL_ADVISORY:           0,
    EvidenceCategory.COMPANY_VERIFICATION:       0,
    EvidenceCategory.VERIFICATION_SIGNAL:        0,
    EvidenceCategory.POSITIVE_SIGNAL:            0,
    EvidenceCategory.NEUTRAL_PROFILE:            0,
    EvidenceCategory.NEUTRAL:                    0,
    EvidenceCategory.UNRELATED:                  0,
    EvidenceCategory.CONTRADICTORY:              0,
}

_SOURCE_TYPE_MULTIPLIER: dict[str, float] = {
    "Government / Regulatory": 1.4,
    "News": 1.2,
    "Review": 1.0,
    "Company": 1.0,
    "Blog / Forum": 0.6,
    "Other": 0.6,
}

_TRUST_MULTIPLIER: dict[SourceTrust, float] = {
    SourceTrust.HIGHER: 1.3,
    SourceTrust.MEDIUM: 1.0,
    SourceTrust.LOWER: 0.6,
    SourceTrust.UNKNOWN: 0.5,
}

MAX_POINTS_PER_DOMAIN = 16


def _extract_domain(url: str) -> str:
    try:
        parsed = urlparse(url)
        host = parsed.netloc or parsed.path.split("/")[0]
        return host.split(":")[0].lower().removeprefix("www.")
    except Exception:
        return "unknown"


# ── Scoring ─────────────────────────────────────────────────────────────────────

def calculate_risk(
    evidence: list[EvidenceItem],
    contradictions: list[dict],
    unique_sources: int = 0,
    content_signal_score: int = 0,
) -> tuple[int, int, int, RiskLevel, Confidence]:
    """Calculate overall risk score, content signal score, web evidence score, risk level, and confidence.

    Rules:
    - IMPERSONATION_TARGET items contribute 0 points against the entity.
    - CONSUMER_DISSATISFACTION items contribute 0 points to scam risk.
    - SECURITY_REPORT and ABUSE_REPORT contribute 0 points to scam risk.
    - GENERAL_ADVISORY / GENERAL_WARNING items contribute 0 points against the entity.
    - POSITIVE_SIGNAL, VERIFICATION_SIGNAL, NEUTRAL_PROFILE, NEUTRAL, UNRELATED items contribute 0 points.
    - Only direct fraud, scam reports, payment fraud, and actionable negative reports contribute significant risk.
    - Caps points contributed by any single publishing domain to prevent duplicate inflation.
    - Requires multiple independent domains to reach HIGH or VERY_HIGH risk from web evidence.
    - Blends content_signal_score and web_evidence_score transparently.
    """
    # 1. Assign points to each evidence item and group by domain
    domain_direct_points: dict[str, float] = defaultdict(float)
    negative_domains: set[str] = set()
    direct_evidence_count = 0
    negative_mention_count = 0
    impersonation_count = 0
    positive_count = 0

    for item in evidence:
        domain = _extract_domain(item.url)

        if item.relationship == EvidenceRelationship.IMPERSONATION_TARGET or item.category == EvidenceCategory.IMPERSONATION_TARGET:
            item.risk_contribution = 0
            impersonation_count += 1
            continue

        if item.category in (
            EvidenceCategory.CONSUMER_DISSATISFACTION,
            EvidenceCategory.SECURITY_REPORT,
            EvidenceCategory.ABUSE_REPORT,
        ) or item.relationship == EvidenceRelationship.SECURITY_ABUSE or getattr(item, "complaint_type", None) in (
            "consumer_dissatisfaction",
            "security_report",
            "abuse_report",
        ):
            item.risk_contribution = 0
            continue

        if item.relationship in (EvidenceRelationship.GENERAL_ADVISORY, EvidenceRelationship.GENERAL_WARNING, EvidenceRelationship.UNRELATED, EvidenceRelationship.NEUTRAL) or item.category in (EvidenceCategory.GENERAL_ADVISORY, EvidenceCategory.NEUTRAL_PROFILE, EvidenceCategory.NEUTRAL, EvidenceCategory.UNRELATED):
            item.risk_contribution = 0
            continue

        if item.relationship in (EvidenceRelationship.POSITIVE_SIGNAL, EvidenceRelationship.POSITIVE) or item.category in (EvidenceCategory.VERIFICATION_SIGNAL, EvidenceCategory.POSITIVE_SIGNAL):
            item.risk_contribution = 0
            positive_count += 1
            continue

        mult = _SOURCE_TYPE_MULTIPLIER.get(item.source_type, _TRUST_MULTIPLIER.get(item.source_trust, 0.7))

        # DIRECT: Entity is specifically accused or penalized
        if item.relationship == EvidenceRelationship.DIRECT:
            base = _DIRECT_CATEGORY_BASE.get(item.category, 8)
            points = round(base * mult)
            item.risk_contribution = points
            domain_direct_points[domain] += points
            negative_domains.add(domain)
            direct_evidence_count += 1
            continue

        # NEGATIVE_MENTION: General complaints or inquiries about entity
        if item.relationship == EvidenceRelationship.NEGATIVE_MENTION:
            base = round(_DIRECT_CATEGORY_BASE.get(item.category, 6) * 0.5)
            points = max(1, round(base * mult))
            item.risk_contribution = points
            domain_direct_points[domain] += points
            negative_domains.add(domain)
            negative_mention_count += 1
            continue

    # 2. Accumulate risk with per-domain cap
    raw_score = 0.0
    for dom, pts in domain_direct_points.items():
        raw_score += min(pts, MAX_POINTS_PER_DOMAIN)

    # 3. Add contradiction penalty only if direct adverse evidence exists
    if contradictions and direct_evidence_count > 0:
        raw_score += len(contradictions) * 8

    # 4. Source Independence constraints for web evidence
    independent_negative_count = len(negative_domains)

    if independent_negative_count == 0:
        # No direct negative evidence against entity!
        web_evidence_score = 0
    elif independent_negative_count == 1:
        # Only one domain reports negative claims -> Cap at MODERATE (max 32)
        web_evidence_score = min(int(raw_score), 32)
    elif independent_negative_count == 2:
        # Two independent domains -> Cap at 65
        web_evidence_score = min(int(raw_score), 65)
    else:
        # 3 or more independent domains -> Can reach high/very high
        web_evidence_score = max(0, min(100, int(raw_score)))

    # 5. Combine content signals and web evidence transparently
    if content_signal_score > 0 and web_evidence_score > 0:
        # Both layers contribute: content claims corroborated by web evidence
        combined = round(content_signal_score * 0.7 + web_evidence_score * 0.5)
        overall_score = max(0, min(100, combined))
    elif content_signal_score > 0:
        # Content signals only: e.g. upfront fee, guaranteed income in submitted text
        overall_score = max(0, min(100, round(content_signal_score * 0.85)))
    else:
        # Web evidence only (e.g. searching a company or domain name)
        overall_score = web_evidence_score

    # 6. Determine Confidence
    if independent_negative_count >= 2 or unique_sources >= 5 or content_signal_score >= 50:
        confidence = Confidence.HIGH
    elif (unique_sources <= 1 and len(evidence) <= 2) and content_signal_score == 0:
        confidence = Confidence.LOW
    else:
        confidence = Confidence.MEDIUM

    # 7. Map to Risk Level
    if overall_score == 0:
        if direct_evidence_count == 0 and negative_mention_count == 0 and content_signal_score == 0:
            if impersonation_count > 0 or positive_count > 0 or unique_sources >= 3:
                level = RiskLevel.LOW
            else:
                level = RiskLevel.INSUFFICIENT
        else:
            level = RiskLevel.LOW
    elif overall_score < 25:
        level = RiskLevel.LOW
    elif overall_score < 50:
        level = RiskLevel.MODERATE
    elif overall_score < 75:
        level = RiskLevel.HIGH
    else:
        level = RiskLevel.VERY_HIGH

    return overall_score, content_signal_score, web_evidence_score, level, confidence


# ── Indicators ──────────────────────────────────────────────────────────────────

def build_indicators(evidence: list[EvidenceItem], contradictions: list[dict]) -> list[RiskIndicator]:
    """Build informative indicator badges reflecting exact relationships."""
    direct_scam = sum(
        1 for e in evidence
        if e.relationship == EvidenceRelationship.DIRECT
        and e.category in (
            EvidenceCategory.FRAUD_ALLEGATION,
            EvidenceCategory.SCAM_REPORT,
            EvidenceCategory.FRAUD_SCAM_ALLEGATION,
            EvidenceCategory.DIRECT_NEGATIVE_REPORT,
            EvidenceCategory.SCAM_FRAUD,
            EvidenceCategory.LEGAL_NEWS,
        )
    )
    impersonation = sum(
        1 for e in evidence
        if e.relationship == EvidenceRelationship.IMPERSONATION_TARGET
        or e.category in (EvidenceCategory.IMPERSONATION_TARGET, EvidenceCategory.FAKE_IMPERSONATION)
    )
    payments = sum(
        1 for e in evidence
        if e.relationship == EvidenceRelationship.DIRECT
        and e.category in (EvidenceCategory.PAYMENT_FRAUD, EvidenceCategory.PAYMENT_REQUEST)
    )
    regulatory_direct = sum(
        1 for e in evidence
        if e.relationship == EvidenceRelationship.DIRECT
        and e.category == EvidenceCategory.REGULATORY_WARNING
    )
    security_abuse = sum(
        1 for e in evidence
        if e.relationship == EvidenceRelationship.SECURITY_ABUSE
        or e.category in (EvidenceCategory.SECURITY_REPORT, EvidenceCategory.ABUSE_REPORT)
        or getattr(e, "complaint_type", None) in ("security_report", "abuse_report")
    )
    dissatisfaction = sum(
        1 for e in evidence
        if e.category == EvidenceCategory.CONSUMER_DISSATISFACTION
        or getattr(e, "complaint_type", None) == "consumer_dissatisfaction"
    )
    other_complaints = sum(
        1 for e in evidence
        if e.relationship in (EvidenceRelationship.DIRECT, EvidenceRelationship.NEGATIVE_MENTION)
        and e.category in (EvidenceCategory.DIRECT_COMPLAINT, EvidenceCategory.COMPLAINT, EvidenceCategory.NEGATIVE_REVIEW)
        and e.category not in (EvidenceCategory.CONSUMER_DISSATISFACTION, EvidenceCategory.SECURITY_REPORT, EvidenceCategory.ABUSE_REPORT)
        and getattr(e, "complaint_type", None) not in ("consumer_dissatisfaction", "security_report", "abuse_report")
    )
    general_warnings = sum(
        1 for e in evidence
        if e.relationship in (EvidenceRelationship.GENERAL_ADVISORY, EvidenceRelationship.GENERAL_WARNING)
        or e.category == EvidenceCategory.GENERAL_ADVISORY
    )
    positive = sum(
        1 for e in evidence
        if e.relationship in (EvidenceRelationship.POSITIVE_SIGNAL, EvidenceRelationship.POSITIVE)
        or e.category in (EvidenceCategory.VERIFICATION_SIGNAL, EvidenceCategory.POSITIVE_SIGNAL, EvidenceCategory.COMPANY_VERIFICATION, EvidenceCategory.NEUTRAL_PROFILE)
    )

    indicators: list[RiskIndicator] = []

    if direct_scam > 0:
        indicators.append(RiskIndicator(
            icon="🚩",
            label="Fraud / adverse reports",
            count=direct_scam,
            severity=EvidenceStrength.HIGH,
        ))

    if impersonation > 0:
        indicators.append(RiskIndicator(
            icon="🛡️",
            label="Impersonation targets",
            count=impersonation,
            severity=EvidenceStrength.HIGH,
        ))

    if payments > 0:
        indicators.append(RiskIndicator(
            icon="💳",
            label="Payment fraud / upfront fees",
            count=payments,
            severity=EvidenceStrength.HIGH,
        ))

    if regulatory_direct > 0:
        indicators.append(RiskIndicator(
            icon="🏛️",
            label="Regulatory enforcement",
            count=regulatory_direct,
            severity=EvidenceStrength.HIGH,
        ))

    if security_abuse > 0:
        indicators.append(RiskIndicator(
            icon="🔒",
            label="Security & abuse reports",
            count=security_abuse,
            severity=EvidenceStrength.LOW,
        ))

    if dissatisfaction > 0:
        indicators.append(RiskIndicator(
            icon="💬",
            label="Consumer dissatisfaction",
            count=dissatisfaction,
            severity=EvidenceStrength.LOW,
        ))

    if other_complaints > 0:
        indicators.append(RiskIndicator(
            icon="⚠️",
            label="Direct complaints",
            count=other_complaints,
            severity=EvidenceStrength.LOW,
        ))

    if general_warnings > 0:
        indicators.append(RiskIndicator(
            icon="ℹ️",
            label="General advisories",
            count=general_warnings,
            severity=EvidenceStrength.LOW,
        ))

    if positive > 0:
        indicators.append(RiskIndicator(
            icon="✅",
            label="Verification signals",
            count=positive,
            severity=EvidenceStrength.LOW,
        ))

    if contradictions:
        indicators.append(RiskIndicator(
            icon="⚡",
            label="Contradictory claims",
            count=len(contradictions),
            severity=EvidenceStrength.HIGH,
        ))

    return indicators


# ── Summary ─────────────────────────────────────────────────────────────────────

def generate_summary(
    normalized_input: str,
    risk_level: RiskLevel,
    evidence: list[EvidenceItem],
    contradictions: list[dict],
    confidence: Confidence,
    unique_sources: int = 0,
    content_signals: list[ContentSignal] | None = None,
    content_signal_score: int = 0,
    web_evidence_score: int = 0,
) -> str:
    """Generate a dynamic, evidence-grounded explanation based strictly on actual findings.
    
    Clearly distinguishes signals found directly in user content from external web evidence.
    Never infers that a domain is newly registered or has a minimal online footprint
    without explicit, verified evidence.
    """
    total = len(evidence)
    impersonation_items = [
        e for e in evidence
        if e.relationship == EvidenceRelationship.IMPERSONATION_TARGET
        or e.category in (EvidenceCategory.IMPERSONATION_TARGET, EvidenceCategory.FAKE_IMPERSONATION)
    ]
    direct_adverse_items = [
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
            EvidenceCategory.LEGAL_NEWS,
        )
    ]
    security_abuse_items = [
        e for e in evidence
        if e.relationship == EvidenceRelationship.SECURITY_ABUSE
        or e.category in (EvidenceCategory.SECURITY_REPORT, EvidenceCategory.ABUSE_REPORT)
        or getattr(e, "complaint_type", None) in ("security_report", "abuse_report")
    ]
    dissatisfaction_items = [
        e for e in evidence
        if e.category == EvidenceCategory.CONSUMER_DISSATISFACTION
        or getattr(e, "complaint_type", None) == "consumer_dissatisfaction"
    ]
    other_complaint_items = [
        e for e in evidence
        if (e.category in (EvidenceCategory.DIRECT_COMPLAINT, EvidenceCategory.COMPLAINT, EvidenceCategory.NEGATIVE_REVIEW)
            or (e.relationship in (EvidenceRelationship.DIRECT, EvidenceRelationship.NEGATIVE_MENTION) and e not in direct_adverse_items))
        and e not in dissatisfaction_items
        and e not in security_abuse_items
    ]
    general_items = [
        e for e in evidence
        if e.relationship in (EvidenceRelationship.GENERAL_ADVISORY, EvidenceRelationship.GENERAL_WARNING)
        or e.category == EvidenceCategory.GENERAL_ADVISORY
    ]
    positive_items = [
        e for e in evidence
        if e.relationship in (EvidenceRelationship.POSITIVE_SIGNAL, EvidenceRelationship.POSITIVE)
        or e.category in (EvidenceCategory.VERIFICATION_SIGNAL, EvidenceCategory.POSITIVE_SIGNAL, EvidenceCategory.COMPANY_VERIFICATION, EvidenceCategory.NEUTRAL_PROFILE)
    ]

    # Scenario 0: Submitted content contains high-risk claim signals
    if content_signals:
        signal_descriptions: list[str] = []
        for s in content_signals:
            if s.category == ContentSignalCategory.UPFRONT_PAYMENT:
                signal_descriptions.append("an upfront payment or registration fee request")
            elif s.category == ContentSignalCategory.GUARANTEED_INCOME:
                signal_descriptions.append("a guaranteed income or assured return claim")
            elif s.category == ContentSignalCategory.UNREALISTIC_EARNINGS:
                signal_descriptions.append("an unrealistic earnings claim requiring no prior experience")
            elif s.category == ContentSignalCategory.JOB_SCAM_PATTERNS:
                signal_descriptions.append("remote task recruitment patterns")
            elif s.category == ContentSignalCategory.URGENCY_PRESSURE:
                signal_descriptions.append("artificial urgency pressure tactics")
            elif s.category == ContentSignalCategory.PERSONAL_DATA_REQUEST:
                signal_descriptions.append("a request for sensitive credentials or personal data")
            elif s.category == ContentSignalCategory.INVESTMENT_PATTERNS:
                signal_descriptions.append("high-yield investment doubling promises")
            else:
                signal_descriptions.append(s.title.lower())

        seen_desc = set()
        unique_descs = [d for d in signal_descriptions if not (d in seen_desc or seen_desc.add(d))]

        if len(unique_descs) == 1:
            desc_phrase = unique_descs[0]
        elif len(unique_descs) == 2:
            desc_phrase = f"{unique_descs[0]} and {unique_descs[1]}"
        else:
            desc_phrase = f"{', '.join(unique_descs[:-1])}, and {unique_descs[-1]}"

        content_part = (
            f"The submitted offer contains {len(content_signals)} risk indicator(s) directly within the text, "
            f"including {desc_phrase}. These indicators warrant heightened caution as advance-fee and task "
            f"solicitations frequently present these characteristics, though they do not by themselves independently establish fraud."
        )

        if len(direct_adverse_items) > 0:
            web_part = (
                f"External web searches identified {len(direct_adverse_items)} direct adverse report(s) "
                f"corroborating these concerns across independent sources."
            )
        elif len(general_items) > 0:
            web_part = (
                f"External web searches across {unique_sources} source(s) retrieved general advisories on employment "
                f"and payment security rather than direct complaints filed against a specific registered entity."
            )
        elif total == 0:
            web_part = (
                f"External web searches did not locate independent public records specifically corroborating or refuting this offer text."
            )
        else:
            web_part = (
                f"External web searches across {unique_sources} source(s) did not identify direct regulatory actions or confirmed scam reports regarding this specific offer."
            )

        conclusion = (
            "Review the external web evidence separately from the claims identified in the submitted content before taking action or sending money."
        )

        return f"{content_part} {web_part} {conclusion}"

    # Scenario A: Impersonation Target (e.g. Microsoft, PayPal, major brand)
    # The entity has impersonation warnings, but 0 direct fraud allegations
    if len(impersonation_items) > 0 and len(direct_adverse_items) == 0 and len(other_complaint_items) <= 1:
        dissatisfaction_note = ""
        if len(dissatisfaction_items) > 0:
            dissatisfaction_note = (
                f" Search results also included {len(dissatisfaction_items)} mention(s) of ordinary customer service or "
                f"technical dissatisfaction, which represent standard consumer feedback rather than scam risk."
            )
        return (
            f"ScamShield analysed {total} search result(s) from {unique_sources} independent source(s) regarding '{normalized_input}'. "
            f"The investigation found {len(impersonation_items)} source(s) discussing scams where attackers, fraudsters, or fake tech support "
            f"callers impersonate '{normalized_input}'. These findings indicate that '{normalized_input}' is a frequent impersonation target, "
            f"rather than a fraudulent actor itself.{dissatisfaction_note} No credible direct adverse evidence or regulatory actions against '{normalized_input}' were identified."
        )

    # Scenario B: Direct adverse evidence (real scam or penalized entity)
    if len(direct_adverse_items) > 0:
        cat_mentions = set()
        for e in direct_adverse_items:
            if e.category in (EvidenceCategory.PAYMENT_FRAUD, EvidenceCategory.PAYMENT_REQUEST):
                cat_mentions.add("compulsory upfront payment requests or payment deception")
            elif e.category == EvidenceCategory.REGULATORY_WARNING:
                cat_mentions.add("regulatory enforcement warnings from official authorities")
            elif e.category in (EvidenceCategory.FRAUD_SCAM_ALLEGATION, EvidenceCategory.DIRECT_NEGATIVE_REPORT, EvidenceCategory.SCAM_FRAUD):
                cat_mentions.add("direct scam and fraud allegations")
            else:
                cat_mentions.add("direct legal or investigative reports")

        cats_str = ", ".join(cat_mentions)
        contradiction_note = (
            f" In addition, {len(contradictions)} contradiction(s) were identified between promotional claims and external reports."
            if contradictions else ""
        )
        return (
            f"ScamShield identified {len(direct_adverse_items)} direct concern(s) regarding '{normalized_input}' across independent web sources, "
            f"including {cats_str}.{contradiction_note} Multiple independent sources directly associate '{normalized_input}' with "
            f"questionable practices. Exercise extreme caution before transferring funds or sharing confidential credentials."
        )

    # Scenario C1: Consumer dissatisfaction only (ordinary customer service/product feedback)
    if len(dissatisfaction_items) > 0 and len(direct_adverse_items) == 0 and len(other_complaint_items) == 0:
        return (
            f"This investigation found {len(dissatisfaction_items)} report(s) reflecting customer service or product dissatisfaction regarding '{normalized_input}'. "
            f"These represent ordinary consumer feedback (such as technical support, software performance, or refund inquiries) rather than fraud or scam activity. "
            f"No direct scam reports, upfront fee demands, or regulatory enforcement actions against '{normalized_input}' were identified."
        )

    # Scenario C2: Other complaints
    if len(other_complaint_items) > 0:
        return (
            f"This investigation found {len(other_complaint_items)} consumer complaint(s) or negative review(s) concerning '{normalized_input}'. "
            f"While there is no record of official regulatory sanctions or direct advance-fee fraud, customer feedback suggests recurring dissatisfaction. "
            f"Review individual sources below to evaluate specific concerns."
        )

    # Scenario C3: Security or abuse reports only (technical DNS, SSL, configuration, registrar abuse without fraud)
    if len(security_abuse_items) > 0 and len(direct_adverse_items) == 0:
        return (
            f"ScamShield identified {len(security_abuse_items)} technical security or abuse report(s) regarding '{normalized_input}'. "
            f"These findings (such as DNS configuration, certificate, or network administration records) reflect technical and security administration "
            f"rather than evidence of deceptive consumer fraud. No direct scam allegations, advance-fee schemes, or regulatory enforcement actions were identified."
        )

    # Scenario D: Official positive verification signals
    if len(positive_items) > 0:
        return (
            f"ScamShield verified official and positive records for '{normalized_input}' across {unique_sources} independent source(s). "
            f"No direct scam reports, upfront fee complaints, or regulatory enforcement actions against '{normalized_input}' were identified."
        )

    # Scenario E: Results were primarily general advisories rather than evidence directly concerning this entity
    if len(general_items) > 0:
        return (
            f"The investigation did not find enough direct, relevant evidence to make a conclusive assessment regarding '{normalized_input}'. "
            f"The available results were primarily general advisories and consumer security guides rather than evidence directly concerning this entity. "
            f"No direct adverse reports or official regulatory enforcement actions targeting '{normalized_input}' were identified."
        )

    # Scenario F: Zero search results found
    if total == 0:
        return (
            f"The investigation did not locate relevant public search records or direct evidence concerning '{normalized_input}'. "
            f"Without public verification records or direct reports, a conclusive evidence-based risk assessment cannot be established. "
            f"Exercise standard diligence when interacting with unfamiliar entities."
        )

    # Scenario G: Search results returned, but neutral or unrelated mentions only
    return (
        f"The investigation did not find enough direct, relevant evidence to make a conclusive assessment regarding '{normalized_input}'. "
        f"The retrieved search results did not contain direct adverse reports, regulatory sanctions, or confirmed scam patterns concerning this entity."
    )
