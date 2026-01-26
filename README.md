# SysDesk

**SysDesk** is an **email-based helpdesk ticketing system** built with **Python + Django**.

> 🚧 **Status: Under Development**
>
> This project is actively being built. Features, APIs, database schema, and deployment setup may change frequently.

---

## What SysDesk Does (Goal)

SysDesk turns inbound emails into support tickets, then lets an IT Admin/Agent manage and reply from a web portal.

### Core Flow

1. A user sends an email (e.g., to `support@yourdomain.com`)
2. SysDesk ingests the email and **creates a ticket automatically**
3. Admin logs into SysDesk portal and sees:
   - Open Ticket Queue
   - Closed Ticket Queue
4. Admin replies from the portal
5. User receives the reply in their inbox
6. If the user replies back, SysDesk **threads** it into the same ticket

---

## Planned Features

### MVP (Phase 1)

- Ticket creation from inbound email payload (webhook-style endpoint)
- Ticket queues: Open / Closed
- Ticket detail view with message timeline
- Admin login (Django authentication)
- Reply to requester from portal (outbound email)
- Internal notes (not emailed)

### Phase 2 (Production-ish)

- Email threading:
  - Message-ID / In-Reply-To / References
  - Ticket key in subject like: `[SYS-000001]`
  - Custom header: `X-SysDesk-Ticket`
- Attachments support
- Full-text search (Postgres)
- Audit log (ticket lifecycle events)
- SLA rules + scheduled tasks
- Rate limiting / abuse protection

### DevOps / Deployment (Phase 3)

- Dockerized local development stack
- Nginx + Gunicorn production setup
- CI/CD with GitHub Actions
- DigitalOcean deployment
- Health checks and backups

---

## Tech Stack

- Backend: Django (server-rendered, no DRF)
- Database: PostgreSQL
- Cache / Queue: Redis
- Background Jobs: Celery (planned)
- Reverse Proxy: Nginx
- Email (Dev): MailHog
- Deployment: Docker + DigitalOcean + GitHub Actions

---

## Repository Structure (Planned)

```
sysdesk/
  app/
    manage.py
    config/
    accounts/
    tickets/
    mailbox/
    auditlog/
  infra/
    nginx/
    scripts/
  .github/
    workflows/
  compose.dev.yml
  compose.prod.yml
  README.md
```

---

## Development Status

SysDesk is currently under **active development**.

- APIs may change
- Database schema may evolve
- Features are implemented incrementally following a milestone-based roadmap

This repository is intended as a **production-style learning project** demonstrating:

- Backend system design
- Email-driven workflows
- Dockerized deployments
- CI/CD pipelines
- Cloud infrastructure (DigitalOcean)

---

## License

MIT (planned)
