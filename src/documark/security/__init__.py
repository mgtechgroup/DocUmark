from documark.security.scanner import scan_file
from documark.security.injection import detect_injection
from documark.security.quarantine import quarantine_file
from documark.security.reporter import report_to_virustotal

__all__ = ["check_file", "scan_file", "detect_injection", "quarantine_file", "report_to_virustotal"]


def check_file(file_path: str, vt_api_key: str | None = None) -> dict:
    """
    Full security pre-check. Fail-closed: any exception -> blocked + quarantined.
    Returns {"safe": bool, "reason": str, "details": dict}.
    """
    result: dict = {"safe": False, "reason": "unknown", "details": {}}
    try:
        scan_result = scan_file(file_path, vt_api_key)
        result["details"]["scan"] = scan_result
        if not scan_result["clean"]:
            quarantine_file(file_path, scan_result)
            if vt_api_key:
                report_to_virustotal(file_path, scan_result, vt_api_key)
            result["reason"] = f"virus/malware: {scan_result.get('threat', 'unknown')}"
            return result

        with open(file_path, encoding="utf-8", errors="replace") as f:
            content = f.read()
        injection_result = detect_injection(content)
        result["details"]["injection"] = injection_result
        if injection_result["detected"]:
            quarantine_file(file_path, injection_result)
            result["reason"] = f"prompt injection detected: {injection_result.get('pattern', 'unknown')}"
            return result

        result["safe"] = True
        result["reason"] = "clean"
    except Exception as exc:
        result["reason"] = f"scan error (fail-closed): {exc}"
        try:
            quarantine_file(file_path, {"error": str(exc)})
        except Exception:
            pass
    return result
