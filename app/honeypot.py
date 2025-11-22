from flask import Blueprint, request, jsonify
import jwt
import time

from app.utils import log_event, hash_payload
from app.fingerprint import generate_fingerprint

honeypot_bp = Blueprint("honeypot", __name__)

SECRET = "superfakekey"
FAKE_USER_ID = "user_948201"
FAKE_API_KEY = "api_live_3821_yz923"

recent_payloads = set()

@honeypot_bp.route("/api/login", methods=["POST"])
def fake_login():
    ip = request.remote_addr
    ua = request.headers.get("User-Agent", "unknown")

    try:
        payload = request.get_json(force=True) or {}
    except:
        payload = {}

    header_dump = dict(request.headers)

    fingerprint = generate_fingerprint(ip, ua, header_dump)
    payload_hash = hash_payload(payload)

    replay = payload_hash in recent_payloads

    recent_payloads.add(payload_hash)

    fake_token = jwt.encode(
        {"user_id": FAKE_USER_ID, "iat": int(time.time())},
        SECRET,
        algorithm="HS256",
    )

    log_event({
        "type": "LOGIN_TRAP",
        "ip": ip,
        "user_agent": ua,
        "fingerprint": fingerprint,
        "payload": payload,
        "replay_detected": replay,
        "headers": header_dump,
        "fake_token_returned": True
    })

    return jsonify({
        "status": "success",
        "token": fake_token,
        "api_key": FAKE_API_KEY,
        "message": "Welcome back! (ShadowTrace Honeypot)"
    })
