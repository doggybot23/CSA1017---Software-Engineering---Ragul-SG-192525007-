# ResQWatch — Simple Python Implementation

This project is a simple Python Flask implementation of the Intelligent Disaster Early Warning and Evacuation Management System. The supplied `INDEX.html` interface is preserved as the primary frontend so that the original dark emergency-operations UI/UX, navigation, cards, maps, charts, dialogs, and demo interactions remain unchanged.

## Project structure

```text
 disaster_flask_app/
 ├── app.py
 ├── requirements.txt
 ├── README.md
 └── templates/
     └── index.html
```

## Features

The Flask backend provides lightweight JSON endpoints for dashboard metrics, sensors, alerts, shelters, incidents, and response teams. It also accepts simple POST requests for creating demo alerts and incidents. Data is stored in memory for easy demonstration and is reset whenever the server restarts. The frontend continues to provide the original client-side demo interactions from the supplied HTML file.

## Run locally

```bash
cd disaster_flask_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

## API examples

```bash
curl http://127.0.0.1:5000/api/health
curl http://127.0.0.1:5000/api/dashboard
curl http://127.0.0.1:5000/api/sensors
curl http://127.0.0.1:5000/api/shelters
curl http://127.0.0.1:5000/api/incidents
curl http://127.0.0.1:5000/api/teams
```

Create a demo alert:

```bash
curl -X POST http://127.0.0.1:5000/api/alerts \\
  -H 'Content-Type: application/json' \\
  -d '{"hazard":"Flood","location":"North Zone","severity":"critical","message":"Prepare to evacuate if instructed."}'
```

## Important scope note

This is an academic prototype. The application uses simulated data and in-memory storage. It is not an official warning service, does not connect to real emergency infrastructure, and does not guarantee safe evacuation routes. A production system would require authentication, a persistent database, real sensor feeds, validated GIS and routing data, tested notification providers, audit logs, security controls, and approval from disaster-management authorities.

## Verification performed

The Flask application was started locally and verified through the browser. The original interface loaded with the expected AEGIS COMMAND navigation, dashboard cards, charts, emergency controls, and simulation disclaimer. The `ACTIVATE EMERGENCY` control changed the interface to `CRITICAL EMERGENCY STATE`, displayed the emergency banner, changed the control to `DEACTIVATE EMERGENCY`, and produced the original emergency toast message. The backend endpoints `/api/health`, `/api/dashboard`, and `/api/sensors` returned valid JSON responses.
