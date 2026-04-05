"""
Incident Report Structuring Environment — Server-side core logic.

This is the brain of the environment. When an LLM connects:
  1. reset() → picks a task, shows messy text + which fields to extract
  2. step()  → receives extracted JSON, grades it using the grader
  3. state() → returns episode metadata
"""

import random
import json
from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

# Try both import paths (local dev vs Docker)
try:
    from models import IncidentAction, IncidentObservation
    from tasks import TASKS, get_task_by_id
    from grader import grade_extraction
except ImportError:
    from data_extraction.models import IncidentAction, IncidentObservation
    from data_extraction.tasks import TASKS, get_task_by_id
    from data_extraction.grader import grade_extraction


class IncidentEnvironment(Environment):
    """
    An environment where an LLM agent must extract structured data
    from messy unstructured text.

    The agent receives raw text + a list of fields to extract,
    and must return a JSON dict with the extracted values.
    The grader uses fuzzy matching to score each field.
    """

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_task = None

    def reset(self, task_id: str = None, **kwargs) -> IncidentObservation:
        """
        Start a new episode.

        Picks a task (random or specific), and returns the challenge:
        the raw text, which fields to extract, and format hints.
        """
        self._state = State(episode_id=str(uuid4()), step_count=0)

        # Pick a task
        task = get_task_by_id(task_id) if task_id else None
        if task:
            self._current_task = task
        else:
            self._current_task = random.choice(TASKS)

        return IncidentObservation(
            task_id=self._current_task["id"],
            difficulty=self._current_task["difficulty"],
            raw_text=self._current_task["raw_text"],
            fields_to_extract=self._current_task["fields_to_extract"],
            extraction_hints=self._current_task["extraction_hints"],
            feedback="Extract the required fields from the incident report.",
            fields_correct=0,
            fields_total=len(self._current_task["fields_to_extract"]),
            field_scores={},
            done=False,
            reward=0.0,
        )

    def step(self, action: IncidentAction) -> IncidentObservation:
        """
        The agent submitted extracted data. Grade it.

        Uses the grader to compare each extracted field against ground truth,
        with appropriate matching strategies (exact, numeric, fuzzy, etc.).
        """
        self._state.step_count += 1

        if self._current_task is None:
            return IncidentObservation(
                feedback="Error: No task loaded. Call reset() first.",
                done=True,
                reward=0.0,
            )

        # Parse the extracted data
        extracted = action.extracted_data
        if not isinstance(extracted, dict):
            try:
                extracted = json.loads(str(extracted))
            except (json.JSONDecodeError, TypeError):
                return IncidentObservation(
                    task_id=self._current_task["id"],
                    difficulty=self._current_task["difficulty"],
                    raw_text=self._current_task["raw_text"],
                    fields_to_extract=self._current_task["fields_to_extract"],
                    extraction_hints=self._current_task["extraction_hints"],
                    feedback="Error: extracted_data must be a valid JSON dictionary.",
                    fields_correct=0,
                    fields_total=len(self._current_task["ground_truth"]),
                    field_scores={},
                    done=True,
                    reward=0.0,
                )

        # Grade the extraction
        result = grade_extraction(
            extracted_data=extracted,
            ground_truth=self._current_task["ground_truth"],
            field_types=self._current_task["field_types"],
        )

        # Build feedback string
        feedback_lines = [
            f"Task: {self._current_task['id']} ({self._current_task['difficulty']})",
            f"Fields correct (score >= 0.8): {result['fields_correct']}/{result['fields_total']}",
            f"Overall reward: {result['reward']:.3f}",
            "",
            "Per-field breakdown:",
        ] + result["feedback_lines"]

        return IncidentObservation(
            task_id=self._current_task["id"],
            difficulty=self._current_task["difficulty"],
            raw_text=self._current_task["raw_text"],
            fields_to_extract=self._current_task["fields_to_extract"],
            extraction_hints=self._current_task["extraction_hints"],
            feedback="\n".join(feedback_lines),
            fields_correct=result["fields_correct"],
            fields_total=result["fields_total"],
            field_scores=result["field_scores"],
            done=True,
            reward=result["reward"],
        )

    @property
    def state(self) -> State:
        return self._state