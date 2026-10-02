/* ── API service ──────────────────────────────────────────────────────── */

import type { HealthResponse, InvestigateResponse, InputCategory } from '../types';

// Use VITE_API_URL if configured, otherwise fall back to relative /api (handled by Vite proxy in dev)
const rawBaseUrl = import.meta.env.VITE_API_URL ? String(import.meta.env.VITE_API_URL).trim() : '';
const API_BASE = (rawBaseUrl ? rawBaseUrl.replace(/\/+$/, '') : '') + '/api';

export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Backend unavailable');
  return res.json();
}

export async function investigate(
  input: string,
  category: InputCategory = 'auto',
): Promise<InvestigateResponse> {
  const res = await fetch(`${API_BASE}/investigate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input, category }),
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({ detail: 'Investigation failed' }));
    throw new Error(data.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

export async function getDemoInvestigation(demoId: string): Promise<InvestigateResponse> {
  const res = await fetch(`${API_BASE}/demo/${encodeURIComponent(demoId)}`);
  if (!res.ok) {
    const data = await res.json().catch(() => ({ detail: 'Failed to load demo investigation' }));
    throw new Error(data.detail || `HTTP ${res.status}`);
  }
  return res.json();
}
