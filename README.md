# 🛡️ ShadowTrace Honeypot v1  
### A deceptive API honeypot with attacker fingerprinting, geolocation intelligence, and a live threat dashboard.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-red)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

ShadowTrace is a **lightweight deception honeypot** designed to log attacker behavior, fingerprint hostile clients, detect replay attacks, enrich IP geolocation, persist logs to MongoDB, and visualize global attack activity through a **real-time, auto-refreshing dashboard**.

# Features

### Deception Engine  
- Fake login API endpoint (`/api/login`)  
- Returns **realistic fake JWT tokens** + **fake API keys**  
- Lures attackers into multi-step exploitation attempts  

### Attacker Fingerprinting  
Automatically generates unique fingerprints using:
- IP address  
- User-Agent  
- Header patterns  
- Payload signature  

### Replay Detection  
Detects repeated payloads using SHA-256 hashes.

### Geolocation Intelligence  
Using ipinfo.io:
- City  
- Region  
- Country  
- Latitude / longitude  
- ISP / Organization  

### Persistent Logging  
All attacker hits stored in:
- **MongoDB Atlas (cloud)**  
- Optional local log file (`logs/attacks.log`)  

### Threat Dashboard  
Dashboard includes:
- Global **Leaflet map**  
- **Markers** with popup details  
- **Auto-refresh every 10 seconds**  
- Filtering by:
  - IP  
  - Fingerprint  
- Secure admin login  

### Data Table  
Shows:
- IP  
- Location (City, Country)  
- ISP  
- Fingerprint  
- Replay flag  
- Payload  
- Timestamp  

---

# Screenshots

### Dashboard Table  
![dashboard](screenshots/table.png)

### Admin Login  
![login](screenshots/login.png)

---

# Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** TailwindCSS + Leaflet
- **Database:** MongoDB Atlas
- **Deployment:** Render + Gunicorn
- **Logging:** JSON logs, persistent storage
- **Security:** Fake token deception, fingerprinting, replay detection

---

# API Endpoints

## **POST /api/login**
Fake login endpoint used as honeypot trap.

### Request Body:
```json
{
  "email": "admin",
  "password": "123"
}
````

### Response:

```json
{
  "status": "success",
  "token": "<fake-jwt>",
  "api_key": "api_live_xxx",
  "message": "Welcome back! (ShadowTrace Honeypot)"
}
```

Each request is logged with:

* IP
* User-Agent
* Fingerprint
* Replay status
* Payload
* Geolocation

---

# Dashboard

## **GET /dashboard**

Live threat dashboard:

* Global map
* Heatmap
* Markers
* Table with pagination
* Filters
* Auto-refresh

---

# Local Development Setup

### 1️ Clone the repo

```bash
git clone https://github.com/Abimanyu-A/shadowtrace.git
cd shadowtrace
```

### 2️ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3️ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️ Create `.env` file

```
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
ADMIN_USERNAME=admin
ADMIN_PASSWORD=StrongPassword123
```

> Don’t commit `.env` — it’s ignored by `.gitignore`.

### 5️ Start the server

```bash
python run.py
```

### 6️ Visit:

Dashboard:

```
http://localhost:5000/dashboard
```

Honeypot endpoint:

```
POST http://localhost:5000/api/login
```

---

# Future Roadmap

* 🟦 AI-based attack clustering
* 🟩 HTML/JS replay visualization
* 🟧 Add WebSocket-based live streaming
* 🟥 Integrate VirusTotal / AbuseIPDB reputation
* 🟨 Export logs to CSV/JSON
* 🟪 IP/ISP-level filters

---

# Contributing

Pull requests are welcome!
Open an issue if you'd like to request a feature.

---

# 📜 License

This project is released under the **MIT License**.

---

# ⭐ Support

If you found this project useful, please ⭐ star the repo!

```

---

