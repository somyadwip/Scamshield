import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

tests = [
    ("TEST 1", "Earn ₹50,000 per month from home. No experience required. Pay ₹999 registration fee to start. Guaranteed income."),
    ("TEST 2", "Microsoft"),
    ("TEST 3", "XYZ Super Mega Careers 928374"),
    ("TEST 4", "Join our company as a software engineer. Salary ₹8 LPA. Apply through our official website."),
]

for label, query in tests:
    print(f"\n=======================================================", flush=True)
    print(f"{label}: \"{query}\"", flush=True)
    print(f"=======================================================", flush=True)
    payload = json.dumps({"input": query, "category": "auto"}).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/investigate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"Detected Type: {data.get('detected_type')}", flush=True)
            content_signals = data.get("content_signals", [])
            print(f"Content Signals ({len(content_signals)} found):", flush=True)
            for s in content_signals:
                print(f"  - [{s.get('category')}] {s.get('title')}: \"{s.get('quote')}\" (+{s.get('risk_contribution')} pts)", flush=True)
            print(f"Content Signal Score: {data.get('content_signal_score')}", flush=True)
            print(f"External Evidence Items: {len(data.get('evidence', []))}", flush=True)
            print(f"Web Evidence Score: {data.get('web_evidence_score')}", flush=True)
            print(f"Overall Risk Score: {data.get('overall_risk_score')}", flush=True)
            print(f"Risk Level: {data.get('risk_level')}", flush=True)
            print(f"Confidence: {data.get('confidence')}", flush=True)
            print(f"Independent Sources: {data.get('unique_sources')}", flush=True)
            print(f"Summary: {data.get('summary')}", flush=True)
    except Exception as exc:
        print(f"Error during {label}: {exc}", file=sys.stderr, flush=True)
