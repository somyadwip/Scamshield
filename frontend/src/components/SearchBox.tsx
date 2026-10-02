import { useMemo } from 'react';
import {
  Search,
  ArrowRight,
  X,
  Globe,
  Building2,
  Briefcase,
  ShoppingCart,
  TrendingUp,
  GraduationCap,
  Sparkles,
  HelpCircle,
  ShieldAlert,
} from 'lucide-react';
import type { InputCategory } from '../types';

interface Props {
  value: string;
  onChange: (v: string) => void;
  onSubmit: () => void;
  loading: boolean;
  selectedCategory: InputCategory;
  onCategoryChange: (cat: InputCategory) => void;
  onPopulateExample: (text: string, category: InputCategory) => void;
}

const CATEGORIES: { value: InputCategory; label: string; icon: React.ReactNode }[] = [
  { value: 'auto', label: 'Auto Detect', icon: <Sparkles className="w-3.5 h-3.5" /> },
  { value: 'website', label: 'Website', icon: <Globe className="w-3.5 h-3.5" /> },
  { value: 'company', label: 'Company', icon: <Building2 className="w-3.5 h-3.5" /> },
  { value: 'job_offer', label: 'Job Offer', icon: <Briefcase className="w-3.5 h-3.5" /> },
  { value: 'shopping', label: 'Shopping', icon: <ShoppingCart className="w-3.5 h-3.5" /> },
  { value: 'investment', label: 'Investment', icon: <TrendingUp className="w-3.5 h-3.5" /> },
  { value: 'course', label: 'Course', icon: <GraduationCap className="w-3.5 h-3.5" /> },
  { value: 'other', label: 'Other', icon: <HelpCircle className="w-3.5 h-3.5" /> },
];

export default function SearchBox({
  value,
  onChange,
  onSubmit,
  loading,
  selectedCategory,
  onCategoryChange,
  onPopulateExample,
}: Props) {
  // Client-side auto detection preview for user feedback
  const detectedType = useMemo(() => {
    const trimmed = value.trim().toLowerCase();
    if (!trimmed) return null;
    if (trimmed.startsWith('http://') || trimmed.startsWith('https://') || /^[a-z0-9-]+(\.[a-z]{2,})+/i.test(trimmed)) {
      return 'Website / URL';
    }
    if (
      trimmed.includes('fee') ||
      trimmed.includes('salary') ||
      trimmed.includes('earn') ||
      trimmed.includes('per month') ||
      trimmed.includes('₹') ||
      trimmed.includes('registration') ||
      trimmed.includes('job') ||
      trimmed.includes('work from home')
    ) {
      return 'Job Offer / Scheme';
    }
    if (trimmed.includes('course') || trimmed.includes('curriculum') || trimmed.includes('masterclass')) {
      return 'Course / Education';
    }
    if (trimmed.includes('invest') || trimmed.includes('guaranteed return') || trimmed.includes('crypto') || trimmed.includes('yield')) {
      return 'Investment Scheme';
    }
    if (trimmed.includes('shop') || trimmed.includes('store') || trimmed.includes('discount') || trimmed.includes('price')) {
      return 'Shopping Site';
    }
    return 'Company / Entity';
  }, [value]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !loading && value.trim()) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4">
      {/* Main Search Bar Card */}
      <div className="glass-input rounded-2xl p-2 transition-all">
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
          {/* Input field */}
          <div className="flex-1 flex items-center gap-3 px-3 py-2 sm:py-2.5">
            <Search className="w-5 h-5 text-sky-400 shrink-0 select-none" />
            <input
              id="search-input"
              type="text"
              value={value}
              onChange={(e) => onChange(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Paste a URL, company, job offer, or suspicious message..."
              disabled={loading}
              className="w-full bg-transparent text-sm sm:text-base text-white placeholder:text-slate-500 outline-none font-medium"
              autoComplete="off"
              aria-label="Search term or suspicious content to investigate"
            />
            {value && !loading && (
              <button
                type="button"
                onClick={() => onChange('')}
                className="text-slate-500 hover:text-slate-300 p-1 rounded-md transition-colors"
                aria-label="Clear input"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Investigate Action Button */}
          <button
            id="investigate-btn"
            type="button"
            onClick={onSubmit}
            disabled={loading || !value.trim()}
            className="px-6 py-3.5 sm:py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 active:scale-[0.98] text-white shadow-[0_0_20px_rgba(14,165,233,0.35)] hover:shadow-[0_0_25px_rgba(14,165,233,0.5)] disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none transition-all flex items-center justify-center gap-2 shrink-0 cursor-pointer"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>INVESTIGATING</span>
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <span>INVESTIGATE</span>
                <ArrowRight className="w-4 h-4" />
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Category Pills & Auto-Detection Status */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 px-1">
        {/* Category selection */}
        <div className="flex flex-wrap items-center gap-1.5" role="radiogroup" aria-label="Target category">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mr-1 select-none">
            Category:
          </span>
          {CATEGORIES.map((cat) => {
            const isSelected = selectedCategory === cat.value;
            return (
              <button
                key={cat.value}
                type="button"
                role="radio"
                aria-checked={isSelected}
                onClick={() => onCategoryChange(cat.value)}
                className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-sky-500/20 text-sky-300 border border-sky-400/40 shadow-[0_0_10px_rgba(14,165,233,0.2)]'
                    : 'bg-white/[0.03] text-slate-400 border border-white/[0.06] hover:bg-white/[0.07] hover:text-slate-200'
                }`}
              >
                {cat.icon}
                <span>{cat.label}</span>
              </button>
            );
          })}
        </div>

        {/* Live Auto-detection Feedback */}
        {selectedCategory === 'auto' && detectedType && (
          <div className="flex items-center gap-1.5 text-xs text-sky-300 bg-sky-950/40 border border-sky-500/25 px-2.5 py-0.5 rounded-full self-start sm:self-auto">
            <span className="w-1.5 h-1.5 rounded-full bg-sky-400 animate-pulse" />
            <span className="text-slate-400">Detected:</span>
            <span className="font-semibold text-sky-300">{detectedType}</span>
          </div>
        )}
      </div>

      {/* Demo Example Chips (Clicking populates input, DOES NOT immediately submit) */}
      <div className="pt-2 border-t border-white/[0.05] flex flex-wrap items-center gap-2 text-xs">
        <span className="text-slate-500 font-medium">Try a demo example:</span>
        <button
          type="button"
          onClick={() => onPopulateExample('https://example.com', 'website')}
          className="px-2.5 py-1 rounded-md bg-white/[0.04] hover:bg-white/[0.09] text-slate-300 hover:text-white border border-white/[0.08] transition-colors cursor-pointer"
          title="Click to populate input with example.com"
        >
          <span className="text-slate-500 mr-1.5">🌐 Website:</span>
          <strong>example.com</strong>
        </button>

        <button
          type="button"
          onClick={() => onPopulateExample('Microsoft', 'company')}
          className="px-2.5 py-1 rounded-md bg-white/[0.04] hover:bg-white/[0.09] text-slate-300 hover:text-white border border-white/[0.08] transition-colors cursor-pointer"
          title="Click to populate input with Microsoft"
        >
          <span className="text-slate-500 mr-1.5">🏢 Company:</span>
          <strong>Microsoft</strong>
        </button>

        <button
          type="button"
          onClick={() =>
            onPopulateExample(
              'Earn ₹50,000 per month from home. No experience required. Pay ₹999 registration fee to start. Guaranteed income.',
              'job_offer'
            )
          }
          className="px-2.5 py-1 rounded-md bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 hover:text-rose-200 border border-rose-500/25 transition-colors cursor-pointer flex items-center gap-1.5"
          title="Click to populate input with a fictional suspicious job offer demo"
        >
          <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
          <span>Suspicious job offer</span>
          <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-rose-500/25 text-rose-200 border border-rose-500/40">
            DEMO EXAMPLE
          </span>
        </button>
      </div>
    </div>
  );
}
