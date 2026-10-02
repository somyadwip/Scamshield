import { useState } from 'react';
import {
  ChevronDown,
  ChevronUp,
  ExternalLink,
  Layers,
  Landmark,
  Newspaper,
  Building2,
  Star,
  MessagesSquare,
  Globe,
} from 'lucide-react';
import type { SourceItem } from '../types';

interface Props {
  sources: SourceItem[];
}

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
    badge: 'bg-slate-800 text-slate-300 border-slate-700/60',
  },
};

export default function SourcePanel({ sources }: Props) {
  const [open, setOpen] = useState(false);

  if (!sources || !sources.length) return null;

  return (
    <div className="glass overflow-hidden rounded-2xl border-white/[0.08] transition-all">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between p-5 hover:bg-white/[0.02] transition-colors cursor-pointer"
        aria-expanded={open}
      >
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-sky-500/10 border border-sky-500/25 text-sky-400">
            <Layers className="w-4 h-4" />
          </div>
          <div className="text-left">
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold uppercase tracking-wider text-white">
                RELEVANT INDEPENDENT SOURCES ({sources.length})
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Authoritative external domains and public reporting registries evaluated
            </p>
          </div>
        </div>

        <span className="text-slate-400">
          {open ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </span>
      </button>

      {open && (
        <div className="px-5 pb-6 space-y-2.5 border-t border-white/[0.05] pt-3 fade-in">
          {sources.map((src, i) => {
            const srcCfg = SOURCE_TYPE_CONFIG[src.source_type] || SOURCE_TYPE_CONFIG.Other;
            return (
              <div
                key={i}
                className="p-3.5 rounded-xl bg-black/40 border border-white/[0.05] hover:border-white/[0.1] transition-colors flex flex-col sm:flex-row sm:items-start justify-between gap-3 text-xs"
              >
                <div className="flex-1 min-w-0 space-y-1">
                  <div className="flex items-center gap-2">
                    <p className="text-sm font-semibold text-white line-clamp-1">{src.title}</p>
                  </div>
                  <p className="text-[11px] font-mono text-sky-400">{src.domain}</p>
                  <p className="text-slate-400 text-xs line-clamp-2 leading-relaxed">
                    {src.snippet}
                  </p>
                </div>

                <div className="flex items-center gap-2 shrink-0 self-end sm:self-start pt-1 sm:pt-0">
                  <span
                    className={`inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-md border font-medium ${srcCfg.badge}`}
                  >
                    {srcCfg.icon}
                    <span>{srcCfg.label}</span>
                  </span>

                  <a
                    href={src.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-1.5 rounded-lg bg-sky-500/10 hover:bg-sky-500/20 text-sky-300 border border-sky-500/25 transition-colors"
                    title="Open external source"
                    aria-label={`Open source: ${src.title}`}
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
