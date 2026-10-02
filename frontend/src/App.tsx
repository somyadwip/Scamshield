import { useState, useEffect } from 'react';
import { investigate, checkHealth } from './services/api';
import type { InvestigateResponse, InputCategory } from './types';

import Header from './components/Header';
import SearchBox from './components/SearchBox';
import HeroSection from './components/HeroSection';
import LoadingAnimation from './components/LoadingAnimation';
import ResultHeader from './components/ResultHeader';
import RiskIndicators from './components/RiskIndicators';
import SummaryCard from './components/SummaryCard';
import ContradictionCard from './components/ContradictionCard';
import ContentSignalsPanel from './components/ContentSignalsPanel';
import EvidenceList from './components/EvidenceList';
import SourcePanel from './components/SourcePanel';
import SearchTransparency from './components/SearchTransparency';
import ErrorMessage from './components/ErrorMessage';
import Footer from './components/Footer';
import { Shield, X, Lock } from 'lucide-react';

export default function App() {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState<InputCategory>('auto');
  const [result, setResult] = useState<InvestigateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [serpapiConfigured, setSerpapiConfigured] = useState<boolean | null>(null);
  const [privacyModalOpen, setPrivacyModalOpen] = useState(false);
  const [aboutModalOpen, setAboutModalOpen] = useState(false);

  useEffect(() => {
    checkHealth()
      .then((h) => setSerpapiConfigured(h.serpapi_configured))
      .catch(() => setSerpapiConfigured(false));
  }, []);

  const handleInvestigate = async (overrideQuery?: string, overrideCategory?: InputCategory) => {
    const searchTerm = (overrideQuery ?? query).trim();
    if (!searchTerm) return;

    const targetCategory = overrideCategory ?? category;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await investigate(searchTerm, targetCategory);
      setResult(data);
      // Smooth scroll to results
      setTimeout(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 100);
    } catch (err: any) {
      setError(err.message || "ScamShield couldn't complete the investigation.");
    } finally {
      setLoading(false);
    }
  };

  // When clicking an example chip, POPULATE input without immediately submitting (Spec 1 & 22)
  const handlePopulateExample = (exampleText: string, exampleCategory: InputCategory) => {
    setQuery(exampleText);
    setCategory(exampleCategory);
    // Focus search input
    const input = document.getElementById('search-input');
    if (input) {
      input.focus();
      input.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
    setQuery('');
    setCategory('auto');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleNavigateHowItWorks = () => {
    if (result) {
      setResult(null);
    }
    setTimeout(() => {
      const el = document.getElementById('how-it-works');
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }, 50);
  };

  const handleNavigateAbout = () => {
    setAboutModalOpen(true);
  };

  return (
    <div className="bg-grid min-h-dvh flex flex-col relative text-slate-100">
      <Header
        onReset={handleReset}
        onNavigateHowItWorks={handleNavigateHowItWorks}
        onNavigateAbout={handleNavigateAbout}
        serpapiConfigured={serpapiConfigured}
      />

      <main className="flex-1 w-full max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-8 space-y-8">
        {/* Search area - large, prominent, always accessible */}
        <div className="w-full">
          <SearchBox
            value={query}
            onChange={setQuery}
            onSubmit={() => handleInvestigate()}
            loading={loading}
            selectedCategory={category}
            onCategoryChange={setCategory}
            onPopulateExample={handlePopulateExample}
          />
        </div>

        {/* Loading state - multi-stage sequence */}
        {loading && <LoadingAnimation />}

        {/* Error message */}
        {error && !loading && (
          <ErrorMessage message={error} onRetry={() => handleInvestigate()} />
        )}

        {/* Results view */}
        {result && !loading && (
          <div className="space-y-6 fade-in">
            {/* Section 4 & 5: Results Hero, Circular Score Ring, Sub-scores */}
            <ResultHeader data={result} />

            {/* Quick Summary Indicators */}
            {result.indicators && result.indicators.length > 0 && (
              <RiskIndicators indicators={result.indicators} />
            )}

            {/* Section 6: Prominent "WHY WAS THIS FLAGGED?" Card */}
            <SummaryCard summary={result.summary} />

            {/* Contradictions Detected (if any) */}
            {result.contradictions && result.contradictions.length > 0 && (
              <ContradictionCard contradictions={result.contradictions} />
            )}

            {/* Section 7: LAYER 1 - Signals Found Directly in Your Input */}
            <ContentSignalsPanel
              signals={result.content_signals}
              score={result.content_signal_score}
            />

            {/* Section 7, 8, 9, 10: LAYER 2 - External Web Evidence, Categories, Security Separation & Filtered Results */}
            <EvidenceList
              evidence={result.evidence}
              webScore={result.web_evidence_score}
              filteredCount={result.filtered_unrelated_count}
              filteredResults={result.filtered_results}
            />

            {/* Section 9: Relevant Independent Sources Panel */}
            <SourcePanel sources={result.sources} />

            {/* Section 11: HOW SCAMSHIELD INVESTIGATED (Searches & SerpApi Attribution) */}
            <SearchTransparency
              queries={result.queries}
              searchCount={result.search_count}
              relevantEvidenceCount={result.relevant_evidence_count ?? result.evidence.length}
              relevantSourcesCount={result.relevant_unique_sources ?? result.sources.length}
              duplicatesRemoved={result.duplicate_results_removed}
              filteredUnrelatedCount={result.filtered_unrelated_count}
            />
          </div>
        )}

        {/* Landing Page Hero (shown before search or when reset) */}
        {!loading && !result && !error && (
          <HeroSection
            onSelectCategory={(cat) => setCategory(cat)}
            onPopulateExample={handlePopulateExample}
          />
        )}
      </main>

      <Footer
        onNavigateHowItWorks={handleNavigateHowItWorks}
        onOpenPrivacy={() => setPrivacyModalOpen(true)}
        onOpenAbout={() => setAboutModalOpen(true)}
      />

      {/* Privacy & Methodology Modal */}
      {privacyModalOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm fade-in"
          role="dialog"
          aria-modal="true"
        >
          <div className="glass max-w-lg w-full p-6 sm:p-7 rounded-2xl border-white/[0.1] bg-[#090d16] space-y-4">
            <div className="flex items-center justify-between border-b border-white/[0.08] pb-3">
              <div className="flex items-center gap-2">
                <Shield className="w-5 h-5 text-sky-400" />
                <h3 className="text-base font-bold text-white">Privacy & Investigation Methodology</h3>
              </div>
              <button
                type="button"
                onClick={() => setPrivacyModalOpen(false)}
                className="text-slate-400 hover:text-white p-1 rounded transition-colors"
                aria-label="Close modal"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs sm:text-sm text-slate-300 leading-relaxed max-h-96 overflow-y-auto pr-1">
              <p>
                <strong>1. User Privacy:</strong> ScamShield does not sell, track, or store your submitted personal data. Investigations query public search indices via SerpApi in real-time.
              </p>
              <p>
                <strong>2. Two-Layer Architecture:</strong> Layer 1 inspects the structural claims in submitted text (e.g. upfront fee requests or guaranteed return promises). Layer 2 verifies public reports, regulatory notices, and independent reviews across the public web.
              </p>
              <p>
                <strong>3. Entity Relevance Filter:</strong> Generic search results (such as IRS tax forms or state DMV pages) and technical DNS or network maintenance notices are cleanly separated and excluded from consumer fraud scores.
              </p>
              <p>
                <strong>4. Informational Scope:</strong> ScamShield provides evidentiary research and does not deliver legal rulings or financial counsel.
              </p>
            </div>

            <div className="pt-2 text-right">
              <button
                type="button"
                onClick={() => setPrivacyModalOpen(false)}
                className="px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider bg-sky-500/15 hover:bg-sky-500/25 text-sky-300 border border-sky-500/30 transition-colors cursor-pointer"
              >
                Got it
              </button>
            </div>
          </div>
        </div>
      )}

      {/* About Modal */}
      {aboutModalOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm fade-in"
          role="dialog"
          aria-modal="true"
        >
          <div className="glass max-w-lg w-full p-6 sm:p-7 rounded-2xl border-white/[0.1] bg-[#090d16] space-y-4">
            <div className="flex items-center justify-between border-b border-white/[0.08] pb-3">
              <div className="flex items-center gap-2">
                <Shield className="w-5 h-5 text-sky-400" />
                <h3 className="text-base font-bold text-white">About ScamShield</h3>
              </div>
              <button
                type="button"
                onClick={() => setAboutModalOpen(false)}
                className="text-slate-400 hover:text-white p-1 rounded transition-colors"
                aria-label="Close modal"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs sm:text-sm text-slate-300 leading-relaxed">
              <p>
                <strong>ScamShield</strong> was created for the Google Antigravity Hackathon to solve a pervasive problem: black-box AI tools that give arbitrary confidence scores without evidence.
              </p>
              <p>
                Instead of guessing, ScamShield runs live, multi-angle targeted web investigations using <strong>SerpApi</strong>, filters out unrelated noise, separates harmless customer grievances from genuine fraud, and reveals the exact sources behind every score.
              </p>
              <p className="text-slate-400 text-xs">
                "Don't just get a verdict. See the evidence."
              </p>
            </div>

            <div className="pt-2 text-right">
              <button
                type="button"
                onClick={() => setAboutModalOpen(false)}
                className="px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider bg-sky-500/15 hover:bg-sky-500/25 text-sky-300 border border-sky-500/30 transition-colors cursor-pointer"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
