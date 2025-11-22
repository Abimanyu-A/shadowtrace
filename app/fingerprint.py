import hashlib

def generate_fingerprint(ip: str, user_agent: str, headers: dict) -> str:
    key = f"{ip}---{user_agent}---{sorted(headers.items())}"
    return hashlib.md5(key.encode()).hexdigest()