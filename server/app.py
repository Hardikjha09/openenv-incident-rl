"""
FastAPI server for the Incident Report Structuring Environment.
"""

import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from openenv.core.env_server import create_app
from server.incident_environment import IncidentEnvironment
from models import IncidentAction, IncidentObservation

# create_app automatically reads openenv.yaml and sets up ALL required 
# endpoints (/metadata, /reset, /step, etc.) strictly to platform spec.
app = create_app(
    IncidentEnvironment,
    IncidentAction,
    IncidentObservation,
    max_concurrent_envs=10,
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

def main():
    """Entry point for running the server directly."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()