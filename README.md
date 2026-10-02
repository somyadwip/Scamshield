# 🛡️ ScamShield

> Evidence-based investigation of suspicious websites, companies and offers.

ScamShield is an open intelligence verification tool that investigates online entities, job solicitations, investment schemes, courses, and URLs using live Google Web search indices powered by **SerpApi**.

---

## 🔍 Problem

People encounter suspicious job offers, websites, shopping stores, investment schemes, and courses every day. However, traditional scam detection tools and generic AI dashboards often produce a simplistic, black-box "scam / not scam" verdict with little transparency and zero supporting evidence. 

When users are not shown the actual evidence or sources, they cannot verify whether a warning is legitimate or if a trusted brand is merely being impersonated by bad actors.

## 💡 Solution

ScamShield combines:

- **Submitted Content Analysis (Layer 1)**: In-depth heuristic extraction of inherent risk signals directly from the submitted text (e.g. upfront fee requests, guaranteed income promises, unrealistic salaries).
- **Live Web Investigation (Layer 2)**: Targeted, multi-angle search query generation powered by **SerpApi**.
- **Evidence Relevance Filtering**: Strict canonical domain matching and government notice validation that discards unrelated search noise (e.g. IRS forms, DMV pages, or incidental RFC email placeholders).
- **Relationship Classification**: Clean separation between direct fraud allegations, consumer dissatisfaction complaints, technical security/abuse notices, and brand impersonation attacks.
- **Transparent Risk Assessment**: Dual-score evidence breakdown showing exact risk points, independent sources, and the full audit trail.

## 🎯 Key Feature

**ScamShield does not simply return "SCAM".**

Instead, it transparently shows:
- **WHAT** was found (direct allegations, regulatory warnings, reviews, technical security advisories)
- **WHERE** it was found (authoritative government bodies, news organizations, company sites, review platforms)
- **WHY** it matters (risk points breakdown and investigative context)
- **WHETHER** it came from the user's input (Layer 1) or external web evidence (Layer 2)

---

## ✨ Features

- **URL Investigation**: Resolves canonical domains, checks reputation, DNS security, and abuse histories.
- **Company Investigation**: Validates business registries, customer complaints, and regulatory filings.
- **Job-Offer Analysis**: Flags fake recruitment, registration fees, and guaranteed income claims.
- **Shopping-Site Investigation**: Evaluates counterfeit complaints, non-delivery reports, and consumer reviews.
- **Investment Investigation**: Identifies unregistered funds, Ponzi promises, and crypto schemes.
- **Course Investigation**: Analyzes placement guarantees, fake accreditation, and tuition refund disputes.
- **Suspicious-Text Analysis**: Directly pastes messages, SMS alerts, or emails for structural claim parsing.
- **Content-Based Risk Signals**: Layer 1 heuristic detection of advance fees, artificial urgency, and guarantees.
- **Live Web Search**: Multi-angle targeted query generation via SerpApi.
- **Evidence Filtering**: Automatic exclusion of unrelated government pages, DMV forms, and forum noise.
- **Duplicate Detection**: Deduplication across search queries for accurate source metrics.
- **Source Classification**: Categorization into Government / Regulatory, News, Company, Review, Blog / Forum, and Other.
- **Impersonation Detection**: Distinguishes attackers spoofing reputable brands from fraud committed by the entity itself.
- **Transparent Risk Scoring**: Clear 0–100 evidence-based heuristic score with animated circular gauge.
- **Evidence Report**: Expandable cards with direct source links, snippets, and investigation rationale.

---

## 🏗️ Architecture

```
User Input (URL, Company, Offer, or Message)
  │
  ▼
Input Classification & Auto-Detection
  │
  ├─────────────────────────────────────────────────┐
  ▼                                                 ▼
[ LAYER 1: Content Signal Analysis ]     [ LAYER 2: Live Web Search ]
- Upfront fee detection                  - Targeted query generation
- Guaranteed return claims               - Real-time SerpApi Google queries
- Urgency & data requests                - Result deduplication
  │                                                 │
  │                                                 ▼
  │                                      Result Relevance Filtering
  │                                      - Canonical domain matching
  │                                      - Unrelated search noise removal
  │                                                 │
  │                                                 ▼
  │                                      Evidence Classification
  │                                      - Direct fraud vs dissatisfaction
  │                                      - Impersonation target recognition
  │                                      - Security / abuse isolation
  │                                                 │
  └────────────────────────┬────────────────────────┘
                           │
                           ▼
                      Risk Engine
            (Weighted Heuristic Evaluation)
                           │
                           ▼
            Transparent Dual-Layer Report
     (Content Score + Web Evidence Score + Sources)
```

---

## ⚡ SerpApi Usage

ScamShield uses **SerpApi** to perform live web searches for complaints, fraud reports, warnings, reviews, security information, and other relevant public evidence. Search results are then deduplicated, filtered for relevance, classified by relationship to the investigated entity, and incorporated into the external-evidence layer.

### Integration Details
- **Engine**: Google Search via SerpApi (`google-search-results` Python client library).
- **Targeted Query Generation**: Instead of generic loose queries, ScamShield constructs targeted query sets:
  - URLs: `"{domain}" scam`, `"{domain}" fraud`, `"{domain}" complaints`, `"{domain}" security`, `"{domain}" abuse`, `"{domain}" reviews`.
  - Companies: `"{company}" scam`, `"{company}" fraud`, `"{company}" complaints`, `"{company}" reviews`, `"{company}" warning`, `"{company}" news`, `"{company}" fake`.
  - Job Offers: Quotes extracted signals (e.g. `"{fee}" registration fee job scam`, `"{salary}" work from home scam`).
- **Transparency**: Every single query executed, its status, and the raw result count is displayed in the expandable "How ScamShield Investigated This" audit panel with SerpApi attribution.

---

## 🛠️ Tech Stack

### Frontend
- **React 19** & **TypeScript**
- **Vite** (Build Tool & Dev Server)
- **Tailwind CSS v4** (Cyber dark theme & glassmorphism)
- **Lucide React** (Clean cybersecurity icons, no cartoon emojis)

### Backend
- **Python 3.10+**
- **FastAPI** (REST API)
- **Uvicorn** (ASGI Server)
- **google-search-results** (Official SerpApi Python SDK)
- **Pydantic v2** (Schema validation)
- **python-dotenv** (Environment configuration)

---

## 🚀 Installation & Setup

### Prerequisites
- **Node.js** 18+ and **npm**
- **Python** 3.10+
- **SerpApi API Key** (Free tier available at [serpapi.com](https://serpapi.com))

### 1. Clone the repository
```bash
git clone https://github.com/your-username/scamshield.git
cd scamshield
```

### 2. Backend Setup

#### Windows (PowerShell):
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

#### macOS / Linux:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```
Open `backend/.env` and paste your SerpApi API key:
```env
SERPAPI_KEY=your_actual_serpapi_key_here
```
*(Note: Never commit `.env` to version control. It is already included in `.gitignore`.)*

### 4. Start the Backend API
```bash
uvicorn main:app --port 8000 --reload
```
The backend API will start at **http://127.0.0.1:8000**.
Verify health by visiting: `http://127.0.0.1:8000/api/health`

### 5. Frontend Setup (in a separate terminal)
```bash
cd frontend
npm install
npm run dev
```
The frontend application will be live at **http://localhost:5173**.

---

## 🔑 Environment Variables

### Backend Configuration (`backend/.env` or Cloud Host)
| Variable | Required | Description |
| :--- | :---: | :--- |
| `SERPAPI_KEY` | ✅ | **Server-side secret.** Your SerpApi API key from serpapi.com. Never exposed to the frontend or browser bundle. |
| `FRONTEND_URL` | ⚠️ | Production URL of your deployed frontend (e.g. `https://scamshield.onrender.com`) for CORS authorization. In development, defaults to `http://localhost:5173`. |
| `PORT` | ❌ | Port to bind the server to. Cloud platforms (like Render) supply this automatically. Defaults to `8000`. |

### Frontend Configuration (`frontend/.env` or Cloud Host)
| Variable | Required | Description |
| :--- | :---: | :--- |
| `VITE_API_URL` | ⚠️ | Full URL of the deployed backend service (e.g. `https://scamshield-backend.onrender.com`). In local development, defaults to relative `/api` (proxied by Vite to port 8000). |
| `VITE_GITHUB_URL` | ❌ | Optional link to your public GitHub repository for the footer navigation. |

---

## 🌐 Public Deployment Guide

ScamShield is engineered to be deployed as two decoupled services:
1. **Backend Web Service**: Python FastAPI application deployed on a cloud host (such as Render, Railway, or Fly.io) that binds to `0.0.0.0:$PORT`.
2. **Frontend Static Site**: React + Vite SPA built to static HTML/JS/CSS assets and distributed via a CDN (Render Static Sites, Vercel, Netlify, or Cloudflare Pages).

### Automated Blueprint (`render.yaml`)
A ready-to-use [`render.yaml`](render.yaml) is included in the root directory. To deploy via Render Blueprint:
1. Push your repository to GitHub.
2. In the [Render Dashboard](https://dashboard.render.com), click **New** → **Blueprint**.
3. Connect your repository. Render will automatically parse `render.yaml` and configure both services.
4. When prompted, enter your `SERPAPI_KEY` under the backend environment settings.

---

### Manual Deployment Steps

#### Step 1: Deploy the Backend (Render Web Service)
1. In Render, select **New** → **Web Service**.
2. Connect your GitHub repository.
3. Configure the service:
   - **Name**: `scamshield-backend`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `SERPAPI_KEY`: *(Paste your private SerpApi key)*
   - `FRONTEND_URL`: `https://your-frontend-subdomain.onrender.com` *(You can update this after Step 2)*
5. Click **Create Web Service**. Note the backend URL (e.g. `https://scamshield-backend.onrender.com`).
6. Verify deployment by visiting: `https://scamshield-backend.onrender.com/api/health`

#### Step 2: Deploy the Frontend (Render Static Site)
1. In Render, select **New** → **Static Site**.
2. Connect the same repository.
3. Configure the static site:
   - **Name**: `scamshield-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add Environment Variables:
   - `VITE_API_URL`: `https://scamshield-backend.onrender.com` *(The URL from Step 1)*
5. Under **Redirects/Rewrites**, add a rewrite rule:
   - **Source**: `/*`
   - **Destination**: `/index.html`
   - **Action**: `Rewrite`
6. Click **Create Static Site**.

#### How the Frontend Connects to the Backend in Production
- The browser frontend loads from the CDN and reads `VITE_API_URL` to send API requests to `https://scamshield-backend.onrender.com/api/investigate`.
- The FastAPI backend validates that the `Origin` header matches `FRONTEND_URL` and processes the request.
- The `SERPAPI_KEY` remains securely stored in the backend environment and is used to communicate directly with SerpApi over server-side TLS. The client never touches or receives the API key.

---

## 📖 Usage Examples

### Investigating a Known Company
Enter:
```
Microsoft
```
- **Result**: Low Risk (0/100).
- **Behavior**: Recognizes that Microsoft is a target of phishing and tech-support impersonation schemes, rather than penalizing Microsoft as a fraudulent actor.

### Investigating a Website
Enter:
```
https://example.com
```
- **Result**: Low Risk (1/100).
- **Behavior**: Extracts the canonical domain `example.com`, filters out unrelated IRS/DMV tax refund pages, separates technical RFC security notices (+0 risk points), and lists filtered results transparently.

### Investigating a Suspicious Job Offer
Paste the full solicitation text into the search bar:
```
Earn ₹50,000 per month from home. No experience required. Pay ₹999 registration fee to start. Guaranteed income.
```
- **Result**: High Risk (~72/100).
- **Behavior**: Layer 1 extracts 3 critical content signals (`UPFRONT_PAYMENT`, `GUARANTEED_INCOME`, `UNREALISTIC_EARNINGS`) with direct quotes and risk points. Layer 2 queries Google for employment advisory notices from the FTC and regulatory bodies.

---

## ⚖️ Risk Model

The ScamShield risk score (0–100) is an **internal evidence-based heuristic**, NOT a mathematical probability of fraud.

$$\text{Overall Score} = \min(100, \text{Content Signals Score} + \text{External Web Evidence Score})$$

### Score Tiers
- **0 – 24**: **LOW RISK** (No credible adverse evidence or verified entity)
- **25 – 49**: **MODERATE RISK** (Consumer dissatisfaction, critical reviews, or cautionary signals)
- **50 – 74**: **HIGH RISK** (Direct advance-fee requests, multiple complaints, or regulatory warnings)
- **75 – 100**: **VERY HIGH RISK** (Severe fraud allegations, confirmed deceptive practices, or regulatory bans)
- **INSUFFICIENT EVIDENCE**: Displayed when search records are too sparse to make a conclusive assessment, avoiding false accusations.

### Key Risk Heuristics
1. **Ordinary Complaints ≠ Scams**: Software bugs, customer support delays, or refund disputes are classified as `CONSUMER_DISSATISFACTION` and contribute 0 risk points.
2. **Impersonation Protection**: When scammers spoof a legitimate company (e.g. fake Microsoft support calls), the entity is tagged as `IMPERSONATION_TARGET` (+0 risk points).
3. **Security Reports ≠ Fraud**: Technical DNS complaints, vulnerability disclosures, and network abuse reports are isolated under `SECURITY_REPORT` (+0 scam points).

---

## 🏆 Hackathon Spotlight: Why SerpApi?

Live web search is indispensable for threat intelligence and scam detection:

1. **Static Datasets Go Stale Fast**: Fraudulent domains, fake recruitment agencies, and Ponzi schemes appear and disappear in days. Static blacklists cannot keep up.
2. **Real-Time Consumer Grievances**: When a new scam surfaces, victims discuss it on forums, Reddit, and review sites days before official regulatory notices are issued.
3. **Nuanced Reputation Signals**: Assessing legitimacy requires reading fresh reviews, news coverage, and corporate filings.

**SerpApi** delivers the real-time Google search infrastructure that makes this multi-angle evidentiary investigation possible without scraping friction or rate limits.

---

## 🧪 Demo Scenarios for Evaluators

### Scenario 1: Suspicious Job Offer (Advance-Fee Scheme)
- **Input**: `"Earn ₹50,000 per month from home. No experience required. Pay ₹999 registration fee to start. Guaranteed income."`
- **Expected Behavior**: Immediately flags 3 Layer 1 risk signals (upfront payment, guaranteed income, unrealistic earnings), quotes the text, and assigns ~72/100 HIGH RISK.

### Scenario 2: Known Enterprise (Impersonation Target)
- **Input**: `"Microsoft"`
- **Expected Behavior**: Identifies 12+ public sources discussing scammers impersonating Microsoft. Awards 0 scam risk points and displays the `Impersonation Target Recognized` badge.

### Scenario 3: Unknown Entity (Insufficient Evidence)
- **Input**: `"XYZ Super Mega Careers 928374"`
- **Expected Behavior**: Filters 40+ unrelated search results (such as government grant programs containing "mega") and renders a clean **0/100 LOW RISK / INSUFFICIENT EVIDENCE** verdict rather than fabricating false evidence.

---

## ⚠️ Limitations

- **Public Index Availability**: Search results reflect public online records indexed by Google; unindexed private communications cannot be detected.
- **Ambiguity in Content**: A low score does not guarantee legitimacy, and a high score does not independently establish criminal guilt.
- **Heuristic Nature**: ScamShield provides investigative research based on patterns and public records, not absolute certainty.

---

## 🛡️ Responsible Use

> **Disclaimer**: ScamShield is an informational research and risk investigation tool. It does not provide legal, financial, or cyber incident response advice. Users should always review the underlying primary sources before taking financial, employment, or purchasing decisions.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
