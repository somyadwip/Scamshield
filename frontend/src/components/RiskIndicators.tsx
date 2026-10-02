import {
  Landmark,
  ShieldCheck,
  AlertTriangle,
  ShieldAlert,
  MessageSquareWarning,
  Lock,
  CheckCircle2,
  AlertOctagon,
} from 'lucide-react';
import type { RiskIndicator } from '../types';

interface Props {
  indicators: RiskIndicator[];
}

function getIndicatorIcon(label: string) {
  const l = label.toLowerCase();
  if (l.includes('regulatory') || l.includes('official')) {
    return <Landmark className="w-5 h-5 text-rose-400" />;
  }
  if (l.includes('impersonat')) {
    return <ShieldCheck className="w-5 h-5 text-cyan-400" />;
  }
  if (l.includes('fraud') || l.includes('scam')) {
    return <ShieldAlert className="w-5 h-5 text-rose-400" />;
  }
  if (l.includes('complaint')) {
    return <AlertTriangle className="w-5 h-5 text-orange-400" />;
  }
  if (l.includes('dissatisfaction')) {
    return <MessageSquareWarning className="w-5 h-5 text-amber-400" />;
  }
  if (l.includes('security') || l.includes('abuse')) {
    return <Lock className="w-5 h-5 text-sky-400" />;
  }
  if (l.includes('positive') || l.includes('verification')) {
    return <CheckCircle2 className="w-5 h-5 text-emerald-400" />;
  }
  return <AlertOctagon className="w-5 h-5 text-slate-400" />;
}

export default function RiskIndicators({ indicators }: Props) {
  if (!indicators || !indicators.length) return null;

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 fade-in">
      {indicators.map((ind, i) => (
        <div
          key={i}
          className={`p-4 rounded-xl text-center transition-all bg-black/40 border ${
            ind.severity === 'HIGH'
              ? 'border-rose-500/25 bg-rose-950/10'
              : ind.severity === 'MEDIUM'
              ? 'border-amber-500/25 bg-amber-950/10'
              : 'border-white/[0.06] hover:border-white/[0.12]'
          }`}
        >
          <div className="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.06] flex items-center justify-center mx-auto mb-2">
            {getIndicatorIcon(ind.label)}
          </div>
          <p className="text-2xl font-black font-mono text-white tracking-tight">{ind.count}</p>
          <p className="text-xs font-semibold text-slate-300 mt-1 leading-snug">{ind.label}</p>
        </div>
      ))}
    </div>
  );
}
