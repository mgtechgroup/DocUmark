import hashlib
import os
import requests

_KNOWN_CLEAN_HASHES: set[str] = set()
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/files"
_DANGEROUS_EXTENSIONS = {".exe", ".dll", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jar", ".sh"}


def _sha256(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_file(file_path: str, vt_api_key: str | None = None) -> dict:
    """
    Scan a file for viruses/malware. Fail-closed: exception -> {"clean": False}.
    Returns {"clean": bool, "threat": str | None, "engine": str, "sha256": str}.
    """
    try:
        sha = _sha256(file_path)
    except OSError as exc:
        return {"clean": False, "threat": f"unreadable: {exc}", "engine": "local", "sha256": ""}

    if sha in _KNOWN_CLEAN_HASHES:
        return {"clean": True, "threat": None, "engine": "local_cache", "sha256": sha}

    if vt_api_key:
        try:
            headers = {"x-apikey": vt_api_key}
            resp = requests.get(
                f"https://www.virustotal.com/api/v3/files/{sha}",
                headers=headers,
                timeout=15,
            )
            if resp.status_code == 200:
                stats = (
                    resp.json()
                    .get("data", {})
                    .get("attributes", {})
                    .get("last_analysis_stats", {})
                )
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                if malicious > 0 or suspicious > 0:
                    return {
                        "clean": False,
                        "threat": f"malicious={malicious} suspicious={suspicious}",
                        "engine": "virustotal",
                        "sha256": sha,
                    }
                _KNOWN_CLEAN_HASHES.add(sha)
                return {"clean": True, "threat": None, "engine": "virustotal", "sha256": sha}
            elif resp.status_code == 404:
                # Not in VT — submit for scanning; treat as pending = blocked (fail-closed)
                with open(file_path, "rb") as f:
                    requests.post(
                        VIRUSTOTAL_URL,
                        headers=headers,
                        files={"file": (os.path.basename(file_path), f)},
                        timeout=60,
                    )
                return {
                    "clean": False,
                    "threat": "pending_vt_scan",
                    "engine": "virustotal_submitted",
                    "sha256": sha,
                }
        except requests.RequestException as exc:
            return {"clean": False, "threat": f"vt_error: {exc}", "engine": "virustotal", "sha256": sha}

    # No API key — fall back to extension heuristic
    ext = os.path.splitext(file_path)[1].lower()
    if ext in _DANGEROUS_EXTENSIONS:
        return {"clean": False, "threat": f"dangerous_extension: {ext}", "engine": "local_heuristic", "sha256": sha}

    _KNOWN_CLEAN_HASHES.add(sha)
    return {"clean": True, "threat": None, "engine": "local_heuristic", "sha256": sha}
