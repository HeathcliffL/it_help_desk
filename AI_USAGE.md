# AI_USAGE.md

## AI Tools Planned / Used
- ChatGPT: project scoping, route design, database schema drafting, debugging support, README drafting
- GitHub Copilot: code completion, repetitive Flask/SQLAlchemy scaffolding, template assistance

## Component Ownership Map
| Component | Primary Author | Notes |
|---|---|---|
| Initial project structure | AI + human | Generated as a starting scaffold, then reorganized manually |
| Authentication routes | AI + human | Human reviewed password hashing and session handling |
| Ticket CRUD logic | AI + human | Human validated ownership checks and field validation |
| Admin status update flow | AI + human | Human confirmed server-side role enforcement |
| Comment feature | AI + human | Human reviewed ticket access control before accepting |
| README and submission docs | AI + human | Human edited wording to match course requirements |

## Example Prompts
1. "Generate a Flask project skeleton for a multi-user campus IT help desk app using PostgreSQL and SQLAlchemy."
2. "Show a secure example of session-based login with password hashing in Flask."
3. "Add a ticket comment system with server-side ownership checks and an admin reply flow."

## AI Output Review / Fixes
### 1. Session and route protection
An AI-generated draft handled role differences mostly in the UI. This was revised to enforce authorization server-side with explicit decorators and ownership checks.

### 2. Ticket access control
An early draft allowed ticket lookup by ID without confirming ticket ownership for normal users. This was corrected by checking `ticket.user_id == current_user.id` unless the current user is an admin.

### 3. Reopen ticket feature
AI-assisted guidance was used to add a `POST /tickets/<id>/reopen` route, a resolved-ticket form, and documentation updates. The final code was manually reviewed to keep the ownership check server-side while leaving the reason validation intentionally minimal for later analysis.

## Security Reflection
One intentionally weak area remains in the application: there is no rate limiting on login, comment submission, or ticket reopening. The reopen form also performs only a required-field check on the reason field. This is acceptable for the Phase 0 handoff because it creates a realistic abuse-prevention and input-validation discussion point, but it would need stronger limits, length checks, and audit controls before production use.

## Current Known Limitations
- Reopen reasons are stored as plain ticket comments rather than a separate audit-log table.
- Reopening does not prevent repeated submissions after the ticket is resolved again.
- The project uses server-side role and ownership checks, but it intentionally avoids more advanced authorization policies to keep the codebase understandable.
