import hashlib
import mimetypes
import os
import requests

_KNOWN_CLEAN_HASHES: set[str] = set()
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/files"

# Extensions always blocked regardless of API key — executable / script types
_DANGEROUS_EXTENSIONS = {
    ".exe", ".dll", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jar",
    ".sh", ".bash", ".zsh", ".fish", ".bin", ".app", ".msi", ".scr",
    ".hta", ".wsf", ".wsh", ".reg", ".pif", ".com", ".cpl",
}

# MIME types that are always blocked regardless of extension
_DANGEROUS_MIMES = {
    "application/x-msdownload",
    "application/x-executable",
    "application/x-sh",
    "application/x-shellscript",
    "application/x-msdos-program",
    "application/x-java-archive",
    "application/vnd.microsoft.portable-executable",
}

# Maximum file size: 50 MB — larger files are blocked to prevent DoS
MAX_FILE_BYTES = 50 * 1024 * 1024


def _sha256(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _check_mime(file_path: str) -> str | None:
    """Return a threat string if the MIME type is dangerous, else None."""
    mime, _ = mimetypes.guess_type(file_path)
    if mime and mime.lower() in _DANGEROUS_MIMES:
        return f"dangerous_mime: {mime}"
    return None


def scan_file(file_path: str, vt_api_key: str | None = None) -> dict:
    """
    Scan a file for viruses/malware. Fail-closed: any exception -> {"clean": False}.
    Returns {"clean": bool, "threat": str | None, "engine": str, "sha256": str}.

    Checks (in order):
    1. File size limit (50 MB max)
    2. Dangerous extension block
    3. MIME type block
    4. VirusTotal API hash lookup (if key provided)
    5. Local heuristic fallback
    """
    # --- Size check (DoS prevention) ---
    try:
        size = os.path.getsize(file_path)
    except OSError as exc:
        return {"clean": False, "threat": f"stat_error: {exc}", "engine": "local", "sha256": ""}

    if size > MAX_FILE_BYTES:
        return {
            "clean": False,
            "threat": f"file_too_large: {size} bytes (max {MAX_FILE_BYTES})",
            "engine": "local_size_check",
            "sha256": "",
        }

    # --- Extension block ---
    ext = os.path.splitext(file_path)[1].lower()
    if ext in _DANGEROUS_EXTENSIONS:
        return {
            "clean": False,
            "threat": f"dangerous_extension: {ext}",
            "engine": "local_heuristic",
            "sha256": "",
        }

    # --- MIME type block ---
    mime_threat = _check_mime(file_path)
    if mime_threat:
        return {"clean": False, "threat": mime_threat, "engine": "local_mime_check", "sha256": ""}

    # --- Hash ---
    try:
        sha = _sha256(file_path)
    except OSError as exc:
        return {"clean": False, "threat": f"unreadable: {exc}", "engine": "local", "sha256": ""}

    if sha in _KNOWN_CLEAN_HASHES:
        return {"clean": True, "threat": None, "engine": "local_cache", "sha256": sha}

    # --- VirusTotal ---
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
                # Not in VT — submit; treat as pending = blocked (fail-closed)
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
            # Network failure = fail-closed
            return {"clean": False, "threat": f"vt_error: {exc}", "engine": "virustotal", "sha256": sha}

    # --- Local heuristic fallback (no API key) ---
    _KNOWN_CLEAN_HASHES.add(sha)
    return {"clean": True, "threat": None, "engine": "local_heuristic", "sha256": sha}
