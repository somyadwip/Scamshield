import { useEffect, useState } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  ShieldQuestion,
  AlertTriangle,
  Copy,
  Check,
  Search,
  Layers,
  Filter,
  ExternalLink,
  Shield,
} from 'lucide-react';
import type { InvestigateResponse, RiskLevel } from '../types';

interface Props {
  data: InvestigateResponse;
}

const RISK_CONFIG: Record<
  RiskLevel,
  {
    color: string;
    glow: string;
    icon: React.ReactNode;
    label: string;
    textColor: string;
    ringColor: string;
    barColor: string;
    desc: string;
  }
> = {
  LOW: {
    color: 'bg-emerald-500/10 border-emerald-500/25',
    glow: 'glow-green',
    icon: <ShieldCheck className="w-6 h-6 text-emerald-400" />,
    label: 'LOW RISK',
    textColor: 'text-emerald-400',
    ringColor: '#10b981',
    barColor: 'bg-emerald-500',
    desc: 'No credible direct fraud allegations or regulatory warnings found against this entity.',
  },
  MODERATE: {
    color: 'bg-amber-500/10 border-amber-500/25',
    glow: 'glow-amber',
    icon: <AlertTriangle className="w-6 h-6 text-amber-400" />,
    label: 'MODERATE RISK',
    textColor: 'text-amber-400',
    ringColor: '#f59e0b',
    barColor: 'bg-amber-500',
    desc: 'Mild risk indicators or consumer dissatisfaction reports detected. Exercise caution.',
  },
  HIGH: {
    color: 'bg-orange-500/10 border-orange-500/25',
    glow: 'glow-orange',
    icon: <ShieldAlert className="w-6 h-6 text-orange-400" />,
    label: 'HIGH RISK',
    textColor: 'text-orange-400',
    ringColor: '#f97316',
    barColor: 'bg-orange-500',
    desc: 'Multiple strong risk indicators, advance-fee signals, or adverse reports detected.',
  },
  VERY_HIGH: {
    color: 'bg-rose-500/10 border-rose-500/25',
    glow: 'glow-red',
    icon: <ShieldAlert className="w-6 h-6 text-rose-400" />,
    label: 'VERY HIGH RISK',
    textColor: 'text-rose-400',
    ringColor: '#ef4444',
    barColor: 'bg-rose-500',
    desc: 'Critical fraud patterns, regulatory warnings, or severe scam allegations identified.',
  },
  INSUFFICIENT: {
    color: 'bg-slate-500/10 border-slate-500/25',
    glow: 'glow-gray',
    icon: <ShieldQuestion className="w-6 h-6 text-slate-400" />,
    label: 'INSUFFICIENT EVIDENCE',
    textColor: 'text-slate-400',
    ringColor: '#94a3b8',
    barColor: 'bg-slate-500',
    desc: 'Public records are currently insufficient to establish a conclusive risk score.',
  },
};

export default function ResultHeader({ data }: Props) {
  const [copied, setCopied] = useState(false);
  const [animatedScore, setAnimatedScore] = useState(0);

  const cfg = RISK_CONFIG[data.risk_level] || RISK_CONFIG.LOW;
  const isInsufficient = data.risk_level === 'INSUFFICIENT';

  // Smooth animated count-up for score
  useEffect(() => {
    const target = data.risk_score;
    if (target === 0) {
      setAnimatedScore(0);
      return;
    }
    let current = 0;
    const step = Math.max(1, Math.floor(target / 25));
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        setAnimatedScore(target);
        clearInterval(timer);
      } else {
        setAnimatedScore(current);
      }
    }, 25);
    return () => clearInterval(timer);
  }, [data.risk_score]);

  const circumference = 2 * Math.PI * 52;
  const targetOffset = circumference - (data.risk_score / 100) * circumference;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(data.normalized_input);
    setCopied(true);
    setTimeout(() => setCopied(false), 1800);
  };

  const relevantEvidence = data.relevant_evidence_count ?? data.evidence.length;
  const relevantSources = data.relevant_unique_sources ?? (data.unique_sources || data.sources.length);

  return (
    <div className={`glass p-6 sm:p-8 rounded-2xl ${cfg.glow} border-white/[0.08] space-y-6 fade-in`}>
      {/* Top Banner: Investigation Target */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-white/[0.08]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-widest text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/25">
              INVESTIGATION RESULT
            </span>
            <span className="text-[11px] font-semibold text-slate-400 bg-slate-900/80 px-2 py-0.5 rounded border border-slate-800">
              Type: {data.detected_type}
            </span>
            {data.is_demo && (
              <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-300 bg-cyan-950/60 border border-cyan-500/30 px-2 py-0.5 rounded">
                Simulated Demo
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight break-all">
              {data.normalized_input}
            </h2>
            <button
              onClick={copyToClipboard}
              className="text-slate-500 hover:text-slate-300 p-1 rounded transition-colors"
              title="Copy target text"
              aria-label="Copy target text"
            >
              {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
            </button>
          </div>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto text-xs text-slate-400">
          <span>Confidence:</span>
          <span
            className={`font-bold px-2 py-0.5 rounded border ${
              data.confidence === 'HIGH'
                ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
                : data.confidence === 'MEDIUM'
                ? 'text-amber-400 bg-amber-500/10 border-amber-500/20'
                : 'text-slate-400 bg-slate-800 border-slate-700'
            }`}
          >
            {data.confidence}
          </span>
        </div>
      </div>

      {/* Main Hero Card: Score Ring & Risk Verdict */}
      <div className="p-6 rounded-2xl bg-[#090d17]/80 border border-white/[0.06] flex flex-col md:flex-row items-center justify-between gap-8">
        {/* Left: Risk Verdict & Explanation */}
        <div className="space-y-3 flex-1 text-center md:text-left">
          <div className={`inline-flex items-center gap-2.5 px-4 py-2 rounded-xl border ${cfg.color}`}>
            {cfg.icon}
            <span className={`text-lg font-black tracking-wider ${cfg.textColor}`}>
              {cfg.label}
            </span>
          </div>

          <p className="text-xs sm:text-sm text-slate-300 max-w-md leading-relaxed">
            {isInsufficient
              ? 'The investigation did not locate sufficient authoritative direct evidence to make a definitive assessment. Caution is advised for unverified entities.'
              : cfg.desc}
          </p>
        </div>

        {/* Center: Circular Score Indicator */}
        <div className="relative w-36 h-36 shrink-0 flex items-center justify-center">
          <svg className="score-ring w-full h-full" viewBox="0 0 120 120">
            <circle className="track" cx="60" cy="60" r="52" strokeWidth="8" />
            <circle
              className="value"
              cx="60"
              cy="60"
              r="52"
              strokeWidth="8"
              stroke={cfg.ringColor}
              strokeDasharray={circumference}
              strokeDashoffset={targetOffset}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
            {isInsufficient ? (
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400 px-2">
                INSUFFICIENT
              </span>
            ) : (
              <>
                <span className={`text-3xl font-black font-mono tracking-tight ${cfg.textColor}`}>
                  {animatedScore}
                </span>
                <span className="text-[10px] uppercase font-bold tracking-widest text-slate-400">
                  / 100
                </span>
                <span className="text-[9px] uppercase font-medium text-slate-400 mt-0.5">
                  Evidence Score
                </span>
              </>
            )}
          </div>
        </div>

        {/* Right: Two-Layer Sub-Scores */}
        <div className="w-full md:w-64 space-y-3 p-4 rounded-xl bg-black/40 border border-white/[0.05]">
          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Score Components
          </p>

          {/* Layer 1: Content Signals */}
          <div className="space-y-1">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-300 font-medium">Layer 1: Content Signals</span>
              <span className="font-mono font-bold text-rose-400">
                {data.content_signal_score} / 100
              </span>
            </div>
            <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-rose-500 h-full rounded-full transition-all duration-700"
                style={{ width: `${Math.min(100, data.content_signal_score)}%` }}
              />
            </div>
          </div>

          {/* Layer 2: Web Evidence */}
          <div className="space-y-1">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-300 font-medium">Layer 2: Web Evidence</span>
              <span className="font-mono font-bold text-amber-400">
                {data.web_evidence_score} / 100
              </span>
            </div>
            <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-amber-500 h-full rounded-full transition-all duration-700"
                style={{ width: `${Math.min(100, data.web_evidence_score)}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Secondary Metrics Row (Visually secondary to the risk result) */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-3 pt-2">
        <div className="p-3 rounded-xl bg-white/[0.02] border border-white/[0.05] text-center">
          <p className="text-xl font-bold font-mono text-white">{relevantEvidence}</p>
          <p className="text-[11px] text-slate-400 mt-0.5">Relevant evidence</p>
        </div>

        <div className="p-3 rounded-xl bg-white/[0.02] border border-white/[0.05] text-center">
          <p className="text-xl font-bold font-mono text-sky-400">{relevantSources}</p>
          <p className="text-[11px] text-slate-400 mt-0.5">Independent sources</p>
        </div>

        <div className="p-3 rounded-xl bg-white/[0.02] border border-white/[0.05] text-center">
          <p className="text-xl font-bold font-mono text-slate-300">{data.search_count}</p>
          <p className="text-[11px] text-slate-400 mt-0.5">Searches performed</p>
        </div>

        <div className="p-3 rounded-xl bg-white/[0.02] border border-white/[0.05] text-center">
          <p className="text-xl font-bold font-mono text-slate-400">{data.duplicate_results_removed}</p>
          <p className="text-[11px] text-slate-400 mt-0.5">Duplicates filtered</p>
        </div>

        {typeof data.filtered_unrelated_count === 'number' && data.filtered_unrelated_count > 0 && (
          <div className="p-3 rounded-xl bg-white/[0.02] border border-white/[0.05] text-center col-span-2 sm:col-span-1">
            <p className="text-xl font-bold font-mono text-amber-400/90">{data.filtered_unrelated_count}</p>
            <p className="text-[11px] text-slate-400 mt-0.5">Filtered unrelated</p>
          </div>
        )}
      </div>

      {/* Impersonation Target Callout (when brand spoofing is detected) */}
      {data.impersonation_target_count > 0 && (
        <div className="p-4 rounded-xl bg-cyan-950/30 border border-cyan-500/30 flex items-start gap-3">
          <Shield className="w-5 h-5 text-cyan-400 shrink-0 mt-0.5" />
          <div className="space-y-1 text-xs">
            <p className="font-bold text-cyan-300">
              Impersonation Target Recognized ({data.impersonation_target_count} source{data.impersonation_target_count === 1 ? '' : 's'})
            </p>
            <p className="text-cyan-200/80 leading-relaxed">
              Public search indices describe scams where fraudsters impersonate or spoof <em>'{data.normalized_input}'</em> (e.g. fake tech support, phishing emails). ScamShield recognizes that this entity is a frequent target of brand impersonation, which does not penalize the entity's own risk score.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
