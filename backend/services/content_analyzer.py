"""User-content analyzer for ScamShield.

Analyzes raw user input text directly before any external search is executed.
Extracts claim-based risk signals and suspicious patterns (e.g. upfront payment demands,
guaranteed income promises, unrealistic earnings claims, urgency tactics).
"""

from __future__ import annotations

import re
from models.schemas import ContentSignal, ContentSignalCategory, EvidenceStrength


def analyze_content(text: str) -> tuple[list[ContentSignal], int]:
    """Analyze submitted text for direct risk indicators.

    Returns:
        (signals_list, content_signal_score)
    """
    clean_text = text.strip()
    lower_text = clean_text.lower()
    signals: list[ContentSignal] = []

    # Helper to extract the sentence or clause containing a match
    def extract_snippet(pattern: str) -> str:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if not match:
            return clean_text[:120]
        start = max(0, match.start() - 30)
        end = min(len(clean_text), match.end() + 40)
        snippet = clean_text[start:end].strip()
        # Clean up leading/trailing punctuation if cropped
        if start > 0:
            snippet = "..." + snippet
        if end < len(clean_text):
            snippet = snippet + "..."
        return snippet

    # 1. UPFRONT_PAYMENT
    upfront_payment_patterns = [
        r"(pay\s+(?:₹|\$|rs\.?|inr)?\s*\d+[\d,]*(?:\s*(?:registration|joining|application|security|training|processing|onboarding|kit|equipment|start)\s*(?:fee|deposit|charge|amount|money))?)",
        r"((?:registration|joining|application|security|training|processing|onboarding|kit|equipment)\s*(?:fee|deposit|charge)\s*(?:of)?\s*(?:₹|\$|rs\.?|inr)?\s*\d+[\d,]*)",
        r"\b(?:pay\s+before\s+starting|pay\s+to\s+start|send\s+money\s+first|pay\s+first|advance\s+fee|refundable\s+deposit|refundable\s+fee|processing\s+charge|deposit\s+required)\b",
    ]
    matched_upfront = False
    for pat in upfront_payment_patterns:
        m = re.search(pat, clean_text, re.IGNORECASE)
        if m:
            quote = m.group(0).strip()
            amount_match = re.search(r"(?:₹|\$|rs\.?|inr)\s*[\d,]+", quote, re.IGNORECASE)
            amt_str = f" a {amount_match.group(0)}" if amount_match else " an upfront"
            signals.append(
                ContentSignal(
                    category=ContentSignalCategory.UPFRONT_PAYMENT,
                    severity=EvidenceStrength.HIGH,
                    title="Upfront payment request",
                    description=f"The offer asks for{amt_str} registration fee or payment before starting.",
                    quote=quote,
                    risk_contribution=35,
                )
            )
            matched_upfront = True
            break

    # 2. GUARANTEED_INCOME
    guaranteed_patterns = [
        r"\b(?:guaranteed\s+(?:income|salary|profit|returns|payout|earnings)|assured\s+(?:income|salary|returns)|risk-?free\s+returns|100%\s+guaranteed|daily\s+guaranteed)\b",
    ]
    for pat in guaranteed_patterns:
        m = re.search(pat, clean_text, re.IGNORECASE)
        if m:
            quote = m.group(0).strip()
            signals.append(
                ContentSignal(
                    category=ContentSignalCategory.GUARANTEED_INCOME,
                    severity=EvidenceStrength.HIGH,
                    title="Guaranteed income claim",
                    description="The offer explicitly promises guaranteed income or returns, a common indicator of advance-fee and task scams.",
                    quote=quote,
                    risk_contribution=30,
                )
            )
            break

    # 3. UNREALISTIC_EARNINGS (e.g. high pay with no experience, or huge yields)
    has_earnings = bool(re.search(r"(?:earn|salary|make|income)\s*(?:of)?\s*(?:₹|\$|rs\.?|inr)?\s*[\d,]+(?:\s*(?:per\s+month|per\s+day|daily|monthly|weekly|p\.?m\.?))?", lower_text))
    has_no_exp = bool(re.search(r"\b(?:no\s+experience|no\s+qualification|simple\s+work|little\s+effort|anyone\s+can\s+do|without\s+investment)\b", lower_text))

    if has_earnings and has_no_exp:
        # Extract earnings clause
        m_earn = re.search(r"((?:earn|salary|make|income)\s*(?:of)?\s*(?:₹|\$|rs\.?|inr)?\s*[\d,]+(?:\s*(?:per\s+month|per\s+day|daily|monthly|weekly|p\.?m\.?))?[^.]*)", clean_text, re.IGNORECASE)
        quote = m_earn.group(0).strip() if m_earn else "Earn with no experience required"
        signals.append(
            ContentSignal(
                category=ContentSignalCategory.UNREALISTIC_EARNINGS,
                severity=EvidenceStrength.HIGH,
                title="Unrealistic earnings with no experience",
                description="The offer promises substantial earnings while requiring no experience or qualifications.",
                quote=quote,
                risk_contribution=20,
            )
        )

    # 4. JOB_SCAM_PATTERNS
    job_scam_flags = [
        r"\b(?:work\s+from\s+home|from\s+home|wfh)\b",
        r"\b(?:no\s+experience\s+required|no\s+prior\s+experience)\b",
        r"\b(?:immediate\s+joining|instant\s+hiring|direct\s+joining|no\s+interview)\b",
        r"\b(?:data\s+entry\s+job|sms\s+sending\s+job|typing\s+job|part-?time\s+mobile\s+work)\b",
    ]
    matched_flags = [re.search(p, clean_text, re.IGNORECASE) for p in job_scam_flags]
    matched_flags = [m.group(0).strip() for m in matched_flags if m]
    # If multiple job scam tropes exist and it's not already completely covered
    if len(matched_flags) >= 2 and not any(s.category == ContentSignalCategory.UNREALISTIC_EARNINGS for s in signals):
        signals.append(
            ContentSignal(
                category=ContentSignalCategory.JOB_SCAM_PATTERNS,
                severity=EvidenceStrength.MEDIUM,
                title="Common remote work recruitment pattern",
                description="Work-from-home offers with zero qualification criteria frequently target remote applicants.",
                quote=", ".join(matched_flags),
                risk_contribution=15,
            )
        )

    # 5. URGENCY_PRESSURE
    urgency_patterns = [
        r"\b(?:act\s+now|limited\s+seats|today\s+only|immediate\s+payment|last\s+chance|hurry\s+up|slots\s+filling\s+fast|offer\s+expires\s+today|within\s+24\s+hours)\b",
    ]
    for pat in urgency_patterns:
        m = re.search(pat, clean_text, re.IGNORECASE)
        if m:
            signals.append(
                ContentSignal(
                    category=ContentSignalCategory.URGENCY_PRESSURE,
                    severity=EvidenceStrength.MEDIUM,
                    title="Artificial urgency / pressure",
                    description="Employs time-pressure tactics to compel immediate payment or sign-up without time for reflection.",
                    quote=m.group(0).strip(),
                    risk_contribution=10,
                )
            )
            break

    # 6. PERSONAL_DATA_REQUEST
    data_patterns = [
        r"\b(?:send\s+otp|share\s+otp|send\s+aadhaar|send\s+pan|send\s+bank\s+details|send\s+card\s+details|share\s+password|remote\s+access|install\s+anydesk|install\s+teamviewer)\b",
    ]
    for pat in data_patterns:
        m = re.search(pat, clean_text, re.IGNORECASE)
        if m:
            signals.append(
                ContentSignal(
                    category=ContentSignalCategory.PERSONAL_DATA_REQUEST,
                    severity=EvidenceStrength.HIGH,
                    title="Request for sensitive credentials or personal data",
                    description="Asks for confidential credentials, one-time passwords, or remote access software.",
                    quote=m.group(0).strip(),
                    risk_contribution=30,
                )
            )
            break

    # 7. INVESTMENT_PATTERNS (Crypto / Doubling)
    crypto_patterns = [
        r"\b(?:double\s+your\s+money|fixed\s+daily\s+profit|risk-?free\s+investment|500%\s+daily|hourly\s+profit|guaranteed\s+crypto|passive\s+crypto\s+income)\b",
    ]
    for pat in crypto_patterns:
        m = re.search(pat, clean_text, re.IGNORECASE)
        if m:
            signals.append(
                ContentSignal(
                    category=ContentSignalCategory.INVESTMENT_PATTERNS,
                    severity=EvidenceStrength.HIGH,
                    title="High-yield / guaranteed investment scheme",
                    description="Promotes mathematically impossible or guaranteed yields on capital.",
                    quote=m.group(0).strip(),
                    risk_contribution=35,
                )
            )
            break

    # Calculate content signal score (capped at 100)
    raw_score = sum(s.risk_contribution for s in signals)
    content_signal_score = min(100, raw_score)

    return signals, content_signal_score
