import hashlib
import json
import copy
from datetime import datetime
import os

from app.db import collection
from app.geolocation import lookup_ip

LOG_FILE = "logs/attacks.log"

def ensure_log_file():
    log_dir = os.path.dirname(LOG_FILE)

    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("") 

def log_event(data: dict):
    ensure_log_file()
    
    data["timestamp"] = datetime.utcnow().isoformat()
    
    geo = lookup_ip(data["ip"])
    data["geolocation"] = geo
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
        
    if collection is not None:
        try:
            collection.insert_one(copy.deepcopy(data))
        except Exception as e:
            print("MongoDB Insert Error: ", e)
            
    print("HONEYPOT-EVENT: ", json.dumps(data))

def hash_payload(payload: dict) -> str:
    """Generate a replay-detection hash."""
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()
