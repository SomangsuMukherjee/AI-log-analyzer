import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")


def fallback_summary(incident: dict) -> str:
    return (
        f"{incident['severity']} severity incident detected: {incident['type']} from "
        f"IP {incident['ip_address']} with {incident['event_count']} related events. "
        f"Recommended action: {incident['recommendation']}"
    )


def summarize_incident(incident: dict) -> str:
    """Use local Ollama if available. Fall back gracefully if Ollama is not running."""
    prompt = f"""
You are a junior SOC analyst assistant. Summarize this security incident in 3 short bullet points.
Include likely cause, risk level, and recommended action.

Incident:
{incident}
"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=15,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip() or fallback_summary(incident)
    except Exception:
        return fallback_summary(incident)
