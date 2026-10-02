import { Shield, ExternalLink } from 'lucide-react';

interface Props {
  onNavigateHowItWorks: () => void;
  onOpenPrivacy: () => void;
  onOpenAbout: () => void;
}

export default function Footer({ onNavigateHowItWorks, onOpenPrivacy, onOpenAbout }: Props) {
  // Only show GitHub link if explicitly configured via environment variable
  const githubUrl = import.meta.env.VITE_GITHUB_URL || null;

  return (
    <footer className="w-full border-t border-white/[0.08] bg-[#05070c]/90 py-8 px-4 sm:px-6 text-xs text-slate-400 mt-16">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Brand & Mission */}
        <div className="flex flex-col sm:flex-row items-center gap-3 text-center sm:text-left">
          <div className="w-8 h-8 rounded-xl bg-sky-500/15 border border-sky-500/30 flex items-center justify-center text-sky-400">
            <Shield className="w-4 h-4" />
          </div>
          <div>
            <p className="font-black text-white tracking-wider flex items-center justify-center sm:justify-start gap-1">
              SCAM<span className="text-sky-400">SHIELD</span>
            </p>
            <p className="text-[11px] text-slate-400">
              Evidence-based risk investigation powered by{' '}
              <a
                href="https://serpapi.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sky-400 hover:text-sky-300 font-semibold underline decoration-sky-400/40 underline-offset-2"
              >
                SerpApi
              </a>
              .
            </p>
          </div>
        </div>

        {/* Links */}
        <div className="flex flex-wrap items-center justify-center gap-5 text-xs font-medium text-slate-300">
          <button
            type="button"
            onClick={onNavigateHowItWorks}
            className="hover:text-white transition-colors cursor-pointer"
          >
            How it works
          </button>

          <button
            type="button"
            onClick={onOpenPrivacy}
            className="hover:text-white transition-colors cursor-pointer"
          >
            Privacy & Methodology
          </button>

          <button
            type="button"
            onClick={onOpenAbout}
            className="hover:text-white transition-colors cursor-pointer"
          >
            About
          </button>

          {/* GitHub link: only rendered if configured */}
          {githubUrl && (
            <a
              href={githubUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition-colors flex items-center gap-1 cursor-pointer"
            >
              <span>GitHub</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          )}
        </div>
      </div>

      {/* Legal disclaimer */}
      <div className="max-w-6xl mx-auto pt-6 mt-6 border-t border-white/[0.05] text-center text-[11px] text-slate-400">
        <p>
          Informational assessment only. Not legal or financial advice. ScamShield provides evidentiary research and risk indicators based on public records.
        </p>
      </div>
    </footer>
  );
}
