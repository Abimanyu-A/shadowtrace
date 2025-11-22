import hashlib
import json
import copy
from datetime import datetime

from app.db import collection
from app.geolocation import lookup_ip

LOG_FILE = "logs/attacks.log"

def log_event(data: dict):
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
