"""ScamShield – FastAPI backend.

Entry point: uvicorn main:app --reload --port 8000
"""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import (
    DetectedType,
    ErrorResponse,
    EvidenceRelationship,
    HealthResponse,
    InputCategory,
    InvestigateRequest,
    InvestigateResponse,
    QueryRecord,
)
from services.content_analyzer import analyze_content
from services.evidence_extractor import detect_contradictions, extract_evidence
from services.query_generator import generate_queries
from services.risk_engine import build_indicators, calculate_risk, generate_summary
from services.serpapi_service import SerpApiError, serpapi_service
from services.demo_service import DEMO_DATASETS, get_demo_investigation
from utils.input_helpers import detect_input_type, normalize_input

# ── Bootstrap ───────────────────────────────────────────────────────────────────

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger("scamshield")

app = FastAPI(
    title="ScamShield API",
    version="1.0.0",
    description="Investigate suspicious websites, companies and offers using web evidence.",
)

# ── CORS Configuration ────────────────────────────────────────────────────────
default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

frontend_url_env = os.getenv("FRONTEND_URL", "").strip()
allowed_origins = list(default_origins)
if frontend_url_env:
    for origin in frontend_url_env.split(","):
        cleaned = origin.strip().rstrip("/")
        if cleaned and cleaned not in allowed_origins:
            allowed_origins.append(cleaned)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ──────────────────────────────────────────────────────────────────────

@app.get("/api/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        serpapi_configured=serpapi_service.is_configured(),
    )


# ── Demo ────────────────────────────────────────────────────────────────────────

@app.get("/api/demo/{demo_id}", response_model=InvestigateResponse)
async def get_demo(demo_id: str):
    return get_demo_investigation(demo_id)


# ── Investigate ─────────────────────────────────────────────────────────────────

@app.post("/api/investigate", response_model=InvestigateResponse)
async def investigate(req: InvestigateRequest):
    raw_input = req.input.strip()

    if not raw_input:
        raise HTTPException(status_code=400, detail="Input cannot be empty.")

    # 1. Normalize & detect type
    normalized = normalize_input(raw_input)
    detected_type = detect_input_type(raw_input, req.category)

    # 1b. Content Analysis (Extract signals directly from submitted text)
    content_signals, content_signal_score = analyze_content(raw_input)
    if content_signals:
        logger.info("Found %d content signals in submitted text (score=%d)", len(content_signals), content_signal_score)

    # If SerpApi is not configured, gracefully return a demo investigation
    if not serpapi_service.is_configured():
        logger.info("SerpApi key not configured – providing demo showcase for: %s", normalized)
        return get_demo_investigation(normalized)

    logger.info("Investigating: %s  (type=%s)", normalized, detected_type.value)

    # 2. Generate queries
    queries = generate_queries(normalized, detected_type)
    logger.info("Generated %d queries", len(queries))

    # 3. Execute searches via SerpApi
    all_organic_results: list[dict] = []
    query_records: list[QueryRecord] = []

    for q in queries:
        try:
            data = serpapi_service.search(q)
            organic = data.get("organic_results", [])
            all_organic_results.extend(organic)

            # Also grab knowledge graph if present
            kg = data.get("knowledge_graph")
            if kg:
                kg_result = {
                    "title": kg.get("title", ""),
                    "link": kg.get("website", kg.get("source", {}).get("link", "")),
                    "snippet": kg.get("description", ""),
                    "displayed_link": kg.get("website", ""),
                }
                if kg_result["link"]:
                    all_organic_results.append(kg_result)

            query_records.append(QueryRecord(query=q, result_count=len(organic), status="completed"))
            logger.info("  ✓ '%s' → %d results", q, len(organic))

        except SerpApiError as exc:
            logger.warning("  ✗ '%s' → %s", q, exc.message)
            query_records.append(QueryRecord(query=q, result_count=0, status=f"error: {exc.error_type}"))

            # If the key is missing/invalid, fail fast
            if exc.error_type in ("api_key_missing", "invalid_api_key"):
                raise HTTPException(
                    status_code=503,
                    detail=exc.message,
                )

    # 4. Try a news search (1 extra query, for named entities and short titles only)
    if len(normalized.split()) <= 6 and detected_type in (DetectedType.COMPANY, DetectedType.INVESTMENT, DetectedType.SHOPPING, DetectedType.COURSE):
        news_query = f'"{normalized}" news'
        try:
            news_data = serpapi_service.search_news(news_query, num=5)
            news_results = news_data.get("news_results", [])
            # Convert news results to organic-like dicts
            for nr in news_results:
                all_organic_results.append({
                    "title": nr.get("title", ""),
                    "link": nr.get("link", ""),
                    "snippet": nr.get("snippet", ""),
                    "displayed_link": nr.get("source", ""),
                })
            query_records.append(QueryRecord(query=news_query, result_count=len(news_results), status="completed"))
        except SerpApiError:
            query_records.append(QueryRecord(query=news_query, result_count=0, status="error"))

    # 5. Extract evidence with relationship classification & canonical deduplication
    evidence, sources, unique_sources, dups_removed, filtered_unrelated_count, filtered_items = extract_evidence(all_organic_results, normalized)

    # 6. Detect contradictions
    contradictions = detect_contradictions(evidence, normalized)

    # 7. Calculate dual-layer risk
    overall_score, content_score, web_score, level, confidence = calculate_risk(
        evidence,
        contradictions,
        unique_sources=unique_sources,
        content_signal_score=content_signal_score,
    )

    # 8. Build indicators
    indicators = build_indicators(evidence, contradictions)

    # 9. Generate dynamic summary
    summary = generate_summary(
        normalized,
        level,
        evidence,
        contradictions,
        confidence,
        unique_sources=unique_sources,
        content_signals=content_signals,
        content_signal_score=content_score,
        web_evidence_score=web_score,
    )

    impersonation_target_count = sum(1 for e in evidence if e.relationship == EvidenceRelationship.IMPERSONATION_TARGET)

    return InvestigateResponse(
        input=raw_input,
        normalized_input=normalized,
        detected_type=detected_type,
        risk_score=overall_score,
        overall_risk_score=overall_score,
        content_signal_score=content_score,
        web_evidence_score=web_score,
        risk_level=level,
        confidence=confidence,
        summary=summary,
        content_signals=content_signals,
        indicators=indicators,
        evidence=evidence,
        sources=sources,
        queries=query_records,
        search_count=len(query_records),
        unique_sources=unique_sources,
        relevant_evidence_count=len(evidence),
        relevant_unique_sources=unique_sources,
        filtered_unrelated_count=filtered_unrelated_count,
        filtered_results=filtered_items,
        duplicate_results_removed=dups_removed,
        impersonation_target_count=impersonation_target_count,
        contradictions=contradictions,
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=False)

