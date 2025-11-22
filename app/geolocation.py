import requests
import functools

@functools.lru_cache(maxsize=500)
def lookup_ip(ip: str):
    try:
        resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        if resp.status_code == 200:
            data = resp.json()

            return {
                "ip": ip,
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country", "Unknown"),
                "org": data.get("org", "Unknown"),
                "loc": data.get("loc", "0,0")
            }

    except Exception:
        pass

    return {
        "ip": ip,
        "city": "Unknown",
        "region": "Unknown",
        "country": "Unknown",
        "org": "Unknown",
        "loc": "0,0"
    }
