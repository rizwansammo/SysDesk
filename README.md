# SysDesk -- Multi‑Tenant SaaS Helpdesk System

SysDesk is a **production‑ready multi‑tenant helpdesk ticketing system**
designed for MSP‑style IT support teams.\
It allows support providers to manage tickets from multiple
organizations within a unified platform.

This project is being built with **clean architecture, scalable backend
services, and a modern frontend stack**.

------------------------------------------------------------------------

# Overview

SysDesk enables IT support providers to manage support requests across
many organizations while maintaining strict tenant separation.

Example:

Support Provider manages:

-   TechLab
-   Acme Corp
-   StartupHub

Each organization has its own users and tickets, but agents manage
everything from one portal.

------------------------------------------------------------------------

# Key Features (MVP)

## Multi‑Tenant Architecture

-   Multiple organizations (tenants)
-   Users linked to organizations
-   Agents can manage tickets across all organizations

## Role Based Access

Roles supported:

-   Super Admin
-   Agent
-   End User
-   VIP User

VIP users can receive higher priority handling.

------------------------------------------------------------------------

# Ticket Management

Tickets include:

-   Ticket Number
-   Subject
-   Description
-   Organization
-   Created By
-   Assigned Agent
-   Status
-   Priority
-   Category
-   Attachments
-   Replies
-   History tracking

Statuses:

-   Open
-   Pending
-   Resolved
-   Closed

Priority levels:

-   Low
-   Medium
-   High
-   Critical

------------------------------------------------------------------------

# Ticket Features

Supported functionality:

-   Ticket creation
-   Ticket assignment
-   Internal notes
-   Public replies
-   Attachments
-   Ticket history tracking
-   Ticket status changes
-   Merge tickets
-   Reopen tickets

Internal notes are **visible only to agents**.

------------------------------------------------------------------------

# Knowledge Base

SysDesk includes a Knowledge Base system.

Types:

-   Public articles (visible to customers)
-   Internal articles (visible only to agents)

Capabilities:

-   Article search
-   Category grouping
-   Draft / Published / Archived states

Customers only see **public published articles**.

------------------------------------------------------------------------

# Authentication

Authentication uses:

-   JWT tokens
-   Access tokens
-   Refresh tokens

Endpoints:

    POST /api/v1/auth/login/
    POST /api/v1/auth/refresh/
    GET  /api/v1/auth/me/

------------------------------------------------------------------------

# API Endpoints

## Users

    GET  /api/v1/users/
    POST /api/v1/users/
    GET  /api/v1/users/{id}/
    PATCH /api/v1/users/{id}/

## Agents

    GET /api/v1/agents/

## Organizations

    GET  /api/v1/organizations/
    POST /api/v1/organizations/
    GET  /api/v1/organizations/{id}/
    PATCH /api/v1/organizations/{id}/

## Tickets

    GET  /api/v1/tickets/
    POST /api/v1/tickets/
    GET  /api/v1/tickets/{id}/
    PATCH /api/v1/tickets/{id}/
    POST /api/v1/tickets/{id}/reply/
    POST /api/v1/tickets/{id}/assign/

## Knowledge Base

    GET  /api/v1/knowledge-base/articles/
    POST /api/v1/knowledge-base/articles/
    GET  /api/v1/knowledge-base/articles/{id}/
    PATCH /api/v1/knowledge-base/articles/{id}/
    GET  /api/v1/knowledge-base/search/?q=keyword

------------------------------------------------------------------------

# Technology Stack

## Backend

-   Python
-   Django
-   Django REST Framework
-   PostgreSQL (planned for production)
-   Redis
-   Celery
-   JWT Authentication

## Frontend (planned)

-   Next.js
-   React
-   TypeScript
-   Tailwind CSS

------------------------------------------------------------------------

# Project Structure

    SysDesk
    │
    ├── backend
    │   ├── accounts
    │   ├── organizations
    │   ├── tickets
    │   ├── knowledge_base
    │   ├── config
    │   └── manage.py
    │
    ├── frontend
    │   └── (Next.js app)
    │
    └── README.md

------------------------------------------------------------------------

# Setup Instructions

## 1. Clone the repository

    git clone https://github.com/yourusername/sysdesk.git
    cd sysdesk/backend

## 2. Create virtual environment

Windows:

    python -m venv .venv
    .venv\Scripts\activate

Linux / Mac:

    python3 -m venv .venv
    source .venv/bin/activate

## 3. Install dependencies

    pip install -r requirements.txt

------------------------------------------------------------------------

# Run Migrations

    python manage.py makemigrations
    python manage.py migrate

------------------------------------------------------------------------

# Create Super User

    python manage.py createsuperuser

------------------------------------------------------------------------

# Run Development Server

    python manage.py runserver

Server will run at:

    http://127.0.0.1:8000

Admin panel:

    http://127.0.0.1:8000/admin

------------------------------------------------------------------------

# Example Workflow

Customer submits ticket via portal.

Agent receives ticket.

Agent actions:

1.  Review ticket
2.  Add internal notes
3.  Reply to customer
4.  Assign ticket
5.  Resolve issue

Customer sees:

-   Ticket updates
-   Agent replies
-   Ticket status

Customer **cannot see internal notes**.

------------------------------------------------------------------------

# Security

SysDesk implements:

-   JWT authentication
-   Role based permissions
-   Tenant isolation
-   Internal note protection
-   Protected endpoints

------------------------------------------------------------------------

# Future Features

Planned upcoming features:

-   SLA system
-   Automation rules
-   Email‑to‑ticket integration
-   Reporting dashboard
-   Audit logs
-   Redis + Celery background jobs
-   Full Next.js frontend portal
-   Agent dashboard UI
-   Customer portal UI

------------------------------------------------------------------------

# Deployment (Planned)

Production stack will include:

-   Docker
-   PostgreSQL
-   Redis
-   Nginx
-   Gunicorn

------------------------------------------------------------------------

# License

MIT License

------------------------------------------------------------------------

# Author

SysDesk is being developed as a **production‑grade SaaS helpdesk
platform**.

Created by:

Rizwan Sammo
