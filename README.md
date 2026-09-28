# NEXUS NETWORK DEMO

A fictional multi-site web demonstration with a safe, server-side load simulation.

## Run
1. Install Python 3.10+.
2. `pip install -r requirements.txt`
3. `python app.py`
4. Open http://127.0.0.1:8080/site/nexus
5. Open http://127.0.0.1:8080/site/status

## Simulation
POST `/api/simulate/<site>` changes only the displayed state and telemetry. It does not
generate DDoS traffic or send attack requests to external systems.

Example sites:
nexus, pulse, bytewire, voltage, streambox, grid, chatter, cloudvault, travelix, status
