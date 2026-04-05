"""
FastAPI server for the Incident Report Structuring Environment.
"""

from openenv.core.env_server import create_app

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.incident_environment import IncidentEnvironment

try:
    from models import IncidentAction, IncidentObservation
except ImportError:
    from data_extraction.models import IncidentAction, IncidentObservation

app = create_app(
    IncidentEnvironment,
    IncidentAction,
    IncidentObservation,
    max_concurrent_envs=10,
)


def main():
    """Entry point for running the server directly."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()