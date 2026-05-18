import re
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

IP_PATTERN = re.compile(r"(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.|$)){4}")
FAILED_PATTERNS = ["failed password", "failed login", "authentication failure", "invalid user", "login failed"]
SUCCESS_PATTERNS = ["accepted password", "successful login", "login successful", "session opened"]


def extract_ip(line: str) -> str:
    match = IP_PATTERN.search(line)
    return match.group(0).rstrip(".") if match else "unknown"


def severity_for_failed_count(count: int) -> str:
    if count >= 10:
        return "High"
    if count >= 5:
        return "Medium"
    return "Low"


def analyze_logs(log_content: str) -> List[Dict]:
    lines = [line.strip() for line in log_content.splitlines() if line.strip()]
    failed_by_ip = defaultdict(list)
    success_by_ip = defaultdict(list)
    incidents = []

    for line in lines:
        lower = line.lower()
        ip = extract_ip(line)
        if any(pattern in lower for pattern in FAILED_PATTERNS):
            failed_by_ip[ip].append(line)
        elif any(pattern in lower for pattern in SUCCESS_PATTERNS):
            success_by_ip[ip].append(line)

    for ip, failed_events in failed_by_ip.items():
        if len(failed_events) >= 3:
            severity = severity_for_failed_count(len(failed_events))
            incidents.append({
                "type": "Possible brute-force authentication attempt",
                "ip_address": ip,
                "severity": severity,
                "event_count": len(failed_events),
                "evidence": failed_events[:8],
                "recommendation": "Investigate the source IP, check affected accounts, and consider blocking or rate-limiting repeated authentication attempts.",
                "detected_at": datetime.utcnow().isoformat() + "Z",
            })

    for ip, success_events in success_by_ip.items():
        if ip in failed_by_ip and len(failed_by_ip[ip]) >= 3:
            incidents.append({
                "type": "Successful login after repeated failures",
                "ip_address": ip,
                "severity": "High",
                "event_count": len(failed_by_ip[ip]) + len(success_events),
                "evidence": failed_by_ip[ip][:5] + success_events[:3],
                "recommendation": "Treat as possible account compromise. Review user activity, rotate credentials, and validate the login source.",
                "detected_at": datetime.utcnow().isoformat() + "Z",
            })

    return incidents
