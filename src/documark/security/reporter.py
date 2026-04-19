import json
import os
import requests
from datetime import datetime, timezone

REPORT_LOG = os.path.join(os.path.expanduser("~"), ".documark", "reports.log")


def report_to_virustotal(file_path: str, scan_result: dict, vt_api_key: str) -> dict:
    """
    Submit file hash and findings to VirusTotal. Always logs the attempt.
    Returns {"submitted": bool, "response_code": int | None}.
    """
    sha = scan_result.get("sha256", "unknown")
    headers = {"x-apikey": vt_api_key, "Accept": "application/json"}
    outcome: dict = {"submitted": False, "response_code": None, "sha256": sha}

    try:
        resp = requests.get(
            f"https://www.virustotal.com/api/v3/files/{sha}",
            headers=headers,
            timeout=15,
        )
        outcome["response_code"] = resp.status_code
        if resp.status_code == 404 and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                upload = requests.post(
                    "https://www.virustotal.com/api/v3/files",
                    headers=headers,
                    files={"file": (os.path.basename(file_path), f)},
                    timeout=60,
                )
            outcome["response_code"] = upload.status_code
            outcome["submitted"] = upload.status_code in (200, 201)
        else:
            outcome["submitted"] = resp.status_code == 200
    except requests.RequestException as exc:
        outcome["error"] = str(exc)

    _log_report(file_path, scan_result, outcome)
    return outcome


def _log_report(file_path: str, scan_result: dict, outcome: dict) -> None:
    os.makedirs(os.path.dirname(REPORT_LOG), exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "file": file_path,
        "scan_result": scan_result,
        "report_outcome": outcome,
    }
    with open(REPORT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
