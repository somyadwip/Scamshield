/* ── ScamShield types ──────────────────────────────────────────────────── */

export type RiskLevel = 'LOW' | 'MODERATE' | 'HIGH' | 'VERY_HIGH' | 'INSUFFICIENT';
export type EvidenceStrength = 'LOW' | 'MEDIUM' | 'HIGH';
export type Confidence = 'LOW' | 'MEDIUM' | 'HIGH';
export type SourceTrust = 'higher' | 'medium' | 'lower' | 'unknown';

export type SourceType =
  | 'Government / Regulatory'
  | 'News'
  | 'Company'
  | 'Review'
  | 'Blog / Forum'
  | 'Other';

export type EvidenceCategory =
  | 'fraud_allegation'
  | 'scam_report'
  | 'security_report'
  | 'abuse_report'
  | 'consumer_dissatisfaction'
  | 'direct_complaint'
  | 'regulatory_warning'
  | 'general_advisory'
  | 'impersonation_target'
  | 'neutral_profile'
  | 'verification_signal'
  | 'unrelated'
  | 'FRAUD_ALLEGATION'
  | 'SCAM_REPORT'
  | 'SECURITY_REPORT'
  | 'ABUSE_REPORT'
  | 'CONSUMER_DISSATISFACTION'
  | 'DIRECT_COMPLAINT'
  | 'REGULATORY_WARNING'
  | 'GENERAL_ADVISORY'
  | 'IMPERSONATION_TARGET'
  | 'NEUTRAL_PROFILE'
  | 'VERIFICATION_SIGNAL'
  | 'UNRELATED'
  | 'direct_negative_report'
  | 'positive_signal'
  | 'neutral'
  | 'fraud_scam_allegation'
  | 'payment_fraud'
  | 'scam_fraud'
  | 'complaint'
  | 'payment_request'
  | 'negative_review'
  | 'fake_impersonation'
  | 'contradictory'
  | 'legal_news'
  | 'company_verification'
  | 'missing_info';

export type EvidenceRelationship =
  | 'DIRECT'
  | 'NEGATIVE_MENTION'
  | 'IMPERSONATION_TARGET'
  | 'GENERAL_ADVISORY'
  | 'GENERAL_WARNING'
  | 'POSITIVE_SIGNAL'
  | 'POSITIVE'
  | 'NEUTRAL'
  | 'SECURITY_ABUSE'
  | 'UNRELATED';

export interface EvidenceItem {
  category: EvidenceCategory;
  severity: EvidenceStrength;
  title: string;
  summary: string;
  source: string;
  url: string;
  snippet: string;
  evidence_strength: EvidenceStrength;
  source_type: SourceType | string;
  source_trust?: SourceTrust;
  relationship: EvidenceRelationship;
  risk_contribution: number;
  is_impersonation_target?: boolean;
  complaint_type?: string;
}

export interface SourceItem {
  title: string;
  domain: string;
  url: string;
  snippet: string;
  evidence_category: EvidenceCategory | null;
  evidence_strength: EvidenceStrength | null;
  source_type: SourceType | string;
  source_trust?: SourceTrust;
  position: number | null;
  relationship?: EvidenceRelationship;
  complaint_type?: string;
}

export interface RiskIndicator {
  icon: string;
  label: string;
  count: number;
  severity: EvidenceStrength;
}

export interface QueryRecord {
  query: string;
  result_count: number;
  status: string;
}

export interface Contradiction {
  type: string;
  description: string;
  positive_source?: { title: string; url: string; snippet: string };
  negative_source?: { title: string; url: string; snippet: string };
  claim_source?: { title: string; url: string; snippet: string };
  counter_source?: { title: string; url: string; snippet: string };
}

export type ContentSignalCategory =
  | 'UPFRONT_PAYMENT'
  | 'GUARANTEED_INCOME'
  | 'UNREALISTIC_EARNINGS'
  | 'JOB_SCAM_PATTERNS'
  | 'URGENCY_PRESSURE'
  | 'PERSONAL_DATA_REQUEST'
  | 'INVESTMENT_PATTERNS';

export interface ContentSignal {
  category: ContentSignalCategory;
  severity: EvidenceStrength;
  title: string;
  description: string;
  quote: string;
  risk_contribution: number;
}

export interface InvestigateResponse {
  input: string;
  normalized_input: string;
  detected_type: string;
  risk_score: number;
  overall_risk_score: number;
  content_signal_score: number;
  web_evidence_score: number;
  risk_level: RiskLevel;
  confidence: Confidence;
  summary: string;
  content_signals: ContentSignal[];
  indicators: RiskIndicator[];
  evidence: EvidenceItem[];
  sources: SourceItem[];
  queries: QueryRecord[];
  search_count: number;
  unique_sources: number;
  duplicate_results_removed: number;
  relevant_evidence_count?: number;
  relevant_unique_sources?: number;
  filtered_unrelated_count?: number;
  filtered_results?: SourceItem[];
  impersonation_target_count: number;
  contradictions: Contradiction[];
  is_demo?: boolean;
}

export interface HealthResponse {
  status: string;
  serpapi_configured: boolean;
}

export type InputCategory =
  | 'auto'
  | 'website'
  | 'company'
  | 'job_offer'
  | 'shopping'
  | 'investment'
  | 'course'
  | 'other';
