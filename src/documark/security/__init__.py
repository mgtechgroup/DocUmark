import json
import os
from documark.security.scanner import scan_file
from documark.security.injection import detect_injection
from documark.security.quarantine import quarantine_file, LOG_FILE
from documark.security.reporter import report_to_virustotal

__all__ = [
    "check_file",
    "security_stats",
    "scan_file",
    "detect_injection",
    "quarantine_file",
    "report_to_virustotal",
]


def check_file(file_path: str, vt_api_key: str | None = None) -> dict:
    """
    Full security pre-check pipeline. Fail-closed: any exception -> blocked + quarantined.

    Pipeline:
      1. Virus/malware scan (VirusTotal API or local heuristic)
      2. Prompt injection detection
      3. Quarantine + log + report if blocked

    Returns {"safe": bool, "reason": str, "details": dict}.
    """
    result: dict = {"safe": False, "reason": "unknown", "details": {}}
    try:
        # Stage 1: Virus scan
        scan_result = scan_file(file_path, vt_api_key)
        result["details"]["scan"] = scan_result
        if not scan_result["clean"]:
            dest = quarantine_file(file_path, scan_result)
            result["details"]["quarantine_path"] = dest
            if vt_api_key:
                report_result = report_to_virustotal(file_path, scan_result, vt_api_key)
                result["details"]["vt_report"] = report_result
            result["reason"] = f"virus/malware: {scan_result.get('threat', 'unknown')}"
            return result

        # Stage 2: Prompt injection detection (read as text)
        with open(file_path, encoding="utf-8", errors="replace") as f:
            content = f.read()
        injection_result = detect_injection(content)
        result["details"]["injection"] = injection_result
        if injection_result["detected"]:
            dest = quarantine_file(file_path, injection_result)
            result["details"]["quarantine_path"] = dest
            result["reason"] = (
                f"prompt injection detected: {injection_result.get('pattern', 'unknown')}"
            )
            return result

        result["safe"] = True
        result["reason"] = "clean"

    except Exception as exc:
        # Fail-closed: any unexpected error = file is blocked
        result["reason"] = f"scan error (fail-closed): {exc}"
        try:
            dest = quarantine_file(file_path, {"error": str(exc), "type": "scan_exception"})
            result["details"]["quarantine_path"] = dest
        except Exception:
            pass

    return result


def security_stats() -> dict:
    """
    Return counts from the security log: total quarantined, by reason category.
    """
    stats: dict = {
        "total_quarantined": 0,
        "virus_malware": 0,
        "prompt_injection": 0,
        "scan_error": 0,
    }
    if not os.path.exists(LOG_FILE):
        return stats

    with open(LOG_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                stats["total_quarantined"] += 1
                reason = event.get("reason", {})
                if isinstance(reason, dict):
                    if reason.get("clean") is False:
                        stats["virus_malware"] += 1
                    elif reason.get("detected"):
                        stats["prompt_injection"] += 1
                    elif "error" in reason:
                        stats["scan_error"] += 1
            except (json.JSONDecodeError, AttributeError):
                pass

    return stats
