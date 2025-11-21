import hashlib
import json
from datetime import datetime

LOG_FILE = "logs/attacks.log"

def log_event(data: dict):
    data["timestamp"] = datetime.utcnow().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")


def hash_payload(payload: dict) -> str:
    """Generate a replay-detection hash."""
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()
