"""Demo mode data provider for ScamShield hackathon presentations.

Provides realistic, clearly-labeled simulated investigations when SerpApi key is not yet configured
or when the user clicks 'Try Demo Mode'.
"""

from __future__ import annotations

from models.schemas import (
    Confidence,
    DetectedType,
    EvidenceCategory,
    EvidenceItem,
    EvidenceRelationship,
    EvidenceStrength,
    InvestigateResponse,
    QueryRecord,
    RiskIndicator,
    RiskLevel,
    SourceItem,
    SourceTrust,
)

DEMO_DATASETS: dict[str, InvestigateResponse] = {
    "apex-careers": InvestigateResponse(
        input="Apex Careers Recruitment",
        normalized_input="Apex Careers Recruitment",
        detected_type=DetectedType.JOB_OFFER,
        risk_score=68,
        overall_risk_score=68,
        content_signal_score=0,
        web_evidence_score=68,
        risk_level=RiskLevel.HIGH,
        confidence=Confidence.HIGH,
        summary=(
            "This investigation found multiple complaint-related results, upfront payment requests disguised as "
            "'equipment fees', and a direct contradiction between the company's website and external applicant reports. "
            "While not a judicial determination, these signals strongly advise against transferring funds or sharing sensitive personal data."
        ),
        indicators=[
            RiskIndicator(icon="🚩", label="Scam indicators", count=5, severity=EvidenceStrength.HIGH),
            RiskIndicator(icon="⚠️", label="Complaints", count=4, severity=EvidenceStrength.MEDIUM),
            RiskIndicator(icon="⚡", label="Contradictory claims", count=1, severity=EvidenceStrength.HIGH),
            RiskIndicator(icon="📰", label="News reports", count=2, severity=EvidenceStrength.MEDIUM),
            RiskIndicator(icon="🔍", label="Verification signals", count=1, severity=EvidenceStrength.LOW),
        ],
        evidence=[
            EvidenceItem(
                category=EvidenceCategory.PAYMENT_REQUEST,
                severity=EvidenceStrength.HIGH,
                title="Upfront Equipment & Background Check Demands",
                summary="Multiple candidate accounts report being pressured to wire $199 - $450 for home-office workstation software prior to receiving offer documents.",
                source="Consumer Career Protection Board",
                url="https://consumerprotection-demo.org/reports/apex-careers-fee-warning",
                snippet="Numerous job seekers reported receiving unsolicited employment letters from Apex Careers requiring upfront equipment deposits via non-refundable wire transfers.",
                evidence_strength=EvidenceStrength.HIGH,
                source_type=SourceTrust.HIGHER,
            ),
            EvidenceItem(
                category=EvidenceCategory.CONTRADICTORY,
                severity=EvidenceStrength.HIGH,
                title="Discrepancy on Recruitment Fees",
                summary="Company portal claims completely free hiring, but external applicants consistently report compulsory payments.",
                source="JobSeeker Transparency Network",
                url="https://jobseeker-reports-demo.com/apex-contradictions",
                snippet="Official listing claims 'Zero candidate fees', whereas six independent applicants in October documented demand letters for mandatory pre-employment certification fees.",
                evidence_strength=EvidenceStrength.HIGH,
                source_type=SourceTrust.MEDIUM,
            ),
            EvidenceItem(
                category=EvidenceCategory.COMPLAINT,
                severity=EvidenceStrength.MEDIUM,
                title="Ghosting and Non-Delivery of Promised Roles",
                summary="Victims state that once payment was transmitted, communication ceased completely.",
                source="Workplace Forum Reports",
                url="https://workplace-forum-demo.net/t/apex-careers-experience",
                snippet="Paid $250 for the remote onboarding kit. The recruiter email bounced back the next morning. Phone numbers are disconnected.",
                evidence_strength=EvidenceStrength.MEDIUM,
                source_type=SourceTrust.LOWER,
            ),
            EvidenceItem(
                category=EvidenceCategory.LEGAL_NEWS,
                severity=EvidenceStrength.MEDIUM,
                title="Advisory Warning on Remote Hiring Schemes",
                summary="Regional employment bureau issued a bulletin mentioning impersonators operating under similar trade names.",
                source="State Labor Gazette",
                url="https://statelabor-demo.gov/news/remote-work-hiring-schemes-q3",
                snippet="Officials warn of surge in fake recruitment drives mimicking domestic staffing agencies like Apex and requesting payment for telework hardware.",
                evidence_strength=EvidenceStrength.MEDIUM,
                source_type=SourceTrust.HIGHER,
            ),
            EvidenceItem(
                category=EvidenceCategory.COMPANY_VERIFICATION,
                severity=EvidenceStrength.LOW,
                title="Missing Corporate Registry Records",
                summary="No registered business entity under this exact corporate name was found in state LLC filing records.",
                source="Open Corporate Index",
                url="https://opencorporate-demo.org/search/apex-careers-recruitment",
                snippet="No active incorporation or agent of record listed in principal commercial registries matching the stated headquarters address.",
                evidence_strength=EvidenceStrength.LOW,
                source_type=SourceTrust.MEDIUM,
            ),
        ],
        sources=[
            SourceItem(
                title="Consumer Career Protection Board: Apex Careers Advisory",
                domain="consumerprotection-demo.org",
                url="https://consumerprotection-demo.org/reports/apex-careers-fee-warning",
                snippet="Multiple job seekers report advance-fee demands for remote IT and data entry positions.",
                evidence_category=EvidenceCategory.PAYMENT_REQUEST,
                evidence_strength=EvidenceStrength.HIGH,
                source_type=SourceTrust.HIGHER,
                position=1,
            ),
            SourceItem(
                title="State Labor Gazette - Warning on Remote Hiring Schemes",
                domain="statelabor-demo.gov",
                url="https://statelabor-demo.gov/news/remote-work-hiring-schemes-q3",
                snippet="State authorities identify recurring advance-fee hiring tactics targeting remote workers.",
                evidence_category=EvidenceCategory.LEGAL_NEWS,
                evidence_strength=EvidenceStrength.MEDIUM,
                source_type=SourceTrust.HIGHER,
                position=2,
            ),
            SourceItem(
                title="JobSeeker Transparency Network - Apex Careers Reviews",
                domain="jobseeker-reports-demo.com",
                url="https://jobseeker-reports-demo.com/apex-contradictions",
                snippet="Contradictions noted between official zero-fee promise and recurring upfront fee invoices.",
                evidence_category=EvidenceCategory.CONTRADICTORY,
                evidence_strength=EvidenceStrength.HIGH,
                source_type=SourceTrust.MEDIUM,
                position=3,
            ),
            SourceItem(
                title="Workplace Forum: Is Apex Careers Legitimate?",
                domain="workplace-forum-demo.net",
                url="https://workplace-forum-demo.net/t/apex-careers-experience",
                snippet="Discussion thread detailing unreturned payments and unreachable contact numbers.",
                evidence_category=EvidenceCategory.COMPLAINT,
                evidence_strength=EvidenceStrength.MEDIUM,
                source_type=SourceTrust.LOWER,
                position=4,
            ),
        ],
        queries=[
            QueryRecord(query='"Apex Careers" scam', result_count=8, status="completed"),
            QueryRecord(query='"Apex Careers" complaints', result_count=7, status="completed"),
            QueryRecord(query='"Apex Careers" recruitment payment', result_count=6, status="completed"),
            QueryRecord(query='"Apex Careers" reviews', result_count=8, status="completed"),
            QueryRecord(query='"Apex Careers" fraud fake', result_count=5, status="completed"),
            QueryRecord(query='"Apex Careers" news', result_count=3, status="completed"),
        ],
        search_count=6,
        unique_sources=4,
        duplicate_results_removed=5,
        contradictions=[
            {
                "topic": "Registration / Equipment Fees",
                "claimed_by_subject": "Official listing guarantees 100% free candidate registration, placement assistance, and company-supplied hardware.",
                "contradicted_by": "Independent applicant reports and consumer warnings document compulsory upfront fees of $199-$450 for home workstations.",
                "source_claimed": "Apex Careers Portal (Official Listing)",
                "source_evidence": "Consumer Career Protection Board & JobSeeker Network",
            }
        ],
        is_demo=True,
    ),
    "novayield-crypto": InvestigateResponse(
        input="NovaYield Crypto Yield Fund",
        normalized_input="NovaYield Crypto Yield Fund",
        detected_type=DetectedType.INVESTMENT,
        risk_score=84,
        overall_risk_score=84,
        content_signal_score=0,
        web_evidence_score=84,
        risk_level=RiskLevel.VERY_HIGH,
        confidence=Confidence.HIGH,
        summary=(
            "Severe risk indicators detected. The investigation found an official regulator investor alert, "
            "guarantees of impossible 4% daily risk-free returns, multi-tier pyramid referral structures, "
            "and dozens of complaints regarding frozen withdrawal accounts."
        ),
        indicators=[
            RiskIndicator(icon="🚩", label="Regulatory alert", count=2, severity=EvidenceStrength.HIGH),
            RiskIndicator(icon="⚠️", label="Frozen funds complaints", count=8, severity=EvidenceStrength.HIGH),
            RiskIndicator(icon="⚡", label="Contradictory claims", count=1, severity=EvidenceStrength.HIGH),
            RiskIndicator(icon="📰", label="Financial warnings", count=3, severity=EvidenceStrength.MEDIUM),
        ],
        evidence=[
            EvidenceItem(
                category=EvidenceCategory.REGULATORY_WARNING,
                severity=EvidenceStrength.HIGH,
                title="Financial Services Authority Investor Alert",
                summary="Listed on national investor caution list for providing unauthorized financial products.",
                source="Financial Markets Authority",
                url="https://fma-demo.gov/investor-alerts/novayield-fund",
                snippet="NovaYield is not authorized, registered, or insured to solicit investments or custody consumer assets.",
                evidence_strength=EvidenceStrength.HIGH,
                source_type=SourceTrust.HIGHER,
            ),
            EvidenceItem(
                category=EvidenceCategory.SCAM_FRAUD,
                severity=EvidenceStrength.HIGH,
                title="Unrealistic Guaranteed Yield Claims",
                summary="Promotes 'guaranteed 4% daily yield without capital risk', a hallmark indicator of Ponzi schemes.",
                source="Crypto Audit Watch",
                url="https://cryptoaudit-demo.org/reports/novayield-ponzi-indicators",
                snippet="Mathematical models confirm promised returns are unsustainable and funded solely through continuous new depositor inflows.",
                evidence_strength=EvidenceStrength.HIGH,
                source_type=SourceTrust.MEDIUM,
            ),
            EvidenceItem(
                category=EvidenceCategory.COMPLAINT,
                severity=EvidenceStrength.HIGH,
                title="Widespread Withdrawal Lockouts",
                summary="Users report that requesting withdrawals triggers demands for additional 'tax clearance deposits'.",
                source="Investor Trust Forum",
                url="https://investortrust-demo.com/novayield-frozen-funds",
                snippet="Account balances display healthy profits, but withdrawals are locked unless an additional 20% release fee is sent.",
                evidence_strength=EvidenceStrength.HIGH,
                source_type=SourceTrust.LOWER,
            ),
        ],
        sources=[
            SourceItem(
                title="Financial Markets Authority - Investor Blacklist Notice",
                domain="fma-demo.gov",
                url="https://fma-demo.gov/investor-alerts/novayield-fund",
                snippet="Public caution against unlicensed investment solicitation.",
                evidence_category=EvidenceCategory.REGULATORY_WARNING,
                evidence_strength=EvidenceStrength.HIGH,
                source_type=SourceTrust.HIGHER,
                position=1,
            ),
            SourceItem(
                title="Crypto Audit Watch - Yield Investigation",
                domain="cryptoaudit-demo.org",
                url="https://cryptoaudit-demo.org/reports/novayield-ponzi-indicators",
                snippet="Analysis of unrealistic returns and multi-tiered referral mechanisms.",
                evidence_category=EvidenceCategory.SCAM_FRAUD,
                evidence_strength=EvidenceStrength.HIGH,
                source_type=SourceTrust.MEDIUM,
                position=2,
            ),
        ],
        queries=[
            QueryRecord(query='"NovaYield Crypto" scam', result_count=9, status="completed"),
            QueryRecord(query='"NovaYield Crypto" fraud warning', result_count=8, status="completed"),
            QueryRecord(query='"NovaYield Crypto" withdrawal complaints', result_count=7, status="completed"),
            QueryRecord(query='"NovaYield" investment news', result_count=4, status="completed"),
        ],
        search_count=4,
        unique_sources=4,
        duplicate_results_removed=6,
        contradictions=[
            {
                "topic": "Regulatory License & Custody",
                "claimed_by_subject": "Platform website states: 'Fully licensed, audited and insured under tier-1 securities regulators.'",
                "contradicted_by": "Official regulator public registers confirm the entity has zero licenses and appears on unauthorized caution lists.",
                "source_claimed": "NovaYield Marketing Page",
                "source_evidence": "Financial Markets Authority Registry",
            }
        ],
        is_demo=True,
    ),
    "veritas-tech": InvestigateResponse(
        input="Veritas Enterprise Systems",
        normalized_input="Veritas Enterprise Systems",
        detected_type=DetectedType.COMPANY,
        risk_score=14,
        overall_risk_score=14,
        content_signal_score=0,
        web_evidence_score=14,
        risk_level=RiskLevel.LOW,
        confidence=Confidence.HIGH,
        summary=(
            "Investigation reveals a strongly established corporate footprint with verified commercial registrations, "
            "positive customer case studies across reputable media, active enterprise security certifications, "
            "and negligible complaint signals."
        ),
        indicators=[
            RiskIndicator(icon="🔍", label="Verification signals", count=6, severity=EvidenceStrength.LOW),
            RiskIndicator(icon="📰", label="Legitimate news coverage", count=4, severity=EvidenceStrength.LOW),
            RiskIndicator(icon="⚠️", label="Isolated complaints", count=1, severity=EvidenceStrength.LOW),
        ],
        evidence=[
            EvidenceItem(
                category=EvidenceCategory.COMPANY_VERIFICATION,
                severity=EvidenceStrength.LOW,
                title="Verified Active Corporate Incorporation",
                summary="Incorporated since 2014 with transparent executive leadership and publicly registered physical offices.",
                source="National Corporation Directory",
                url="https://corpregistry-demo.gov/records/veritas-enterprise-systems",
                snippet="Veritas Enterprise Systems LLC is in good standing with confirmed business filings dating back over a decade.",
                evidence_strength=EvidenceStrength.LOW,
                source_type=SourceTrust.HIGHER,
            ),
            EvidenceItem(
                category=EvidenceCategory.POSITIVE_SIGNAL,
                severity=EvidenceStrength.LOW,
                title="Established Industry Partnerships & Accreditation",
                summary="Recognized partner with major cloud providers with audited SOC 2 compliance reports.",
                source="Enterprise Tech Review",
                url="https://enterprisetech-demo.com/leaders/veritas-review-2025",
                snippet="Veritas maintains verified enterprise agreements, documented security certifications, and high vendor reliability scores.",
                evidence_strength=EvidenceStrength.LOW,
                source_type=SourceTrust.MEDIUM,
            ),
        ],
        sources=[
            SourceItem(
                title="National Corporation Directory - Veritas Record",
                domain="corpregistry-demo.gov",
                url="https://corpregistry-demo.gov/records/veritas-enterprise-systems",
                snippet="Verified public corporate record and annual filing status.",
                evidence_category=EvidenceCategory.COMPANY_VERIFICATION,
                evidence_strength=EvidenceStrength.LOW,
                source_type=SourceTrust.HIGHER,
                position=1,
            ),
            SourceItem(
                title="Enterprise Tech Review - Technology Vendor Assessment",
                domain="enterprisetech-demo.com",
                url="https://enterprisetech-demo.com/leaders/veritas-review-2025",
                snippet="Independent assessment covering customer satisfaction, SLAs, and security controls.",
                evidence_category=EvidenceCategory.POSITIVE_SIGNAL,
                evidence_strength=EvidenceStrength.LOW,
                source_type=SourceTrust.MEDIUM,
                position=2,
            ),
        ],
        queries=[
            QueryRecord(query='"Veritas Enterprise Systems" scam', result_count=1, status="completed"),
            QueryRecord(query='"Veritas Enterprise Systems" complaints reviews', result_count=5, status="completed"),
            QueryRecord(query='"Veritas Enterprise Systems" company registration', result_count=4, status="completed"),
        ],
        search_count=3,
        unique_sources=2,
        duplicate_results_removed=3,
        contradictions=[],
        is_demo=True,
    ),
}


def get_demo_investigation(query_or_key: str) -> InvestigateResponse:
    """Return a demo investigation response for demonstration / hackathon purposes."""
    cleaned = query_or_key.strip().lower()

    if "crypto" in cleaned or "yield" in cleaned or "invest" in cleaned:
        return DEMO_DATASETS["novayield-crypto"]
    elif "veritas" in cleaned or "safe" in cleaned or "software" in cleaned:
        return DEMO_DATASETS["veritas-tech"]
    else:
        # Default showcase example: Apex Careers (shows contradictory claims & high risk)
        return DEMO_DATASETS["apex-careers"]
