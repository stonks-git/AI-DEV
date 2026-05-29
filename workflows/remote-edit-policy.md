# Remote Edit Policy

> Load this workflow when the project has deployed or remote environments (staging, production, VPS, cloud instances).

## When to Use

Any task that involves files or state on a remote server.

## Four-Tier Rule

| Tier | What | Rule | Example |
|------|------|------|---------|
| **Git-tracked files** | Code, compose files, KB, plans, scripts, .env.example | **Local only.** Edit -> commit -> push -> pull on server. Never edit directly on a remote. | `docker-compose.yml`, `backend/app/main.py` |
| **Gitignored runtime config** | `.env`, secrets, certs, local overrides | Server edit OK — **only** with an explicit task or user request. | `/opt/app/.env`, TLS certs |
| **Ops commands** | Restart, migrate, deploy, recreate containers | OK on server — that is their purpose. | `docker compose up -d`, `alembic upgrade head` |
| **Read-only commands** | Logs, status, health checks, grep, printenv | Always OK — no mutation. | `docker logs`, `systemctl status`, `grep` |

## Why

Editing git-tracked files directly on a remote creates drift between HEAD and working tree. The next `git pull` refuses, the history stops reflecting reality, and the team loses the ability to reason about what is deployed.

## Exception

Legitimate emergency (critical hotfix, no local access): ask the user for explicit confirmation before editing any tracked file on a remote. Document the exception in the devlog.
