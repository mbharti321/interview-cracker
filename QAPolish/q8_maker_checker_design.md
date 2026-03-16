# Maker-Checker Design (FastAPI + SQL)

## Overview
The maker-checker pattern ensures critical actions created by one user (maker) must be approved by another (checker) before taking effect. Key goals: auditability, atomic state transitions, separation of duties.

## Database schema
- `actions` table:
  - `id` UUID/INT PRIMARY KEY
  - `maker_id` (user who created the action)
  - `checker_id` (nullable; set when checker approves/rejects)
  - `action_type` (string)
  - `payload` (JSONB) -- the proposed change
  - `status` ENUM('PENDING','APPROVED','REJECTED','APPLIED')
  - `created_at` TIMESTAMP
  - `updated_at` TIMESTAMP
  - `approved_at` TIMESTAMP (nullable)

- `audit_trail` table (append-only):
  - `id`, `action_id`, `actor_id`, `event_type`, `details` (JSON), `timestamp`

## State transitions
- Maker creates -> `PENDING`.
- Checker approves -> `APPROVED` (set `checker_id`, `approved_at`). A background job applies the change and sets `APPLIED`.
- Checker rejects -> `REJECTED`.

All transitions should be recorded in `audit_trail` for compliance.

## API endpoints (FastAPI)
- `POST /actions` (maker): create pending action.
- `GET /actions/{id}`: view action and status.
- `GET /actions?status=PENDING`: list pending actions (for checkers).
- `POST /actions/{id}/approve`: checker approves (body includes `checker_id`, optional comment).
- `POST /actions/{id}/reject`: checker rejects.
- `GET /audit`: read-only audit feed.

## Key logic (pseudo-code)

```py
from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()

@app.post('/actions')
def create_action(maker_id: int, action_type: str, payload: dict):
    action = db.insert('actions', {
        'maker_id': maker_id,
        'action_type': action_type,
        'payload': payload,
        'status': 'PENDING',
        'created_at': datetime.utcnow()
    })
    db.insert('audit_trail', { 'action_id': action.id, 'actor_id': maker_id, 'event_type': 'CREATED' })
    return action

@app.post('/actions/{id}/approve')
def approve_action(id: int, checker_id: int, comment: str | None = None):
    # 1. Fetch and ensure still PENDING
    action = db.select_for_update('actions', id)
    if action.status != 'PENDING':
        raise HTTPException(400, 'Action not pending')
    # 2. Update atomically to APPROVED
    db.update('actions', id, { 'status': 'APPROVED', 'checker_id': checker_id, 'approved_at': datetime.utcnow() })
    db.insert('audit_trail', { 'action_id': id, 'actor_id': checker_id, 'event_type': 'APPROVED', 'details': { 'comment': comment } })
    # 3. enqueue background task to apply change
    task_queue.enqueue('apply_action', { 'action_id': id })
    return {'status': 'ok'}

def worker_apply_action(payload):
    action_id = payload['action_id']
    # fetch action; ensure status is APPROVED and not applied
    action = db.select_for_update('actions', action_id)
    if action.status != 'APPROVED':
        return
    try:
        # apply the payload change (domain-specific)
        apply_payload(action.payload)
        db.update('actions', action_id, { 'status': 'APPLIED', 'updated_at': datetime.utcnow() })
        db.insert('audit_trail', { 'action_id': action_id, 'actor_id': None, 'event_type': 'APPLIED' })
    except Exception as e:
        # record failure, possibly retry
        db.insert('audit_trail', { 'action_id': action_id, 'actor_id': None, 'event_type': 'APPLY_FAILED', 'details': { 'error': str(e) } })

```

## Additional considerations
- Authentication/authorization: ensure makers cannot approve their own actions; enforce segregation of duties.
- Timeouts and SLA: auto-escalation if pending too long.
- Idempotency: applying an action must be idempotent or guarded by the `APPLIED` state.
- Retention: immutable audit logs and export capability for compliance.
