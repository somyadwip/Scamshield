import { AlertCircle, RefreshCw, WifiOff, KeyRound, SearchX } from 'lucide-react';

interface Props {
  message: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ message, onRetry }: Props) {
  // Format message cleanly without exposing raw stack traces
  const isConnectionError =
    message.toLowerCase().includes('failed to fetch') ||
    message.toLowerCase().includes('network') ||
    message.toLowerCase().includes('connection') ||
    message.toLowerCase().includes('econnrefused');

  const isConfigError =
    message.toLowerCase().includes('serpapi') ||
    message.toLowerCase().includes('key') ||
    message.toLowerCase().includes('configured');

  const isNoResults =
    message.toLowerCase().includes('no results') ||
    message.toLowerCase().includes('not found');

  let title = "ScamShield couldn't complete the investigation.";
  let description = 'Check your connection and try again.';
  let Icon = AlertCircle;

  if (isConnectionError) {
    Icon = WifiOff;
    title = "ScamShield couldn't connect to the backend service.";
    description = 'Check your local network connection and verify that the backend server is running.';
  } else if (isConfigError) {
    Icon = KeyRound;
    title = 'Web investigation is not configured.';
    description = 'Add a valid SERPAPI_KEY in the backend .env file to enable live external web searches.';
  } else if (isNoResults) {
    Icon = SearchX;
    title = 'No relevant public evidence was found.';
    description = 'The query yielded zero public search records. Try specifying a clearer company name or domain.';
  } else {
    description = message.length > 160 ? 'An unexpected error occurred during investigation. Please retry.' : message;
  }

  return (
    <div className="max-w-md mx-auto glass p-6 sm:p-7 text-center space-y-4 fade-in border-rose-500/30 bg-[#140b0f]/80 shadow-[0_0_25px_rgba(239,68,68,0.15)] rounded-2xl">
      <div className="w-12 h-12 rounded-2xl bg-rose-500/15 border border-rose-500/30 flex items-center justify-center text-rose-400 mx-auto">
        <Icon className="w-6 h-6" />
      </div>

      <div className="space-y-1">
        <h3 className="text-base font-bold text-white tracking-wide">{title}</h3>
        <p className="text-xs text-slate-400 leading-relaxed max-w-sm mx-auto">
          {description}
        </p>
      </div>

      {onRetry && (
        <div className="pt-2">
          <button
            type="button"
            onClick={onRetry}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-sky-500/15 hover:bg-sky-500/25 text-sky-300 hover:text-sky-200 border border-sky-500/30 text-xs font-bold uppercase tracking-wider transition-all cursor-pointer shadow-[0_0_12px_rgba(14,165,233,0.15)]"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Try Again</span>
          </button>
        </div>
      )}
    </div>
  );
}
