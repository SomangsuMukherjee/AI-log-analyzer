# AI-Powered Log Monitoring Platform

A cloud-hosted DevOps/security-focused Python platform for detecting suspicious authentication events, classifying incidents, and exposing monitoring-ready APIs.

## Live Demo

API Documentation (Swagger UI):  
https://ai-log-analyzer-jzl9.onrender.com/docs

## GitHub Repository

https://github.com/SomangsuMukherjee/AI-log-analyzer

---

## Overview

This project simulates a lightweight security monitoring and incident analysis platform.

It ingests authentication-style log data, detects suspicious activity patterns such as repeated failed logins, classifies security incidents, and returns structured recommendations through a public REST API.

The project was built to demonstrate practical DevOps, backend engineering, cloud deployment, and automation skills relevant to real-world infrastructure and security engineering roles.

---

## Features

- Detects suspicious authentication patterns
- Identifies repeated failed login attempts
- Flags potential brute-force activity
- Classifies incidents by severity
- Returns structured JSON incident reports
- Public HTTPS deployment
- REST API with interactive Swagger documentation
- Health monitoring endpoint
- Metrics endpoint for Prometheus integration
- Dockerized deployment

---

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn

### DevOps / Infrastructure
- Docker
- Docker Compose
- Render (cloud deployment)
- Prometheus-compatible metrics

### Version Control
- Git
- GitHub

---

## API Endpoints

### Health Check
```http
GET /health
```

Checks service availability.

---

### Analyze Log Content
```http
POST /analyze-text
```

Analyzes raw authentication log content.

Example request:

```json
{
  "content": "Failed login from 192.168.1.44\nFailed login from 192.168.1.44\nFailed login from 192.168.1.44\nSuccessful login from unknown location"
}
```

Example response:

```json
{
  "incident_count": 1,
  "incidents": [
    {
      "type": "Possible brute-force authentication attempt",
      "ip_address": "192.168.1.44",
      "severity": "Low",
      "event_count": 3,
      "recommendation": "Investigate the source IP, check affected accounts, and consider blocking repeated authentication attempts."
    }
  ]
}
```

---

### Upload Log File
```http
POST /upload-log
```

Accepts uploaded log files for analysis.

---

### Incident Retrieval
```http
GET /incidents
```

Returns detected incidents.

---

### Metrics
```http
GET /metrics
```

Prometheus-compatible monitoring endpoint.

---

## Architecture

```text
User / API Client
        |
        v
FastAPI Backend
        |
        v
Log Parser
        |
        v
Incident Detection Engine
        |
        v
Severity Classification
        |
        v
REST API Response
        |
        +------> Prometheus Metrics
```

---


## Future Improvements

- AI-generated incident summaries using LLMs
- IP reputation checking
- Timestamp correlation
- Suspicious geolocation detection
- PostgreSQL incident persistence
- CI/CD pipeline with GitHub Actions
- Authentication / API keys

---

## Author

Somangsu Mukherjee  
Junior DevOps / Cloud Engineer  
Košice, Slovakia
