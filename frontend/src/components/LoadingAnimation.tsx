import { useEffect, useState } from 'react';
import { Search, CheckCircle2, ArrowRight, Circle, Shield, Radio } from 'lucide-react';

interface Stage {
  label: string;
  subtext: string;
}

const STAGES: Stage[] = [
  { label: 'Identified input type', subtext: 'Parsed domain, entity, or claim structure' },
  { label: 'Extracted relevant signals', subtext: 'Analyzing text for advance fees, urgency, or promises' },
  { label: 'Searching the web via SerpApi', subtext: 'Querying live Google indices across 4-7 targeted angles' },
  { label: 'Checking recent reports & complaints', subtext: 'Gathering public forum, consumer, and review signals' },
  { label: 'Comparing evidence & domain matching', subtext: 'Excluding unrelated search noise and isolating security reports' },
  { label: 'Building evidence report', subtext: 'Synthesizing two-layer assessment and independent sources' },
];

export default function LoadingAnimation() {
  const [currentStage, setCurrentStage] = useState(0);

  useEffect(() => {
    // Progress naturally across stages while SerpApi executes
    const timer = setInterval(() => {
      setCurrentStage((prev) => {
        if (prev < STAGES.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, 1800);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="w-full max-w-lg mx-auto py-12 px-4 fade-in" role="status" aria-live="polite">
      <div className="glass p-6 sm:p-8 rounded-2xl border-sky-500/30 bg-[#090d16]/90 shadow-[0_0_35px_rgba(14,165,233,0.15)] space-y-6">
        {/* Terminal Header */}
        <div className="flex items-center justify-between border-b border-sky-500/20 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-sky-500/15 border border-sky-500/30 flex items-center justify-center text-sky-400">
              <Search className="w-4 h-4 animate-pulse" />
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-sky-400 font-mono">
                [LIVE INVESTIGATION]
              </p>
              <h2 className="text-base font-bold text-white tracking-wide">
                ANALYZING INPUT & WEB EVIDENCE
              </h2>
            </div>
          </div>
          <span className="flex items-center gap-1.5 text-[11px] font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded-md border border-slate-800">
            <Radio className="w-3 h-3 text-sky-400 animate-pulse" />
            <span>STAGE {currentStage + 1}/{STAGES.length}</span>
          </span>
        </div>

        {/* Investigation Sequence Steps */}
        <div className="space-y-3 font-mono text-xs">
          {STAGES.map((stage, idx) => {
            const isCompleted = idx < currentStage;
            const isCurrent = idx === currentStage;
            const isPending = idx > currentStage;

            return (
              <div
                key={idx}
                className={`flex items-start gap-3 p-2.5 rounded-xl transition-all duration-300 ${
                  isCurrent
                    ? 'bg-sky-500/10 border border-sky-500/30 shadow-[0_0_12px_rgba(14,165,233,0.15)]'
                    : isCompleted
                    ? 'bg-emerald-500/5 text-slate-300 border border-emerald-500/20'
                    : 'text-slate-600 border border-transparent'
                }`}
              >
                {/* Icon marker */}
                <div className="mt-0.5 shrink-0">
                  {isCompleted ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  ) : isCurrent ? (
                    <ArrowRight className="w-4 h-4 text-sky-400 animate-pulse" />
                  ) : (
                    <Circle className="w-3.5 h-3.5 text-slate-700 ml-0.5" />
                  )}
                </div>

                {/* Text */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <span
                      className={`font-semibold ${
                        isCurrent
                          ? 'text-sky-300 font-bold'
                          : isCompleted
                          ? 'text-slate-200'
                          : 'text-slate-500'
                      }`}
                    >
                      {stage.label}
                    </span>
                    {isCurrent && (
                      <span className="text-[10px] uppercase font-bold text-sky-400 bg-sky-500/20 px-2 py-0.5 rounded-full animate-pulse">
                        In Progress
                      </span>
                    )}
                  </div>
                  <p
                    className={`text-[11px] mt-0.5 ${
                      isCurrent ? 'text-sky-200/70' : isCompleted ? 'text-slate-400' : 'text-slate-600'
                    }`}
                  >
                    {stage.subtext}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Progress Bar Footer */}
        <div className="pt-2 border-t border-white/[0.05] space-y-1.5">
          <div className="flex justify-between text-[11px] text-slate-400 font-mono">
            <span>Evidence Engine Pipeline</span>
            <span>{Math.round(((currentStage + 1) / STAGES.length) * 100)}%</span>
          </div>
          <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden border border-slate-800">
            <div
              className="bg-gradient-to-r from-sky-500 to-blue-500 h-full rounded-full transition-all duration-700"
              style={{ width: `${((currentStage + 1) / STAGES.length) * 100}%` }}
            />
          </div>
          <p className="text-[11px] text-slate-400 text-center pt-1">
            Running multi-angle live searches via SerpApi...
          </p>
        </div>
      </div>
    </div>
  );
}
