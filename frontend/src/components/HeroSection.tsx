import {
  Shield,
  Globe,
  Building2,
  Briefcase,
  ShoppingCart,
  TrendingUp,
  GraduationCap,
  Search,
  Filter,
  Layers,
  FileCheck2,
  ExternalLink,
  ChevronRight,
} from 'lucide-react';
import type { InputCategory } from '../types';

interface Props {
  onSelectCategory: (cat: InputCategory) => void;
  onPopulateExample: (text: string, cat: InputCategory) => void;
}

const CAPABILITIES = [
  {
    category: 'website' as InputCategory,
    icon: <Globe className="w-5 h-5 text-sky-400" />,
    label: 'Website / Domain',
    example: 'https://example.com',
    desc: 'Verify registered domains, DNS records, and scam reports.',
  },
  {
    category: 'company' as InputCategory,
    icon: <Building2 className="w-5 h-5 text-indigo-400" />,
    label: 'Company / Brand',
    example: 'Microsoft',
    desc: 'Distinguish direct fraud from third-party impersonation.',
  },
  {
    category: 'job_offer' as InputCategory,
    icon: <Briefcase className="w-5 h-5 text-emerald-400" />,
    label: 'Job Offer / Recruitment',
    example: 'Earn ₹50,000/month from home. Pay ₹999 registration fee.',
    desc: 'Detect upfront fee demands and guaranteed income claims.',
  },
  {
    category: 'shopping' as InputCategory,
    icon: <ShoppingCart className="w-5 h-5 text-amber-400" />,
    label: 'Shopping / E-Commerce',
    example: 'luxury-deal-store.shop',
    desc: 'Check counterfeit alerts, payment complaints, and reviews.',
  },
  {
    category: 'investment' as InputCategory,
    icon: <TrendingUp className="w-5 h-5 text-rose-400" />,
    label: 'Investment Scheme',
    example: 'Crypto Yield 300% Guaranteed',
    desc: 'Flag Ponzi indicators and unregistered financial schemes.',
  },
  {
    category: 'course' as InputCategory,
    icon: <GraduationCap className="w-5 h-5 text-purple-400" />,
    label: 'Course / Training',
    example: 'Guaranteed High-Paying Placement Course',
    desc: 'Evaluate accreditation records and misleading job promises.',
  },
];

const WORKFLOW_STEPS = [
  {
    step: '1',
    title: 'Enter something suspicious',
    desc: 'Paste a URL, entity name, job recruitment offer, or unsolicited message.',
    icon: <Search className="w-5 h-5 text-sky-400" />,
  },
  {
    step: '2',
    title: 'ScamShield extracts relevant signals',
    desc: 'The text is analyzed for advance-fee demands, unrealistic promises, and urgency pressure.',
    icon: <Layers className="w-5 h-5 text-indigo-400" />,
  },
  {
    step: '3',
    title: 'SerpApi searches the public web',
    desc: 'Targeted multi-angle searches query Google for complaints, fraud alerts, reviews, and news.',
    icon: <Globe className="w-5 h-5 text-cyan-400" />,
  },
  {
    step: '4',
    title: 'Evidence is filtered and classified',
    desc: 'Domain matching separates unrelated noise. Security reports are isolated from consumer scams.',
    icon: <Filter className="w-5 h-5 text-amber-400" />,
  },
  {
    step: '5',
    title: 'You receive a transparent assessment',
    desc: 'Inspect exact risk contributions, independent sources, and the full evidence trail.',
    icon: <FileCheck2 className="w-5 h-5 text-emerald-400" />,
  },
];

export default function HeroSection({ onSelectCategory, onPopulateExample }: Props) {
  const scrollToSearch = () => {
    const input = document.getElementById('search-input');
    if (input) {
      input.focus();
      input.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  return (
    <div className="space-y-16 py-6 fade-in">
      {/* Hero Header */}
      <section className="text-center space-y-5 max-w-3xl mx-auto pt-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/25 text-sky-400 text-xs font-semibold tracking-wide">
          <Shield className="w-3.5 h-3.5" />
          <span>Evidence-Based Web Threat Intelligence</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white">
          SCAM<span className="text-sky-400">SHIELD</span>
        </h1>

        <p className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-slate-200 via-sky-200 to-slate-300 bg-clip-text text-transparent">
          "Investigate before you trust."
        </p>

        <p className="text-sm sm:text-base text-slate-400 leading-relaxed max-w-2xl mx-auto">
          Don't just get a verdict. See the evidence. Analyze suspicious websites, companies, job offers, shopping sites, investment schemes, and courses using live web evidence.
        </p>
      </section>

      {/* What can you investigate section */}
      <section className="space-y-4">
        <div className="text-center">
          <h2 className="text-sm font-bold uppercase tracking-widest text-slate-400">
            What Can You Investigate?
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Select a target type below or paste your content in the search bar above
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5 max-w-4xl mx-auto">
          {CAPABILITIES.map((cap) => (
            <button
              key={cap.category}
              type="button"
              onClick={() => {
                onSelectCategory(cap.category);
                scrollToSearch();
              }}
              className="glass-sm p-4 text-left transition-all hover:border-sky-500/30 hover:bg-sky-950/20 group cursor-pointer focus-visible:ring-2 focus-visible:ring-sky-500 rounded-xl"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="p-2 rounded-lg bg-white/[0.03] border border-white/[0.06] group-hover:scale-105 transition-transform">
                  {cap.icon}
                </div>
                <ChevronRight className="w-4 h-4 text-slate-600 group-hover:text-sky-400 group-hover:translate-x-0.5 transition-all" />
              </div>
              <h3 className="text-sm font-bold text-slate-200 group-hover:text-white transition-colors">
                {cap.label}
              </h3>
              <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                {cap.desc}
              </p>
            </button>
          ))}
        </div>
      </section>

      {/* HOW SCAMSHIELD WORKS Section */}
      <section id="how-it-works" className="glass p-6 sm:p-8 rounded-2xl max-w-4xl mx-auto border-sky-500/20 bg-sky-950/10 space-y-6">
        <div className="text-center space-y-1">
          <div className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-sky-400 bg-sky-500/10 px-2.5 py-0.5 rounded-full border border-sky-500/20">
            5-Stage Verification Pipeline
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-white">
            HOW SCAMSHIELD WORKS
          </h2>
          <p className="text-xs text-slate-400 max-w-xl mx-auto">
            Traditional tools give black-box AI scores. ScamShield gathers public web records, validates entity relevance, and shows you the actual sources.
          </p>
        </div>

        <div className="relative space-y-4 pt-2">
          {WORKFLOW_STEPS.map((step, idx) => (
            <div
              key={step.step}
              className="flex items-start gap-4 p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-slate-700 transition-colors"
            >
              <div className="w-8 h-8 rounded-full bg-sky-500/15 border border-sky-500/30 flex items-center justify-center shrink-0 font-mono font-bold text-sky-300 text-sm shadow-[0_0_10px_rgba(14,165,233,0.2)]">
                {step.step}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-bold text-slate-200">{step.title}</h3>
                </div>
                <p className="text-xs text-slate-400 mt-0.5 leading-relaxed">{step.desc}</p>
              </div>
              <div className="hidden sm:block p-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-400">
                {step.icon}
              </div>
            </div>
          ))}
        </div>

        <div className="pt-2 text-center">
          <button
            type="button"
            onClick={scrollToSearch}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider bg-sky-500/15 hover:bg-sky-500/25 text-sky-300 border border-sky-500/30 hover:border-sky-500/50 transition-all cursor-pointer"
          >
            <span>Start an Investigation</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="max-w-4xl mx-auto p-6 rounded-2xl border border-white/[0.06] bg-slate-950/40 text-center space-y-3">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400">
          About ScamShield
        </h2>
        <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto leading-relaxed">
          ScamShield is an open intelligence verification tool developed for the Google Antigravity Hackathon. Powered by live Google Web Indices via <strong>SerpApi</strong>, ScamShield separates genuine fraud allegations from harmless product dissatisfaction and technical network administration records.
        </p>
        <p className="text-[11px] text-slate-500">
          Informational assessment only. ScamShield provides evidentiary research and does not replace professional legal, financial, or cyber incident response advice.
        </p>
      </section>
    </div>
  );
}
