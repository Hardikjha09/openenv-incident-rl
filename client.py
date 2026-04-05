"""Client for the Incident Report Structuring Environment."""

from dataclasses import dataclass
from typing import Any
from openenv.core.env_client import EnvClient
from openenv.core.env_server.types import State

try:
    from .models import IncidentAction, IncidentObservation
except ImportError:
    from models import IncidentAction, IncidentObservation


@dataclass
class StepResult:
    """Simple container for the result of a reset() or step() call."""
    observation: IncidentObservation
    reward: float = 0.0
    done: bool = False


class IncidentEnv(EnvClient):
    """Client for the Incident Report Structuring environment."""
    action_type = IncidentAction
    observation_type = IncidentObservation

    def _step_payload(self, action: IncidentAction) -> dict:
        return action.model_dump()

    def _parse_result(self, data: dict) -> StepResult:
        obs_data = data.get("observation", {})
        obs = IncidentObservation(**obs_data)
        return StepResult(
            observation=obs,
            reward=data.get("reward", 0.0),
            done=data.get("done", False),
        )

    def _parse_state(self, data: dict) -> State:
        return State(**data)