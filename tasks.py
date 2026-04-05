"""Tasks for the Incident Report Structuring Environment."""

TASKS = [
    {
        "id": "easy_1",
        "difficulty": "easy",
        "description": "Simple web service login downtime",
        "raw_text": """🚨 ALERT: login-service is DOWN
Started: 14:32 IST | Ticket: INC-2026-0341
Affected users: ~2,000 | Severity: P2
On-call: Arjun Mehta (@arjun)
Auth squad looking into it. DB connections timing out.""",
        "fields_to_extract": [
            "incident_id", "severity", "affected_service", "start_time",
            "on_call_engineer", "affected_users"
        ],
        "extraction_hints": "Extract as specified.",
        "ground_truth": {
            "incident_id": "INC-2026-0341",
            "severity": "P2",
            "affected_service": "login-service",
            "start_time": "14:32 IST",
            "on_call_engineer": "Arjun Mehta",
            "affected_users": "2000"
        },
        "field_types": {
            "incident_id": "exact",
            "severity": "contains",
            "affected_service": "fuzzy",
            "start_time": "contains",
            "on_call_engineer": "fuzzy",
            "affected_users": "numeric"
        }
    },
    {
        "id": "easy_2",
        "difficulty": "easy",
        "description": "Database connection pool exhaustion",
        "raw_text": """PagerDuty Alert — HIGH
Service: payments-db (prod)
Error: Connection pool exhausted — max 200 connections reached
First seen: 2026-04-03 11:47 UTC
Reported by: monitoring-bot
Ticket auto-created: INC-2026-0892
Severity: P2 | Status: Firing""",
        "fields_to_extract": [
            "incident_id", "service_name", "error_type", "start_time",
            "reporter", "severity", "status"
        ],
        "extraction_hints": "Extract fields as specified.",
        "ground_truth": {
            "incident_id": "INC-2026-0892",
            "service_name": "payments-db",
            "error_type": "Connection pool exhausted",
            "start_time": "2026-04-03 11:47 UTC",
            "reporter": "monitoring-bot",
            "severity": "P2",
            "status": "Firing"
        },
        "field_types": {
            "incident_id": "exact",
            "service_name": "fuzzy",
            "error_type": "contains",
            "start_time": "contains",
            "reporter": "fuzzy",
            "severity": "contains",
            "status": "contains"
        }
    },
    {
        "id": "easy_3",
        "difficulty": "easy",
        "description": "API rate limit breach",
        "raw_text": """RATE LIMIT BREACH — search-api
Threshold: 10,000 req/min | Current: 24,871 req/min
Triggered at: 16:05:33 IST on 03-Apr-2026
Severity: P3 — performance degraded, not down
Auto-throttling enabled. Notify: platform-team@company.com""",
        "fields_to_extract": [
            "service_name", "alert_type", "threshold_value",
            "current_value", "triggered_at", "severity"
        ],
        "extraction_hints": "follow the field list carefully",
        "ground_truth": {
            "service_name": "search-api",
            "alert_type": "Rate limit breach",
            "threshold_value": "10000",
            "current_value": "24871",
            "triggered_at": "16:05:33 IST",
            "severity": "P3"
        },
        "field_types": {
            "service_name": "fuzzy",
            "alert_type": "contains",
            "threshold_value": "numeric",
            "current_value": "numeric",
            "triggered_at": "contains",
            "severity": "contains"
        }
    },
    {
        "id": "medium_1",
        "difficulty": "medium",
        "description": "Microservice cascade failure",
        "raw_text": """14:10 @priya: order-service throwing 503s, 
looks like inventory-service is not responding
14:12 @rahul: confirmed - inventory-service OOMKilled in k8s
pod restarts: 7 in last 10 mins
14:15 @priya: cascade - payment-service and notification-service 
also degraded now. ~8500 users impacted
14:18 @vikram (IC): taking incident command. sev1.
ticket: INC-2026-1103. ETA for fix: 30 mins
currently: restarting inventory pods with higher memory limit""",
        "fields_to_extract": [
            "primary_service", "affected_downstream_services", "start_time",
            "severity", "on_call_engineer", "incident_commander",
            "current_status", "affected_users", "ticket_id"
        ],
        "extraction_hints": "Extract as specified. For list fields like affected_downstream_services return a JSON array.",
        "ground_truth": {
            "primary_service": "inventory-service",
            "affected_downstream_services": ["order-service", "payment-service", "notification-service"],
            "start_time": "14:10",
            "severity": "P1",
            "on_call_engineer": "Priya",
            "incident_commander": "Vikram",
            "current_status": "Restarting pods",
            "affected_users": "8500",
            "ticket_id": "INC-2026-1103"
        },
        "field_types": {
            "primary_service": "fuzzy",
            "affected_downstream_services": "list",
            "start_time": "contains",
            "severity": "contains",
            "on_call_engineer": "fuzzy",
            "incident_commander": "fuzzy",
            "current_status": "contains",
            "affected_users": "numeric",
            "ticket_id": "exact"
        }
    },
    {
        "id": "medium_2",
        "difficulty": "medium",
        "description": "Security unauthorized access attempt",
        "raw_text": """SECURITY INCIDENT — Unauthorized Access Attempt
Ticket: SEC-2026-0217 | Detected: 02:34 IST
Attack type: Credential stuffing via brute force
Targeted system: admin-portal (prod)
Attacker IP: 185.220.101.47 (known Tor exit node)
Actions taken: IP blocked at WAF, account lockouts triggered
for 23 accounts, security team notified
Severity: P1 | Reporter: security-monitoring-system
Status: Contained — investigation ongoing""",
        "fields_to_extract": [
            "ticket_id", "incident_type", "affected_system",
            "attacker_ip", "attack_vector", "detection_time",
            "containment_action", "severity", "accounts_affected"
        ],
        "extraction_hints": "Return values in specific format.",
        "ground_truth": {
            "ticket_id": "SEC-2026-0217",
            "incident_type": "Unauthorized access attempt",
            "affected_system": "admin-portal",
            "attacker_ip": "185.220.101.47",
            "attack_vector": "Credential stuffing",
            "detection_time": "02:34 IST",
            "containment_action": "IP blocked at WAF",
            "severity": "P1",
            "accounts_affected": "23"
        },
        "field_types": {
            "ticket_id": "exact",
            "incident_type": "contains",
            "affected_system": "fuzzy",
            "attacker_ip": "exact",
            "attack_vector": "contains",
            "detection_time": "contains",
            "containment_action": "contains",
            "severity": "contains",
            "accounts_affected": "numeric"
        }
    },
    {
        "id": "medium_3",
        "difficulty": "medium",
        "description": "CI/CD pipeline failure blocking deployments",
        "raw_text": """hey all — deploy pipeline is broken since ~10:20am
pipeline: main-backend-deploy | stage failing: integration-tests
error: docker.io connection timeout during image pull
workaround tried: switched to ecr mirror, still failing
PRs blocked: 14 PRs cant merge rn
sev2 raised — ticket INC-2026-0654
@devops-oncall pls take a look, build queue piling up
reporter: neha-singh | started: 10:20 IST""",
        "fields_to_extract": [
            "pipeline_name", "failing_stage", "error_type",
            "prs_blocked", "start_time", "reporter",
            "workaround_applied", "severity", "ticket_id"
        ],
        "extraction_hints": "Extract as specified.",
        "ground_truth": {
            "pipeline_name": "main-backend-deploy",
            "failing_stage": "integration-tests",
            "error_type": "docker.io connection timeout",
            "prs_blocked": "14",
            "start_time": "10:20 IST",
            "reporter": "Neha Singh",
            "workaround_applied": "Switched to ECR mirror",
            "severity": "P2",
            "ticket_id": "INC-2026-0654"
        },
        "field_types": {
            "pipeline_name": "fuzzy",
            "failing_stage": "contains",
            "error_type": "contains",
            "prs_blocked": "numeric",
            "start_time": "contains",
            "reporter": "fuzzy",
            "workaround_applied": "contains",
            "severity": "contains",
            "ticket_id": "exact"
        }
    },
    {
        "id": "hard_1",
        "difficulty": "hard",
        "description": "Multi-region DB replication lag causing data inconsistency",
        "raw_text": """03:41 UTC @db-oncall: replication lag spiking on prod-db-primary
us-east-1 → ap-south-1 lag: 847ms (normal <50ms)
03:43 @infra-lead: RDS enhanced monitoring shows I/O saturation
affected regions: ap-south-1, eu-west-2, ap-southeast-1
03:47 @db-oncall: lag now 2341ms on ap-south-1, users seeing 
stale data on order-history and profile-service
03:52 @incident-mgr (kiran.r): IC here. sev1. 
INC-2026-2891. RTO target: 15 mins. RPO: 0 (zero data loss)
03:58 @db-oncall: mitigation - promoted ap-south-1 read replica 
to handle reads. primary lag reducing - now 1205ms
04:03 @infra-lead: root cause - scheduled vacuum on prod-db 
caused I/O spike. vacuum killed. lag: 203ms and falling
postmortem: PM-2026-0341""",
        "fields_to_extract": [
            "primary_db", "affected_regions", "initial_lag_ms",
            "peak_lag_ms", "incident_start_utc", "severity",
            "incident_commander", "rto_minutes", "root_cause",
            "mitigation_applied", "postmortem_ticket",
            "customer_facing_services", "current_lag_ms"
        ],
        "extraction_hints": "Extract as specified. For lists return JSON arrays.",
        "ground_truth": {
            "primary_db": "prod-db-primary",
            "affected_regions": ["ap-south-1", "eu-west-2", "ap-southeast-1"],
            "initial_lag_ms": "847",
            "peak_lag_ms": "2341",
            "incident_start_utc": "03:41 UTC",
            "severity": "P1",
            "incident_commander": "Kiran R",
            "rto_minutes": "15",
            "root_cause": "Scheduled vacuum caused I/O spike",
            "mitigation_applied": "Promoted read replica",
            "postmortem_ticket": "PM-2026-0341",
            "customer_facing_services": ["order-history", "profile-service"],
            "current_lag_ms": "203"
        },
        "field_types": {
            "primary_db": "fuzzy",
            "affected_regions": "list",
            "initial_lag_ms": "numeric",
            "peak_lag_ms": "numeric",
            "incident_start_utc": "contains",
            "severity": "contains",
            "incident_commander": "fuzzy",
            "rto_minutes": "numeric",
            "root_cause": "contains",
            "mitigation_applied": "contains",
            "postmortem_ticket": "exact",
            "customer_facing_services": "list",
            "current_lag_ms": "numeric"
        }
    },
    {
        "id": "hard_2",
        "difficulty": "hard",
        "description": "DDoS attack with partial CDN mitigation",
        "raw_text": """06:15 AUTO-ALERT: Traffic anomaly — api-gateway
incoming: 847 Gbps (normal baseline: 12 Gbps)
06:17 @sec-oncall (maya.p): DDoS confirmed. 
attack type: volumetric UDP flood + HTTP layer7 mix
Cloudflare under Magic Transit engaged — mitigating ~60%
affected endpoints: /api/v2/search, /api/v2/feed, /api/v1/auth
06:22 @sec-oncall: Cloudflare suppressing 512 Gbps
residual 335 Gbps still hitting origin — origin degraded
06:28 @VP-eng (escalation): whats ETA? customers tweeting
06:30 @sec-oncall: additional Cloudflare rules pushed
now mitigating 78%. ticket: SEC-2026-0891. sev1.
estimated cost if down 1hr: ~$240,000
services degraded: api-gateway, cdn-edge, auth-service""",
        "fields_to_extract": [
            "attack_type", "peak_traffic_gbps", "normal_traffic_gbps",
            "affected_endpoints", "cdn_provider", "mitigation_percentage",
            "attack_start_time", "escalated_to", "severity",
            "ticket_id", "services_degraded", "estimated_cost_usd",
            "residual_traffic_gbps"
        ],
        "extraction_hints": "Extract as specified. For lists return JSON arrays.",
        "ground_truth": {
            "attack_type": "Volumetric UDP flood and HTTP layer7",
            "peak_traffic_gbps": "847",
            "normal_traffic_gbps": "12",
            "affected_endpoints": ["/api/v2/search", "/api/v2/feed", "/api/v1/auth"],
            "cdn_provider": "Cloudflare",
            "mitigation_percentage": "78",
            "attack_start_time": "06:15",
            "escalated_to": "VP Engineering",
            "severity": "P1",
            "ticket_id": "SEC-2026-0891",
            "services_degraded": ["api-gateway", "cdn-edge", "auth-service"],
            "estimated_cost_usd": "240000",
            "residual_traffic_gbps": "335"
        },
        "field_types": {
            "attack_type": "contains",
            "peak_traffic_gbps": "numeric",
            "normal_traffic_gbps": "numeric",
            "affected_endpoints": "list",
            "cdn_provider": "fuzzy",
            "mitigation_percentage": "numeric",
            "attack_start_time": "contains",
            "escalated_to": "contains",
            "severity": "contains",
            "ticket_id": "exact",
            "services_degraded": "list",
            "estimated_cost_usd": "numeric",
            "residual_traffic_gbps": "numeric"
        }
    },
    {
        "id": "hard_3",
        "difficulty": "hard",
        "description": "Memory leak causing gradual fleet-wide service degradation",
        "raw_text": """INC-2026-3341 | opened 09:12 IST | reporter: auto-monitor
sev: started P3, escalated P2 at 09:45, now P1 at 10:20
service: recommendation-engine v2.4.1 (NOT v2.4.0 — confirmed)
symptom: gradual mem increase since ~08:30 IST
09:12: mem at 71% across 34/80 pods
09:45: mem 84% — 12 pods OOMKilled, auto-restarted
10:20: mem 91% — 31 pods OOMKilled, latency p99 >8s
total pod restarts so far: 47
@sre-lead (anand.k): RCA - memory leak in new 
embedding cache introduced in v2.4.1 deploy at 07:55 IST
fix: rollback to v2.4.0 initiated at 10:35
10:52: rollback complete, mem stabilizing at 43%
incident duration: ~2hrs 40mins
postmortem scheduled. ticket updated.""",
        "fields_to_extract": [
            "ticket_id", "affected_service", "service_version",
            "memory_usage_percent_peak", "pods_affected",
            "pods_restarted", "degradation_start_time",
            "incident_start_time", "root_cause", "fix_applied",
            "severity_final", "reporter", "incident_duration_minutes"
        ],
        "extraction_hints": "Extract as specified.",
        "ground_truth": {
            "ticket_id": "INC-2026-3341",
            "affected_service": "recommendation-engine",
            "service_version": "v2.4.1",
            "memory_usage_percent_peak": "91",
            "pods_affected": "31",
            "pods_restarted": "47",
            "degradation_start_time": "08:30 IST",
            "incident_start_time": "09:12 IST",
            "root_cause": "Memory leak in embedding cache",
            "fix_applied": "Rollback to v2.4.0",
            "severity_final": "P1",
            "reporter": "auto-monitor",
            "incident_duration_minutes": "160"
        },
        "field_types": {
            "ticket_id": "exact",
            "affected_service": "fuzzy",
            "service_version": "exact",
            "memory_usage_percent_peak": "numeric",
            "pods_affected": "numeric",
            "pods_restarted": "numeric",
            "degradation_start_time": "contains",
            "incident_start_time": "contains",
            "root_cause": "contains",
            "fix_applied": "contains",
            "severity_final": "contains",
            "reporter": "fuzzy",
            "incident_duration_minutes": "numeric"
        }
    }
]

def get_tasks_by_difficulty(difficulty: str) -> list:
    """Return all tasks of a given difficulty."""
    return [t for t in TASKS if t["difficulty"] == difficulty]

def get_task_by_id(task_id: str) -> dict:
    """Return a specific task by ID."""
    for t in TASKS:
        if t["id"] == task_id:
            return t
    return None

def get_all_task_ids() -> list:
    """Return a list of all task IDs."""
    return [t["id"] for t in TASKS]