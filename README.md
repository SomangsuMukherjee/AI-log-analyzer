# AI Log Analyzer Platform

A DevOps and security-focused Python project that detects suspicious authentication events from server logs and produces AI-assisted incident summaries. The project is containerized with Docker Compose and includes Prometheus/Grafana monitoring plus a GitHub Actions CI pipeline.

## Tech Stack

- Python
- FastAPI
- Docker / Docker Compose
- Prometheus
- Grafana
- GitHub Actions
- Optional Ollama + Mistral for local AI summaries

## Features

- Upload or paste authentication logs
- Detect possible brute-force attacks
- Detect successful login after repeated failures
- Classify incidents by severity
- Generate AI-assisted summaries using local Ollama when available
- Expose Prometheus metrics
- Simple web dashboard
- CI pipeline for backend validation and Docker image build

## Architecture

```text
User / Log File
      ↓
Frontend Dashboard
      ↓
FastAPI Backend
      ↓
Python Log Analyzer
      ↓
Optional Ollama/Mistral AI Summary
      ↓
Prometheus Metrics
      ↓
Grafana Monitoring
```

## Run Locally

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:8080
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Default Grafana login:

```text
username: admin
password: admin
```

## Test API

```bash
curl -X POST http://localhost:8000/analyze-text \
  -H "Content-Type: application/json" \
  -d '{"content":"Failed login from 192.168.1.44\nFailed login from 192.168.1.44\nFailed login from 192.168.1.44", "use_ai": false}'
```

## Optional AI Setup with Ollama

Install Ollama and pull Mistral:

```bash
ollama pull mistral
ollama run mistral
```

Then tick "Use AI summary" in the frontend or send `use_ai: true` to the API.

## Prometheus Metrics

The backend exposes metrics at:

```text
http://localhost:8000/metrics
```

Example metrics:

- `app_requests_total`
- `log_processing_seconds`
- `incidents_detected_total`

## CV Description

**AI-Powered Log Monitoring Platform**

- Built a containerized Python/FastAPI platform for analyzing authentication logs and detecting suspicious login behavior.
- Implemented rule-based detection for brute-force attempts and successful login after repeated failures.
- Integrated optional local LLM incident summarization using Ollama and Mistral.
- Added Prometheus metrics and Grafana monitoring for API and incident visibility.
- Implemented GitHub Actions CI pipeline for backend validation and Docker image builds.
