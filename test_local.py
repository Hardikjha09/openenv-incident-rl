"""Quick test to verify the environment works end-to-end locally."""

# Import directly (no server needed for this test)
from server.incident_environment import IncidentEnvironment
from models import IncidentAction

env = IncidentEnvironment()

# Test reset — should return a task
TASK_ID = "easy_1"
obs = env.reset(task_id=TASK_ID)
print(f"Task: {obs.task_id} ({obs.difficulty})")
print(f"Fields to extract: {obs.fields_to_extract}")
print(f"Raw text preview: {obs.raw_text[:100]}...")
print()

# Test step — submit a fake extraction (partially correct)
action = IncidentAction(extracted_data={
    "incident_id": "INC-2026-0341",
    "severity": "P2",
    "affected_service": "login-service",
    "start_time": "14:32 IST",
    "on_call_engineer": "Wrong Name",  # wrong on purpose
    "affected_users": "50",            # Intentionally incorrect
})

result = env.step(action)
print(f"Reward: {result.reward}")
print(f"Fields correct: {result.fields_correct}/{result.fields_total}")
print(f"\nFeedback:\n{result.feedback}")