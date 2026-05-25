# Shortly Constitution

## Core Principles

### I. Minimal Dependencies
Use only what is strictly essential. Each new dependency must justify its existence against a standard-library or zero-dep alternative.

### II. Standard Library First
Prefer Python standard library over third-party packages whenever the difference in developer effort is acceptable. Specifically: persistence uses `sqlite3` (stdlib), not SQLAlchemy.

### III. Testability is Non-Negotiable
Every HTTP endpoint MUST have at least one automated test using FastAPI's `TestClient`. Tests live in `tests/` and run with `pytest`.

### IV. Server-Rendered HTML Only
No single-page application, no frontend build tools, no npm. UI is rendered server-side with Jinja2 and styled with a single CDN stylesheet (Pico.css).

### V. Offline-First Operation
The application MUST run fully offline. No external API calls, no Redis, no message broker, no analytics services.

### VI. Single-File Modules When Reasonable
Prefer one cohesive module file over premature decomposition. Split only when a module exceeds ~300 lines or has clearly separable concerns.

### VII. Explicit Over Implicit
No "magic" frameworks. Routing, persistence, and templating must be visible in the code without relying on metaclasses or auto-discovery.

## Out of Scope (Permanent)

The following are explicitly forbidden for the foreseeable future:
- Authentication / user accounts
- Docker / container orchestration
- ORM (SQLAlchemy, etc.) or database migrations (Alembic)
- Background workers (Celery, RQ)
- Frontend build tools (Vite, webpack, npm)
- External services (Redis, S3, message queues)
- Custom URL slugs by the user
- URL expiration

## Quality Gates

Before merging any change:
1. All `pytest` tests pass
2. App starts cleanly with `uv run uvicorn app.main:app`
3. No new top-level dependencies without explicit Constitution update

## Governance

This constitution supersedes any conflicting suggestions from AI agents or external templates. When in doubt, the principles here win.

**Version:** 1.0.0 | **Ratified:** 2026-05-25
