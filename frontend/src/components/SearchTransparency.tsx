import { useState, useMemo } from 'react';
import { ChevronDown, ChevronUp, Search, CheckCircle2, XCircle, ExternalLink, Zap } from 'lucide-react';
import type { QueryRecord } from '../types';

interface Props {
  queries: QueryRecord[];
  searchCount: number;
  relevantEvidenceCount: number;
  relevantSourcesCount: number;
  duplicatesRemoved: number;
  filteredUnrelatedCount?: number;
}

export default function SearchTransparency({
  queries,
  searchCount,
  relevantEvidenceCount,
  relevantSourcesCount,
  duplicatesRemoved,
  filteredUnrelatedCount = 0,
}: Props) {
  const [open, setOpen] = useState(false);

  const totalRawResults = useMemo(() => {
    return queries.reduce((acc, q) => acc + (q.result_count || 0), 0);
  }, [queries]);

  if (!queries.length) return null;

  return (
    <div className="glass overflow-hidden rounded-2xl border-white/[0.08] transition-all">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full flex flex-col sm:flex-row sm:items-center justify-between p-5 hover:bg-white/[0.02] transition-colors cursor-pointer gap-2"
        aria-expanded={open}
      >
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-sky-500/10 border border-sky-500/25 text-sky-400">
            <Search className="w-4 h-4" />
          </div>
          <div className="text-left">
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold uppercase tracking-wider text-white">
                HOW SCAMSHIELD INVESTIGATED THIS
              </span>
              <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-sky-500/15 text-sky-300 border border-sky-500/30">
                {queries.length} searches
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Technical transparency audit of live Google searches and evidence filtering
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 self-end sm:self-auto">
          {/* POWERED BY SERPAPI Badge */}
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-900 border border-sky-500/30 text-sky-300 text-[11px] font-bold shadow-[0_0_10px_rgba(14,165,233,0.15)]">
            <Zap className="w-3 h-3 text-sky-400 fill-sky-400" />
            <span>POWERED BY SERPAPI</span>
          </div>

          <span className="text-slate-400">
            {open ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </span>
        </div>
      </button>

      {open && (
        <div className="px-5 pb-6 pt-2 space-y-5 border-t border-white/[0.05] fade-in">
          {/* Summary Metrics Row */}
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5 pt-1 text-center font-mono">
            <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
              <p className="text-lg font-bold text-white">{totalRawResults}</p>
              <p className="text-[10px] text-slate-400 font-sans mt-0.5">Results analyzed</p>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
              <p className="text-lg font-bold text-sky-400">{relevantEvidenceCount}</p>
              <p className="text-[10px] text-slate-400 font-sans mt-0.5">Relevant evidence</p>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
              <p className="text-lg font-bold text-emerald-400">{relevantSourcesCount}</p>
              <p className="text-[10px] text-slate-400 font-sans mt-0.5">Independent sources</p>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
              <p className="text-lg font-bold text-slate-400">{duplicatesRemoved}</p>
              <p className="text-[10px] text-slate-400 font-sans mt-0.5">Duplicates removed</p>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 col-span-2 sm:col-span-1">
              <p className="text-lg font-bold text-amber-400">{filteredUnrelatedCount}</p>
              <p className="text-[10px] text-slate-400 font-sans mt-0.5">Unrelated filtered</p>
            </div>
          </div>

          {/* Searches Performed */}
          <div className="space-y-2">
            <p className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Searches performed via SerpApi:
            </p>
            <div className="space-y-1.5 font-mono text-xs">
              {queries.map((q, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between gap-3 px-3 py-2 rounded-lg bg-black/40 border border-white/[0.04]"
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    {q.status === 'completed' ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    ) : (
                      <XCircle className="w-4 h-4 text-rose-400 shrink-0" />
                    )}
                    <span className="text-slate-300 truncate">{q.query}</span>
                  </div>
                  <span className="text-slate-400 shrink-0 text-[11px]">
                    {q.result_count} result{q.result_count !== 1 ? 's' : ''}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* SerpApi Attribution Footer */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-2 p-3 rounded-xl bg-sky-950/30 border border-sky-500/20 text-xs text-sky-200">
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-sky-400" />
              <span>Real-time Google search index provided by <strong>SerpApi</strong>.</span>
            </div>
            <a
              href="https://serpapi.com"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-sky-300 hover:text-white underline font-semibold"
            >
              <span>Learn about SerpApi</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
