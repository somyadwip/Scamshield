import { useState } from 'react';
import {
  ChevronDown,
  ChevronUp,
  ExternalLink,
  Shield,
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  AlertOctagon,
  Lock,
  MessageSquareWarning,
  Landmark,
  Info,
  FileText,
  CheckCircle2,
  EyeOff,
  Newspaper,
  Building2,
  Star,
  MessagesSquare,
  Globe,
  Radio,
  Layers,
} from 'lucide-react';
import type { EvidenceItem, SourceItem } from '../types';

interface Props {
  evidence: EvidenceItem[];
  webScore?: number;
  filteredCount?: number;
  filteredResults?: SourceItem[];
}

const CATEGORY_CONFIG: Record<
  string,
  { icon: React.ReactNode; label: string; color: string; badge: string }
> = {
  fraud_allegation: {
    icon: <AlertOctagon className="w-4 h-4 text-rose-400" />,
    label: 'FRAUD ALLEGATION',
    color: 'text-rose-400',
    badge: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
  },
  FRAUD_ALLEGATION: {
    icon: <AlertOctagon className="w-4 h-4 text-rose-400" />,
    label: 'FRAUD ALLEGATION',
    color: 'text-rose-400',
    badge: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
  },
  scam_report: {
    icon: <ShieldAlert className="w-4 h-4 text-rose-400" />,
    label: 'SCAM REPORT',
    color: 'text-rose-400',
    badge: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
  },
  SCAM_REPORT: {
    icon: <ShieldAlert className="w-4 h-4 text-rose-400" />,
    label: 'SCAM REPORT',
    color: 'text-rose-400',
    badge: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
  },
  security_report: {
    icon: <Lock className="w-4 h-4 text-sky-400" />,
    label: 'SECURITY REPORT',
    color: 'text-sky-400',
    badge: 'bg-sky-500/15 text-sky-300 border-sky-500/30',
  },
  SECURITY_REPORT: {
    icon: <Lock className="w-4 h-4 text-sky-400" />,
    label: 'SECURITY REPORT',
    color: 'text-sky-400',
    badge: 'bg-sky-500/15 text-sky-300 border-sky-500/30',
  },
  abuse_report: {
    icon: <Shield className="w-4 h-4 text-cyan-400" />,
    label: 'ABUSE REPORT',
    color: 'text-cyan-400',
    badge: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
  },
  ABUSE_REPORT: {
    icon: <Shield className="w-4 h-4 text-cyan-400" />,
    label: 'ABUSE REPORT',
    color: 'text-cyan-400',
    badge: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
  },
  consumer_dissatisfaction: {
    icon: <MessageSquareWarning className="w-4 h-4 text-amber-400" />,
    label: 'CONSUMER DISSATISFACTION',
    color: 'text-amber-300',
    badge: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
  },
  CONSUMER_DISSATISFACTION: {
    icon: <MessageSquareWarning className="w-4 h-4 text-amber-400" />,
    label: 'CONSUMER DISSATISFACTION',
    color: 'text-amber-300',
    badge: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
  },
  direct_complaint: {
    icon: <AlertTriangle className="w-4 h-4 text-orange-400" />,
    label: 'DIRECT COMPLAINT',
    color: 'text-orange-400',
    badge: 'bg-orange-500/15 text-orange-300 border-orange-500/30',
  },
  DIRECT_COMPLAINT: {
    icon: <AlertTriangle className="w-4 h-4 text-orange-400" />,
    label: 'DIRECT COMPLAINT',
    color: 'text-orange-400',
    badge: 'bg-orange-500/15 text-orange-300 border-orange-500/30',
  },
  regulatory_warning: {
    icon: <Landmark className="w-4 h-4 text-rose-400" />,
    label: 'REGULATORY WARNING',
    color: 'text-rose-400',
    badge: 'bg-rose-500/20 text-rose-200 border-rose-500/40',
  },
  REGULATORY_WARNING: {
    icon: <Landmark className="w-4 h-4 text-rose-400" />,
    label: 'REGULATORY WARNING',
    color: 'text-rose-400',
    badge: 'bg-rose-500/20 text-rose-200 border-rose-500/40',
  },
  general_advisory: {
    icon: <Info className="w-4 h-4 text-indigo-400" />,
    label: 'GENERAL ADVISORY',
    color: 'text-indigo-300',
    badge: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30',
  },
  GENERAL_ADVISORY: {
    icon: <Info className="w-4 h-4 text-indigo-400" />,
    label: 'GENERAL ADVISORY',
    color: 'text-indigo-300',
    badge: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30',
  },
  impersonation_target: {
    icon: <ShieldCheck className="w-4 h-4 text-cyan-400" />,
    label: 'IMPERSONATION TARGET',
    color: 'text-cyan-300',
    badge: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
  },
  IMPERSONATION_TARGET: {
    icon: <ShieldCheck className="w-4 h-4 text-cyan-400" />,
    label: 'IMPERSONATION TARGET',
    color: 'text-cyan-300',
    badge: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
  },
  neutral_profile: {
    icon: <FileText className="w-4 h-4 text-slate-400" />,
    label: 'NEUTRAL PROFILE',
    color: 'text-slate-400',
    badge: 'bg-slate-500/15 text-slate-300 border-slate-500/30',
  },
  NEUTRAL_PROFILE: {
    icon: <FileText className="w-4 h-4 text-slate-400" />,
    label: 'NEUTRAL PROFILE',
    color: 'text-slate-400',
    badge: 'bg-slate-500/15 text-slate-300 border-slate-500/30',
  },
  verification_signal: {
    icon: <CheckCircle2 className="w-4 h-4 text-emerald-400" />,
    label: 'VERIFICATION SIGNAL',
    color: 'text-emerald-300',
    badge: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
  },
  VERIFICATION_SIGNAL: {
    icon: <CheckCircle2 className="w-4 h-4 text-emerald-400" />,
    label: 'VERIFICATION SIGNAL',
    color: 'text-emerald-300',
    badge: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
  },
  unrelated: {
    icon: <EyeOff className="w-4 h-4 text-slate-500" />,
    label: 'UNRELATED',
    color: 'text-slate-500',
    badge: 'bg-slate-800 text-slate-500 border-slate-700/60',
  },
  UNRELATED: {
    icon: <EyeOff className="w-4 h-4 text-slate-500" />,
    label: 'UNRELATED',
    color: 'text-slate-500',
    badge: 'bg-slate-800 text-slate-500 border-slate-700/60',
  },
};

const SOURCE_TYPE_CONFIG: Record<string, { icon: React.ReactNode; label: string; badge: string }> = {
  'Government / Regulatory': {
    icon: <Landmark className="w-3 h-3 text-emerald-400" />,
    label: 'Government / Regulatory',
    badge: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/25',
  },
  News: {
    icon: <Newspaper className="w-3 h-3 text-sky-400" />,
    label: 'News',
    badge: 'bg-sky-500/10 text-sky-300 border-sky-500/25',
  },
  Company: {
    icon: <Building2 className="w-3 h-3 text-blue-400" />,
    label: 'Company',
    badge: 'bg-blue-500/10 text-blue-300 border-blue-500/25',
  },
  Review: {
    icon: <Star className="w-3 h-3 text-amber-400" />,
    label: 'Review',
    badge: 'bg-amber-500/10 text-amber-300 border-amber-500/25',
  },
  'Blog / Forum': {
    icon: <MessagesSquare className="w-3 h-3 text-purple-400" />,
    label: 'Blog / Forum',
    badge: 'bg-purple-500/10 text-purple-300 border-purple-500/25',
  },
  Other: {
    icon: <Globe className="w-3 h-3 text-slate-400" />,
    label: 'Other',
    badge: 'bg-slate-800/80 text-slate-300 border-slate-700/60',
  },
};

const RELATIONSHIP_CONFIG: Record<string, { label: string; badge: string; desc: string }> = {
  DIRECT: {
    label: 'DIRECT EVIDENCE',
    badge: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
    desc: 'Direct allegation, complaint, or enforcement action directly against the entity',
  },
  NEGATIVE_MENTION: {
    label: 'NEGATIVE MENTION',
    badge: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    desc: 'Customer complaint, critical review, or grievance mentioning the entity',
  },
  IMPERSONATION_TARGET: {
    label: 'IMPERSONATION TARGET',
    badge: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    desc: 'Fraudsters impersonating or spoofing the entity (Attacking brand reputation, not entity fraud)',
  },
  SECURITY_ABUSE: {
    label: 'SECURITY / ABUSE REPORT',
    badge: 'bg-sky-500/15 text-sky-300 border-sky-500/30',
    desc: 'Technical DNS, SSL, network abuse, or vulnerability notification (distinct from consumer scam fraud)',
  },
  GENERAL_ADVISORY: {
    label: 'GENERAL ADVISORY',
    badge: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30',
    desc: 'Educational security guide or generic fraud warning not alleging entity misconduct',
  },
  GENERAL_WARNING: {
    label: 'GENERAL ADVISORY',
    badge: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30',
    desc: 'Educational security guide or generic fraud warning not alleging entity misconduct',
  },
  POSITIVE_SIGNAL: {
    label: 'POSITIVE SIGNAL',
    badge: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    desc: 'Verified business registry, official corporate presence, or trusted directory accreditation',
  },
  POSITIVE: {
    label: 'POSITIVE SIGNAL',
    badge: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    desc: 'Verified business registry, official corporate presence, or trusted directory accreditation',
  },
  NEUTRAL: {
    label: 'NEUTRAL PROFILE',
    badge: 'bg-slate-500/15 text-slate-300 border-slate-500/30',
    desc: 'Standard public directory listing or informational corporate profile',
  },
  UNRELATED: {
    label: 'UNRELATED',
    badge: 'bg-slate-800 text-slate-500 border-slate-700/60',
    desc: 'Search result unrelated to the investigated entity (excluded from evidence)',
  },
};

export default function EvidenceList({
  evidence,
  webScore,
  filteredCount,
  filteredResults,
}: Props) {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
  const [showFiltered, setShowFiltered] = useState(false);

  if (!evidence.length && !filteredCount && (!filteredResults || !filteredResults.length)) return null;

  // Separate scam evidence from technical security & abuse reports
  const isSecurityOrAbuse = (item: EvidenceItem) =>
    item.category === 'security_report' ||
    item.category === 'SECURITY_REPORT' ||
    item.category === 'abuse_report' ||
    item.category === 'ABUSE_REPORT' ||
    item.relationship === 'SECURITY_ABUSE';

  const scamEvidence = evidence.filter((item) => !isSecurityOrAbuse(item));
  const securityReports = evidence.filter(isSecurityOrAbuse);

  const renderCard = (item: EvidenceItem, globalIdx: number) => {
    const catCfg = CATEGORY_CONFIG[item.category] || CATEGORY_CONFIG.neutral_profile;
    const relCfg = RELATIONSHIP_CONFIG[item.relationship] || RELATIONSHIP_CONFIG.NEUTRAL;
    const srcCfg = SOURCE_TYPE_CONFIG[item.source_type] || SOURCE_TYPE_CONFIG.Other;
    const isExpanded = expandedIndex === globalIdx;

    return (
      <div
        key={globalIdx}
        className={`glass-sm overflow-hidden transition-all rounded-xl ${
          item.relationship === 'IMPERSONATION_TARGET'
            ? 'border-cyan-500/30 bg-cyan-950/15 shadow-[0_0_15px_rgba(6,182,212,0.1)]'
            : item.relationship === 'SECURITY_ABUSE'
            ? 'border-sky-500/30 bg-sky-950/15'
            : item.relationship === 'DIRECT'
            ? 'border-rose-500/30 bg-rose-950/10'
            : 'border-white/[0.06] hover:border-white/[0.12]'
        }`}
      >
        {/* Card Header & Preview */}
        <div className="p-4 sm:p-5 space-y-3">
          {/* Badges row */}
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex flex-wrap items-center gap-1.5">
              {/* Category */}
              <span
                className={`inline-flex items-center gap-1.5 text-[10px] px-2.5 py-0.5 rounded-md font-bold uppercase tracking-wider ${catCfg.badge}`}
              >
                {catCfg.icon}
                <span>{catCfg.label}</span>
              </span>

              {/* Relationship */}
              <span
                className={`text-[10px] px-2.5 py-0.5 rounded-md border font-bold uppercase tracking-wider ${relCfg.badge}`}
              >
                {relCfg.label}
              </span>

              {/* Source Type with subtle Lucide badge */}
              <span
                className={`inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-md border font-medium ${srcCfg.badge}`}
              >
                {srcCfg.icon}
                <span>{srcCfg.label}</span>
              </span>
            </div>

            {/* Risk Contribution */}
            <span
              className={`text-[11px] font-mono font-bold px-2.5 py-0.5 rounded-md border ${
                item.risk_contribution > 0
                  ? 'bg-rose-500/15 text-rose-300 border-rose-500/30'
                  : 'bg-slate-800 text-slate-400 border-slate-700/60'
              }`}
            >
              +{item.risk_contribution} pts
            </span>
          </div>

          {/* Title */}
          <h4 className="text-sm sm:text-base font-bold text-white tracking-tight leading-snug">
            {item.title}
          </h4>

          {/* 2-3 line snippet */}
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed line-clamp-3">
            {item.snippet || item.summary}
          </p>

          {/* Actions & Source Info */}
          <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-white/[0.04] text-xs">
            <div className="flex items-center gap-2 text-slate-400 truncate max-w-sm">
              <span className="text-slate-500">Source:</span>
              <strong className="text-slate-200 truncate">{item.source}</strong>
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setExpandedIndex(isExpanded ? null : globalIdx)}
                className="text-xs text-slate-400 hover:text-slate-200 transition-colors inline-flex items-center gap-1 cursor-pointer py-1 px-2 rounded hover:bg-white/[0.04]"
                aria-expanded={isExpanded}
              >
                <span>{isExpanded ? 'Less info' : 'More details'}</span>
                {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>

              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-sky-500/15 hover:bg-sky-500/25 text-sky-300 hover:text-sky-200 border border-sky-500/30 text-xs font-semibold transition-all cursor-pointer"
              >
                <span>VIEW SOURCE</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        </div>

        {/* Expandable Extended Details */}
        {isExpanded && (
          <div className="px-5 pb-5 pt-3 bg-black/40 border-t border-white/[0.05] space-y-2.5 text-xs fade-in">
            <div className="p-3 rounded-lg bg-white/[0.02] border border-white/[0.05] space-y-1">
              <span className="text-slate-400 font-semibold uppercase tracking-wider text-[10px]">
                Investigative Context:
              </span>
              <p className="text-slate-300 leading-relaxed">{relCfg.desc}</p>
            </div>

            <div className="space-y-1">
              <span className="text-slate-400 font-semibold uppercase tracking-wider text-[10px]">
                Full Extracted Snippet:
              </span>
              <p className="text-slate-300 leading-relaxed font-mono text-[11px] bg-slate-950/70 p-3 rounded-lg border border-slate-800">
                {item.snippet}
              </p>
            </div>

            <div className="flex flex-wrap items-center justify-between text-[11px] text-slate-400 pt-1">
              <span>Source URL: <span className="font-mono text-slate-400 break-all">{item.url}</span></span>
              <span>Verification origin: <strong className="text-sky-400">SerpApi Web Index</strong></span>
            </div>
          </div>
        )}
      </div>
    );
  };

  const totalFiltered = filteredCount ?? (filteredResults ? filteredResults.length : 0);

  return (
    <div className="glass p-6 sm:p-7 rounded-2xl border-sky-500/25 bg-[#080d19]/80 shadow-[0_0_30px_rgba(14,165,233,0.1)] space-y-6 fade-in">
      {/* Layer 2 Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-sky-500/20">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-black uppercase tracking-wider text-sky-300 bg-sky-500/20 px-2.5 py-0.5 rounded border border-sky-500/40">
              LAYER 2
            </span>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Targeted Public Search Records
            </span>
          </div>
          <h3 className="text-lg font-black text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-sky-400" />
            External Web Evidence & Verification Findings ({evidence.length})
          </h3>
        </div>

        <div className="text-right flex items-center sm:flex-col sm:items-end justify-between sm:justify-center">
          <span className="text-xs text-slate-400 font-medium">Layer 2 Score</span>
          <span className="text-xl font-bold font-mono text-amber-400">
            {webScore ?? 0} <span className="text-xs text-slate-500 font-normal">/ 100</span>
          </span>
        </div>
      </div>

      {/* Main Scam / Fraud Evidence & Reviews */}
      {scamEvidence.length > 0 ? (
        <div className="space-y-3.5">
          {scamEvidence.map((item, i) => renderCard(item, i))}
        </div>
      ) : (
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-center text-xs text-slate-400">
          No direct adverse scam or fraud allegations found in public search indices.
        </div>
      )}

      {/* Separated Technical Security & Abuse Information */}
      {securityReports.length > 0 && (
        <div className="mt-6 pt-5 border-t border-slate-800 space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <Lock className="w-4 h-4 text-sky-400" />
              <h4 className="text-sm font-bold uppercase tracking-wider text-sky-300">
                Security & Abuse Reports ({securityReports.length})
              </h4>
            </div>
            <span className="text-[11px] text-slate-400 font-medium italic">
              Technical reports — 0 scam risk contribution
            </span>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Technical DNS, SSL, abuse notifications, or network administration records are separated from consumer scam reports and do not indicate consumer fraud.
          </p>
          <div className="space-y-3">
            {securityReports.map((item, i) => renderCard(item, scamEvidence.length + i))}
          </div>
        </div>
      )}

      {/* Filtered Unrelated Results Section (Transparency) */}
      {totalFiltered > 0 && (
        <div className="mt-6 p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-3">
          <button
            type="button"
            onClick={() => setShowFiltered(!showFiltered)}
            className="w-full flex items-center justify-between text-left cursor-pointer group"
            aria-expanded={showFiltered}
          >
            <div className="flex items-center gap-2.5">
              <div className="p-1 rounded bg-slate-800 border border-slate-700">
                <EyeOff className="w-3.5 h-3.5 text-slate-400" />
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-300 group-hover:text-white transition-colors">
                  FILTERED RESULTS ({totalFiltered})
                </span>
                <p className="text-xs text-slate-400 mt-0.5">
                  {totalFiltered} unrelated search {totalFiltered === 1 ? 'result was' : 'results were'} excluded from the assessment.
                </p>
              </div>
            </div>
            <span className="text-xs text-sky-400 group-hover:text-sky-300 font-semibold transition-colors flex items-center gap-1">
              <span>{showFiltered ? 'Hide' : 'Expand'}</span>
              {showFiltered ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </span>
          </button>

          {showFiltered && filteredResults && filteredResults.length > 0 && (
            <div className="mt-3 pt-3 border-t border-slate-800 space-y-2 max-h-80 overflow-y-auto pr-1 fade-in">
              {filteredResults.map((src, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-lg bg-black/40 border border-slate-800 text-xs space-y-1"
                >
                  <div className="flex items-start justify-between gap-2">
                    <p className="font-semibold text-slate-200 line-clamp-1">{src.title}</p>
                    <span className="text-[10px] uppercase font-bold text-slate-400 bg-slate-800 border border-slate-700 px-1.5 py-0.5 rounded shrink-0">
                      Reason: UNRELATED
                    </span>
                  </div>
                  <p className="text-[11px] text-sky-400 font-mono">{src.domain}</p>
                  <p className="text-slate-400 text-xs line-clamp-2 leading-relaxed">{src.snippet}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
