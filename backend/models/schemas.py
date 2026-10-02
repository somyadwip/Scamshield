"""Pydantic schemas for ScamShield API."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── Enums ───────────────────────────────────────────────────────────────────────

class InputCategory(str, Enum):
    AUTO = "auto"
    WEBSITE = "website"
    COMPANY = "company"
    JOB_OFFER = "job_offer"
    SHOPPING = "shopping"
    INVESTMENT = "investment"
    COURSE = "course"
    OTHER = "other"


class DetectedType(str, Enum):
    URL = "url"
    COMPANY = "company"
    JOB_OFFER = "job_offer"
    SHOPPING = "shopping"
    INVESTMENT = "investment"
    COURSE = "course"
    SUSPICIOUS_OFFER = "suspicious_offer"
    GENERAL = "general"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    INSUFFICIENT = "INSUFFICIENT"


class EvidenceStrength(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ContentSignalCategory(str, Enum):
    UPFRONT_PAYMENT = "upfront_payment"
    GUARANTEED_INCOME = "guaranteed_income"
    UNREALISTIC_EARNINGS = "unrealistic_earnings"
    JOB_SCAM_PATTERNS = "job_scam_patterns"
    URGENCY_PRESSURE = "urgency_pressure"
    PERSONAL_DATA_REQUEST = "personal_data_request"
    INVESTMENT_PATTERNS = "investment_patterns"


class ContentSignal(BaseModel):
    category: ContentSignalCategory
    severity: EvidenceStrength
    title: str
    description: str
    quote: str
    risk_contribution: int = 0


class EvidenceCategory(str, Enum):
    # Core 12 categories
    FRAUD_ALLEGATION = "fraud_allegation"
    SCAM_REPORT = "scam_report"
    SECURITY_REPORT = "security_report"
    ABUSE_REPORT = "abuse_report"
    CONSUMER_DISSATISFACTION = "consumer_dissatisfaction"
    DIRECT_COMPLAINT = "direct_complaint"
    REGULATORY_WARNING = "regulatory_warning"
    GENERAL_ADVISORY = "general_advisory"
    IMPERSONATION_TARGET = "impersonation_target"
    NEUTRAL_PROFILE = "neutral_profile"
    VERIFICATION_SIGNAL = "verification_signal"
    UNRELATED = "unrelated"

    # Compatibility aliases
    POSITIVE_SIGNAL = "positive_signal"
    NEUTRAL = "neutral"
    FRAUD_SCAM_ALLEGATION = "fraud_scam_allegation"
    PAYMENT_FRAUD = "payment_fraud"
    DIRECT_NEGATIVE_REPORT = "direct_negative_report"
    SCAM_FRAUD = "scam_fraud"
    COMPLAINT = "complaint"
    PAYMENT_REQUEST = "payment_request"
    NEGATIVE_REVIEW = "negative_review"
    FAKE_IMPERSONATION = "fake_impersonation"
    CONTRADICTORY = "contradictory"
    LEGAL_NEWS = "legal_news"
    COMPANY_VERIFICATION = "company_verification"
    MISSING_INFO = "missing_info"


class EvidenceRelationship(str, Enum):
    DIRECT = "DIRECT"
    NEGATIVE_MENTION = "NEGATIVE_MENTION"
    IMPERSONATION_TARGET = "IMPERSONATION_TARGET"
    SECURITY_ABUSE = "SECURITY_ABUSE"
    GENERAL_ADVISORY = "GENERAL_ADVISORY"
    GENERAL_WARNING = "GENERAL_WARNING"
    POSITIVE_SIGNAL = "POSITIVE_SIGNAL"
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    UNRELATED = "UNRELATED"


class SourceType(str, Enum):
    GOVERNMENT_REGULATORY = "Government / Regulatory"
    NEWS = "News"
    COMPANY = "Company"
    REVIEW = "Review"
    BLOG_FORUM = "Blog / Forum"
    OTHER = "Other"


class SourceTrust(str, Enum):
    HIGHER = "higher"
    MEDIUM = "medium"
    LOWER = "lower"
    UNKNOWN = "unknown"


class Confidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# ── Request / Response Models ───────────────────────────────────────────────────

class InvestigateRequest(BaseModel):
    input: str = Field(..., min_length=1, max_length=500, description="URL, company name, or offer to investigate")
    category: InputCategory = Field(default=InputCategory.AUTO, description="Category hint (auto-detect if 'auto')")


class EvidenceItem(BaseModel):
    category: EvidenceCategory
    severity: EvidenceStrength
    title: str
    summary: str
    source: str
    url: str
    snippet: str
    evidence_strength: EvidenceStrength
    source_type: str = SourceType.OTHER.value
    source_trust: SourceTrust = SourceTrust.UNKNOWN
    relationship: EvidenceRelationship = EvidenceRelationship.NEUTRAL
    risk_contribution: int = 0
    is_impersonation_target: bool = False
    complaint_type: Optional[str] = None


class SourceItem(BaseModel):
    title: str
    domain: str
    url: str
    snippet: str
    evidence_category: Optional[EvidenceCategory] = None
    evidence_strength: Optional[EvidenceStrength] = None
    source_type: str = SourceType.OTHER.value
    source_trust: SourceTrust = SourceTrust.UNKNOWN
    position: Optional[int] = None
    relationship: EvidenceRelationship = EvidenceRelationship.NEUTRAL
    complaint_type: Optional[str] = None


class RiskIndicator(BaseModel):
    icon: str
    label: str
    count: int
    severity: EvidenceStrength


class QueryRecord(BaseModel):
    query: str
    result_count: int
    status: str = "completed"


class InvestigateResponse(BaseModel):
    input: str
    normalized_input: str
    detected_type: DetectedType
    risk_score: int = Field(ge=0, le=100)
    overall_risk_score: int = Field(ge=0, le=100, default=0)
    content_signal_score: int = Field(ge=0, le=100, default=0)
    web_evidence_score: int = Field(ge=0, le=100, default=0)
    risk_level: RiskLevel
    confidence: Confidence
    summary: str
    content_signals: list[ContentSignal] = Field(default_factory=list)
    indicators: list[RiskIndicator] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    sources: list[SourceItem] = Field(default_factory=list)
    queries: list[QueryRecord] = Field(default_factory=list)
    search_count: int = 0
    unique_sources: int = 0
    relevant_evidence_count: int = 0
    relevant_unique_sources: int = 0
    filtered_unrelated_count: int = 0
    filtered_results: list[SourceItem] = Field(default_factory=list)
    duplicate_results_removed: int = 0
    impersonation_target_count: int = 0
    contradictions: list[dict] = Field(default_factory=list)
    is_demo: bool = False


class HealthResponse(BaseModel):
    status: str
    serpapi_configured: bool


class ErrorResponse(BaseModel):
    detail: str
    error_type: str = "unknown"
