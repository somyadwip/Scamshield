import {
  CreditCard,
  Award,
  TrendingUp,
  Clock,
  FileWarning,
  DollarSign,
  AlertTriangle,
  CheckCircle2,
  Layers,
  Quote,
} from 'lucide-react';
import type { ContentSignal, ContentSignalCategory } from '../types';

interface Props {
  signals: ContentSignal[];
  score: number;
}

const CATEGORY_ICON: Record<string, React.ReactNode> = {
  UPFRONT_PAYMENT: <CreditCard className="w-4 h-4 text-rose-400" />,
  GUARANTEED_INCOME: <Award className="w-4 h-4 text-rose-400" />,
  UNREALISTIC_EARNINGS: <TrendingUp className="w-4 h-4 text-amber-400" />,
  URGENCY_PRESSURE: <Clock className="w-4 h-4 text-orange-400" />,
  PERSONAL_DATA_REQUEST: <FileWarning className="w-4 h-4 text-rose-400" />,
  INVESTMENT_PATTERNS: <DollarSign className="w-4 h-4 text-amber-400" />,
  JOB_SCAM_PATTERNS: <AlertTriangle className="w-4 h-4 text-rose-400" />,
};

export default function ContentSignalsPanel({ signals, score }: Props) {
  if (!signals || signals.length === 0) {
    return (
      <div className="glass-sm p-5 rounded-2xl border border-emerald-500/20 bg-emerald-950/10 flex items-center justify-between fade-in">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0">
            <CheckCircle2 className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-0.5">
              <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/15 px-2 py-0.5 rounded border border-emerald-500/30">
                LAYER 1 • INPUT ANALYSIS
              </span>
              <p className="text-sm font-bold text-white">Signals Found in Your Input</p>
            </div>
            <p className="text-xs text-slate-400">
              No advance fees, guaranteed return claims, or artificial urgency patterns were detected directly in the submitted text.
            </p>
          </div>
        </div>
        <span className="text-xs font-mono font-bold px-3 py-1 rounded-lg bg-emerald-500/10 text-emerald-300 border border-emerald-500/25 shrink-0 ml-3">
          0 / 100
        </span>
      </div>
    );
  }

  return (
    <div className="glass p-6 sm:p-7 rounded-2xl border-rose-500/30 bg-[#120a10]/80 shadow-[0_0_30px_rgba(244,63,94,0.12)] space-y-4 fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-rose-500/20">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-black uppercase tracking-wider text-rose-300 bg-rose-500/20 px-2.5 py-0.5 rounded border border-rose-500/40">
              LAYER 1
            </span>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Submitted Content Analysis
            </span>
          </div>
          <h3 className="text-lg font-black text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-rose-400" />
            Signals Found in Your Input ({signals.length})
          </h3>
        </div>

        <div className="text-right flex items-center sm:flex-col sm:items-end justify-between sm:justify-center">
          <span className="text-xs text-slate-400 font-medium">Layer 1 Score</span>
          <span className="text-xl font-bold font-mono text-rose-400">
            {score} <span className="text-xs text-slate-500 font-normal">/ 100</span>
          </span>
        </div>
      </div>

      {/* Transparency Banner: User Claim vs Web Fact */}
      <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/25 flex items-start gap-2.5 text-xs text-amber-200/90 leading-relaxed">
        <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
        <p>
          <strong className="text-amber-300 font-semibold">Important Evidence Distinction:</strong> These {signals.length} indicator(s) were parsed directly from the text submitted to ScamShield (e.g. advance-fee demands or high-pressure claims). They represent inherent risk characteristics within the offer itself, independent of external web records.
        </p>
      </div>

      {/* Signal Cards */}
      <div className="space-y-3">
        {signals.map((sig, idx) => {
          const icon = CATEGORY_ICON[sig.category] || <AlertTriangle className="w-4 h-4 text-rose-400" />;
          return (
            <div
              key={idx}
              className="p-4 rounded-xl border border-rose-500/20 bg-black/45 hover:border-rose-500/40 transition-colors space-y-2.5"
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2.5">
                  <div className="p-1.5 rounded-lg bg-rose-500/15 border border-rose-500/30">
                    {icon}
                  </div>
                  <span className="text-sm font-bold text-white">{sig.title}</span>
                </div>

                <div className="flex items-center gap-2">
                  <span
                    className={`text-[10px] px-2.5 py-0.5 rounded-full border font-bold uppercase tracking-wider ${
                      sig.severity === 'HIGH'
                        ? 'bg-rose-500/15 text-rose-300 border-rose-500/30'
                        : sig.severity === 'MEDIUM'
                        ? 'bg-amber-500/15 text-amber-300 border-amber-500/30'
                        : 'bg-slate-500/15 text-slate-300 border-slate-500/30'
                    }`}
                  >
                    {sig.severity}
                  </span>
                  <span className="text-[11px] px-2.5 py-0.5 rounded-full font-mono font-bold bg-rose-500/15 text-rose-300 border border-rose-500/30">
                    +{sig.risk_contribution} pts
                  </span>
                </div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">
                {sig.description}
              </p>

              {sig.quote && (
                <div className="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs flex items-start gap-2">
                  <Quote className="w-3.5 h-3.5 text-slate-500 shrink-0 mt-0.5" />
                  <div className="text-slate-300 font-mono">
                    <span className="text-slate-500 select-none mr-1.5">Claim:</span>
                    <span className="text-amber-300/95 italic font-semibold">"{sig.quote}"</span>
                  </div>
                </div>
              )}

              <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1 border-t border-white/[0.04]">
                <span>Origin: <strong className="text-slate-400">User-Provided Text</strong></span>
                <span>Signal Category: <strong className="text-slate-400">{sig.category}</strong></span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
