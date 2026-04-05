"""
Models for the Incident Report Structuring Environment.

Think of it like a form:
  - The environment shows the LLM a messy incident report and says "extract these fields"
  - The LLM fills out a JSON with the extracted data
  - The environment grades how correct each field is
"""

from pydantic import Field
from openenv.core.env_server.types import Action, Observation


class IncidentAction(Action):
    """
    What the LLM sends back to us — a JSON dict of extracted fields.
    
    Example:
        IncidentAction(extracted_data={
            "incident_id": "INC-2026-0341",
            "severity": "P2",
            "affected_service": "login-service",
            "start_time": "14:32 IST"
        })
    """
    extracted_data: dict = Field(
        ...,
        description="A dictionary mapping field names to extracted values"
    )


class IncidentObservation(Observation):
    """
    What the environment shows the agent.
    
    On reset(): shows the raw text + which fields to extract
    On step(): shows feedback on how well the extraction went
    
    NOTE: 'done' (bool) and 'reward' (float) are inherited from Observation.
    """
    # --- The task (shown on reset) ---
    task_id: str = Field(default="", description="Unique task identifier")
    difficulty: str = Field(default="easy", description="easy / medium / hard")
    raw_text: str = Field(default="", description="The messy incident report to extract from")
    fields_to_extract: list[str] = Field(
        default_factory=list,
        description="List of field names the agent must extract"
    )
    extraction_hints: str = Field(
        default="",
        description="Hints about expected format for each field"
    )

    # --- Feedback (shown after step) ---
    feedback: str = Field(default="", description="Detailed grading feedback")
    fields_correct: int = Field(default=0, description="Number of fields graded as correct")
    fields_total: int = Field(default=0, description="Total number of fields")
    field_scores: dict = Field(
        default_factory=dict,
        description="Per-field scores: {field_name: score}"
    )