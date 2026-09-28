
from flask import Flask, jsonify, send_from_directory, abort
from pathlib import Path
import random, threading, time

app = Flask(__name__, static_folder="static")
BASE = Path(__file__).parent

SITE_NAMES = {
    "nexus":"NEXUS","pulse":"PULSE","bytewire":"BYTEWIRE","voltage":"VOLTAGE",
    "streambox":"STREAMBOX","grid":"GRID","chatter":"CHATTER","cloudvault":"CLOUDVAULT",
    "travelix":"TRAVELIX","status":"STATUS"
}

state = {k: {"name": v, "load": random.randint(5,18), "connections": random.randint(80,500),
             "state":"ONLINE", "sim": False, "ends": 0} for k,v in SITE_NAMES.items()}

lock = threading.Lock()

def worker(key, seconds):
    end = time.time() + seconds
    with lock:
        state[key]["sim"] = True
        state[key]["ends"] = end
    while time.time() < end:
        with lock:
            left = end - time.time()
            progress = 1 - max(0, left) / seconds
            # purely simulated values; no network traffic is generated
            load = min(99, int(18 + progress * 81 + random.randint(-3,3)))
            state[key]["load"] = load
            state[key]["connections"] = int(120 + progress * 4800 + random.randint(0,250))
            state[key]["state"] = "DEGRADED" if load < 70 else ("OVERLOADED" if load < 96 else "OFFLINE")
        time.sleep(.5)
    with lock:
        state[key].update(load=12, connections=random.randint(80,400), state="ONLINE", sim=False, ends=0)

@app.get("/")
def index():
    return """<h2>NEXUS NETWORK DEMO</h2><p>Open <a href="/site/nexus">NEXUS</a> or <a href="/site/status">STATUS</a>.</p>"""

@app.get("/site/<key>")
def site(key):
    if key not in SITE_NAMES: abort(404)
    filename = "status.html" if key == "status" else f"{key}.html"
    return send_from_directory(BASE / "static", filename)

@app.get("/api/status/<key>")
def api_status(key):
    if key not in state: abort(404)
    with lock:
        return jsonify(state[key])

@app.get("/api/all")
def api_all():
    with lock: return jsonify(state)

@app.post("/api/simulate/<key>")
def simulate(key):
    # Safe demonstration control: changes server UI state only; generates no attack traffic.
    if key not in state: abort(404)
    seconds = 20
    if not state[key]["sim"]:
        threading.Thread(target=worker, args=(key, seconds), daemon=True).start()
    return jsonify({"ok": True, "site": key, "duration": seconds, "simulation": True})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
