# 📸 ScamShield Screenshots

This directory contains visual previews of ScamShield for documentation and hackathon submission.

| File Name | View Description |
| :--- | :--- |
| `home.png` | Landing page hero with cyber dark design, search bar, capability chips, and 5-stage workflow pipeline. |
| `investigation.png` | Live investigation sequence displaying progress across input parsing, signal extraction, and SerpApi searches. |
| `evidence.png` | Two-layer evidence dashboard showing Results Hero, Risk Score gauge, Content Signals (Layer 1), and Web Evidence (Layer 2). |

### Capturing Screenshots for Submission
1. Start the backend: `cd backend && uvicorn main:app --port 8000`
2. Start the frontend: `cd frontend && npm run dev`
3. Navigate to `http://localhost:5173/`
4. Capture full-resolution (1920×1080 or 1440×900) PNG images:
   - `home.png`: Initial landing page before search.
   - `investigation.png`: Active loading state during a search.
   - `evidence.png`: Investigation result for demo cases (e.g. `Microsoft` or the suspicious job offer).
