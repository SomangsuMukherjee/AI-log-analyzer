from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List
import time

from analyzer import analyze_logs
from ai_summary import summarize_incident

app = FastAPI(
    title="AI Log Analyzer Platform",
    description="A DevOps/security-focused Python platform for detecting suspicious log events and generating AI-assisted incident summaries.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUEST_COUNT = Counter("app_requests_total", "Total API requests", ["endpoint"])
PROCESSING_TIME = Histogram("log_processing_seconds", "Time spent processing log files")
INCIDENT_COUNT = Counter("incidents_detected_total", "Total incidents detected", ["severity"])

INCIDENTS = []

class LogText(BaseModel):
    content: str
    use_ai: bool = False

@app.get("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()
    return {"status": "ok", "service": "ai-log-analyzer"}

@app.post("/analyze-text")
def analyze_text(payload: LogText):
    REQUEST_COUNT.labels(endpoint="/analyze-text").inc()
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Log content cannot be empty")

    start = time.time()
    incidents = analyze_logs(payload.content)

    for incident in incidents:
        if payload.use_ai:
            incident["ai_summary"] = summarize_incident(incident)
        INCIDENT_COUNT.labels(severity=incident["severity"]).inc()
        INCIDENTS.append(incident)

    PROCESSING_TIME.observe(time.time() - start)
    return {"incident_count": len(incidents), "incidents": incidents}

@app.post("/upload-log")
async def upload_log(file: UploadFile = File(...), use_ai: bool = False):
    REQUEST_COUNT.labels(endpoint="/upload-log").inc()
    if not file.filename.endswith((".txt", ".log", ".json")):
        raise HTTPException(status_code=400, detail="Only .txt, .log, and .json files are supported")

    content_bytes = await file.read()
    content = content_bytes.decode("utf-8", errors="ignore")

    start = time.time()
    incidents = analyze_logs(content)

    for incident in incidents:
        if use_ai:
            incident["ai_summary"] = summarize_incident(incident)
        INCIDENT_COUNT.labels(severity=incident["severity"]).inc()
        INCIDENTS.append(incident)

    PROCESSING_TIME.observe(time.time() - start)
    return {"filename": file.filename, "incident_count": len(incidents), "incidents": incidents}

@app.get("/incidents")
def get_incidents():
    REQUEST_COUNT.labels(endpoint="/incidents").inc()
    return {"total": len(INCIDENTS), "incidents": INCIDENTS[-50:]}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
