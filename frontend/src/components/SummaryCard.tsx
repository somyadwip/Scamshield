import { useState, useMemo } from 'react';
import { HelpCircle, ChevronDown, ChevronUp, FileText } from 'lucide-react';

interface Props {
  summary: string;
}

export default function SummaryCard({ summary }: Props) {
  const [expanded, setExpanded] = useState(false);

  // Split summary into sentences for clean concise 2-3 sentence initial presentation
  const { conciseText, remainingText, hasMore } = useMemo(() => {
    if (!summary) return { conciseText: '', remainingText: '', hasMore: false };

    // Regex to split on sentence boundaries
    const sentences = summary.match(/[^.!?]+[.!?]+(\s+|$)/g) || [summary];

    if (sentences.length <= 3 || summary.length < 240) {
      return {
        conciseText: summary,
        remainingText: '',
        hasMore: false,
      };
    }

    const concise = sentences.slice(0, 3).join('').trim();
    const remaining = sentences.slice(3).join('').trim();

    return {
      conciseText: concise,
      remainingText: remaining,
      hasMore: Boolean(remaining),
    };
  }, [summary]);

  if (!summary) return null;

  return (
    <div className="glass p-6 sm:p-7 rounded-2xl border-sky-500/25 bg-[#090d18]/80 shadow-[0_0_25px_rgba(14,165,233,0.12)] space-y-3 fade-in">
      {/* Prominent Header */}
      <div className="flex items-center justify-between pb-2 border-b border-white/[0.06]">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-sky-500/15 border border-sky-500/30 flex items-center justify-center text-sky-400">
            <HelpCircle className="w-4 h-4" />
          </div>
          <h3 className="text-base font-extrabold uppercase tracking-wider text-white">
            WHY WAS THIS FLAGGED?
          </h3>
        </div>
        <span className="text-[11px] font-mono text-slate-400">
          Executive Evidence Summary
        </span>
      </div>

      {/* Concise 2-3 sentence explanation */}
      <div className="text-sm sm:text-base text-slate-200 leading-relaxed space-y-2">
        <p>{conciseText}</p>

        {/* Expandable full explanation */}
        {hasMore && expanded && (
          <p className="text-slate-300 pt-2 border-t border-white/[0.05] fade-in">
            {remainingText}
          </p>
        )}
      </div>

      {/* Read More / Read Less Toggle */}
      {hasMore && (
        <div className="pt-1">
          <button
            type="button"
            onClick={() => setExpanded(!expanded)}
            className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-sky-400 hover:text-sky-300 transition-colors cursor-pointer"
          >
            <span>{expanded ? 'Read less' : 'Read more'}</span>
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      )}
    </div>
  );
}
