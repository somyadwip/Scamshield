import { Shield, Radio } from 'lucide-react';

interface Props {
  onReset: () => void;
  onNavigateHowItWorks: () => void;
  onNavigateAbout: () => void;
  serpapiConfigured?: boolean | null;
}

export default function Header({
  onReset,
  onNavigateHowItWorks,
  onNavigateAbout,
  serpapiConfigured,
}: Props) {
  return (
    <header className="w-full border-b border-white/[0.08] bg-[#070a10]/85 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Brand */}
        <button
          onClick={onReset}
          className="flex items-center gap-2.5 group cursor-pointer text-left focus-visible:ring-2 focus-visible:ring-sky-500 rounded-lg p-1"
          aria-label="ScamShield Home"
        >
          <div className="w-9 h-9 rounded-xl bg-sky-500/15 border border-sky-500/30 flex items-center justify-center group-hover:border-sky-400/60 transition-colors shadow-[0_0_12px_rgba(14,165,233,0.25)]">
            <Shield className="w-5 h-5 text-sky-400 group-hover:scale-105 transition-transform" />
          </div>
          <div>
            <span className="text-lg font-black tracking-wider text-white flex items-center gap-1.5">
              SCAM<span className="text-sky-400 font-extrabold">SHIELD</span>
            </span>
            <span className="hidden sm:block text-[10px] uppercase font-semibold tracking-widest text-slate-400">
              Web Threat Intelligence
            </span>
          </div>
        </button>

        {/* Navigation items */}
        <nav className="flex items-center gap-1 sm:gap-2">
          <button
            onClick={onReset}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white hover:bg-white/[0.05] transition-colors cursor-pointer"
          >
            Investigate
          </button>
          <button
            onClick={onNavigateHowItWorks}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white hover:bg-white/[0.05] transition-colors cursor-pointer"
          >
            How it works
          </button>
          <button
            onClick={onNavigateAbout}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white hover:bg-white/[0.05] transition-colors cursor-pointer"
          >
            About
          </button>
        </nav>

        {/* Live SerpApi Status */}
        <div className="hidden md:flex items-center gap-3">
          {serpapiConfigured === true && (
            <div className="flex items-center gap-2 text-xs font-medium text-emerald-400 bg-emerald-500/10 border border-emerald-500/25 px-3 py-1 rounded-full shadow-[0_0_10px_rgba(16,185,129,0.15)]">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span>SerpApi Live</span>
            </div>
          )}
          {serpapiConfigured === false && (
            <div className="flex items-center gap-2 text-xs font-medium text-amber-400 bg-amber-500/10 border border-amber-500/25 px-3 py-1 rounded-full">
              <Radio className="w-3.5 h-3.5 text-amber-400" />
              <span>Simulated Demo Mode</span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
