from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Simple in-memory demo data. Replace with a database for production use.
sensors = [
    {"id": "WTR-104", "name": "River Level Sensor", "type": "Water Level", "value": 3.8, "unit": "m", "status": "ONLINE", "risk": "CRITICAL"},
    {"id": "WX-207", "name": "Rainfall Station", "type": "Rainfall", "value": 82.4, "unit": "mm/hr", "status": "ONLINE", "risk": "WARNING"},
    {"id": "SEI-018", "name": "Seismic Node", "type": "Magnitude", "value": 2.4, "unit": "M", "status": "ONLINE", "risk": "SAFE"},
    {"id": "ENV-311", "name": "Air Quality Node", "type": "Smoke Index", "value": 18.0, "unit": "AQI", "status": "ONLINE", "risk": "SAFE"},
]

alerts = [
    {"id": "ALT-2048", "hazard": "Flood", "location": "North Zone", "severity": "CRITICAL", "message": "Immediate evacuation preparation required.", "status": "BROADCASTED", "time": "08:42 UTC"},
    {"id": "ALT-2047", "hazard": "Cyclone", "location": "Coastal Sector", "severity": "WARNING", "message": "Monitor official instructions and avoid low-lying roads.", "status": "BROADCASTED", "time": "08:15 UTC"},
]

shelters = [
    {"id": "SH-01", "name": "Central Community Hall", "location": "Ward 3", "capacity": 1200, "occupancy": 740, "status": "OPEN", "medical": "Available", "food": "3 days"},
    {"id": "SH-02", "name": "Riverside School", "location": "Ward 5", "capacity": 800, "occupancy": 680, "status": "NEAR CAPACITY", "medical": "Limited", "food": "2 days"},
    {"id": "SH-03", "name": "North Sports Complex", "location": "North Zone", "capacity": 1800, "occupancy": 410, "status": "OPEN", "medical": "Available", "food": "5 days"},
]

incidents = [
    {"id": "INC-1001", "type": "Blocked Road", "location": "Valley Road", "severity": "WARNING", "description": "Waterlogging reported near the bridge.", "status": "OPEN"},
    {"id": "INC-1002", "type": "Medical Emergency", "location": "Market Ward", "severity": "CRITICAL", "description": "Two people require medical assistance.", "status": "ASSIGNED"},
]

teams = [
    {"id": "TM-21", "name": "Fire & Rescue Alpha", "department": "Fire and Rescue", "location": "North Zone", "status": "DEPLOYED", "personnel": 12},
    {"id": "TM-07", "name": "Medical Response Bravo", "department": "Health Services", "location": "Central Hall", "status": "AVAILABLE", "personnel": 8},
]


def now_iso():
    return datetime.now(timezone.utc).isoformat()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "ResQWatch demo API", "timestamp": now_iso()})


@app.get("/api/dashboard")
def dashboard():
    total_capacity = sum(s["capacity"] for s in shelters)
    total_occupancy = sum(s["occupancy"] for s in shelters)
    return jsonify({
        "active_threats": sum(1 for a in alerts if a["severity"] in {"CRITICAL", "WARNING"}),
        "population_at_risk": 24850,
        "open_shelters": sum(1 for s in shelters if s["status"] != "FULL"),
        "shelter_capacity": {"occupied": total_occupancy, "capacity": total_capacity},
        "evacuation_progress": 72,
        "updated_at": now_iso(),
    })


@app.get("/api/sensors")
def get_sensors():
    return jsonify({"items": sensors, "count": len(sensors), "updated_at": now_iso()})


@app.get("/api/alerts")
def get_alerts():
    return jsonify({"items": alerts, "count": len(alerts), "updated_at": now_iso()})


@app.post("/api/alerts")
def create_alert():
    data = request.get_json(silent=True) or {}
    required = ["hazard", "location", "severity", "message"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400
    item = {
        "id": f"ALT-{len(alerts) + 2050}",
        "hazard": data["hazard"],
        "location": data["location"],
        "severity": data["severity"].upper(),
        "message": data["message"],
        "status": "DRAFT",
        "time": datetime.now(timezone.utc).strftime("%H:%M UTC"),
    }
    alerts.insert(0, item)
    return jsonify(item), 201


@app.get("/api/shelters")
def get_shelters():
    return jsonify({"items": shelters, "count": len(shelters), "updated_at": now_iso()})


@app.get("/api/incidents")
def get_incidents():
    return jsonify({"items": incidents, "count": len(incidents), "updated_at": now_iso()})


@app.post("/api/incidents")
def create_incident():
    data = request.get_json(silent=True) or {}
    required = ["type", "location", "severity", "description"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400
    item = {
        "id": f"INC-{1000 + len(incidents) + 1}",
        "type": data["type"],
        "location": data["location"],
        "severity": data["severity"].upper(),
        "description": data["description"],
        "status": "OPEN",
    }
    incidents.insert(0, item)
    return jsonify(item), 201


@app.get("/api/teams")
def get_teams():
    return jsonify({"items": teams, "count": len(teams), "updated_at": now_iso()})


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
