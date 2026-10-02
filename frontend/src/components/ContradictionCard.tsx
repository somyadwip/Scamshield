import { Zap, ExternalLink } from 'lucide-react';
import type { Contradiction } from '../types';

interface Props {
  contradictions: Contradiction[];
}

export default function ContradictionCard({ contradictions }: Props) {
  return (
    <div className="glass p-6 border-accent-amber/20">
      <div className="flex items-center gap-2 mb-4">
        <Zap className="w-5 h-5 text-accent-amber" />
        <h3 className="text-sm font-semibold uppercase tracking-wider text-accent-amber">
          Contradictory Claims Detected
        </h3>
      </div>

      <div className="space-y-4">
        {contradictions.map((c, i) => (
          <div key={i} className="glass-sm p-4 space-y-3">
            <p className="text-sm text-slate-300">{c.description}</p>

            <div className="grid sm:grid-cols-2 gap-3">
              {/* Claim / Positive */}
              {(c.positive_source || c.claim_source) && (
                <div className="p-3 rounded-lg bg-accent-green/5 border border-accent-green/10">
                  <p className="text-xs font-semibold text-accent-green mb-1">Claim</p>
                  <p className="text-xs text-slate-400 mb-1">
                    {(c.positive_source || c.claim_source)!.title}
                  </p>
                  <p className="text-xs text-slate-500 line-clamp-2">
                    {(c.positive_source || c.claim_source)!.snippet}
                  </p>
                  <a
                    href={(c.positive_source || c.claim_source)!.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-[10px] text-accent-blue mt-1 hover:underline"
                  >
                    View source <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              )}

              {/* Counter / Negative */}
              {(c.negative_source || c.counter_source) && (
                <div className="p-3 rounded-lg bg-accent-red/5 border border-accent-red/10">
                  <p className="text-xs font-semibold text-accent-red mb-1">Counter-evidence</p>
                  <p className="text-xs text-slate-400 mb-1">
                    {(c.negative_source || c.counter_source)!.title}
                  </p>
                  <p className="text-xs text-slate-500 line-clamp-2">
                    {(c.negative_source || c.counter_source)!.snippet}
                  </p>
                  <a
                    href={(c.negative_source || c.counter_source)!.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-[10px] text-accent-blue mt-1 hover:underline"
                  >
                    View source <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
