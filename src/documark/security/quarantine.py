import json
import os
import shutil
import time
from datetime import datetime, timezone

QUARANTINE_DIR = os.path.join(os.path.expanduser("~"), ".documark", "quarantine")
LOG_FILE = os.path.join(os.path.expanduser("~"), ".documark", "security.log")


def quarantine_file(file_path: str, reason: dict) -> str:
    """
    Move file to sandboxed quarantine directory and log the event.
    Returns the quarantine path (or error string if move fails).
    """
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    safe_name = f"{int(time.time())}_{os.path.basename(file_path)}"
    dest = os.path.join(QUARANTINE_DIR, safe_name)

    try:
        shutil.move(file_path, dest)
    except Exception as exc:
        dest = f"move_failed: {exc}"

    _append_log({
        "timestamp": timestamp,
        "original_path": file_path,
        "quarantine_path": dest,
        "reason": reason,
    })
    return dest


def _append_log(event: dict) -> None:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
