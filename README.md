# Cartify — Fashion E-Commerce Platform

Cartify is a modern, production-grade fashion e-commerce platform architected to deliver a unified, high-performance shopping experience across web, iOS, and Android clients.

---

## Architecture Overview

All Cartify client applications interface with a single centralized REST API and a shared PostgreSQL database, ensuring complete consistency of product catalogs, carts, orders, inventories, and user state across all devices.

```
┌─────────────────────────────────────────────────────────────┐
│                       Cartify Clients                       │
│                                                             │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────┐   │
│   │ Responsive Web  │   │     iOS App     │   │ Android │   │
│   │  (Next.js App)  │   │ (Swift/SwiftUI) │   │(Flutter)│   │
│   └────────┬────────┘   └────────┬────────┘   └────┬────┘   │
└────────────┼─────────────────────┼─────────────────┼────────┘
             │                     │                 │
             └───────────────┬─────┴─────────────────┘
                             │ HTTPS / JSON REST API
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Cartify Shared Backend                   │
│                                                             │
│       Django & Django REST Framework (Modular Monolith)      │
│                                                             │
│   ┌───────────────┐   ┌────────────────┐   ┌────────────┐   │
│   │ SimpleJWT Auth│   │ Throttling/CORS│   │ API v1 End │   │
│   └───────────────┘   └────────────────┘   └────────────┘   │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
    ┌────────────────────┐          ┌────────────────────┐
    │  PostgreSQL 16+    │          │     Redis 7+       │
    │ (Relational Data)  │          │ (Cache & Broker)   │
    └────────────────────┘          └──────────┬─────────┘
                                               │
                                               ▼
                                    ┌────────────────────┐
                                    │   Celery Workers   │
                                    │ (Background Tasks) │
                                    └────────────────────┘
```

---

## Technology Stack

| Domain | Technology | Description |
| :--- | :--- | :--- |
| **Web Client** | Next.js (App Router), TypeScript, Tailwind CSS | Responsive, SEO-optimized e-commerce storefront |
| **iOS Client** | Swift, SwiftUI, Xcode | Native iOS experience (planned) |
| **Android Client** | Flutter, Dart | Cross-platform native mobile experience (planned) |
| **Backend Framework** | Python, Django, Django REST Framework | Clean, modular REST API monolith |
| **Database** | PostgreSQL | Scalable ACID relational database with connection pooling |
| **Cache & Broker** | Redis | High-speed in-memory caching and message broker |
| **Task Queue** | Celery | Asynchronous background processing |
| **Authentication** | JWT (SimpleJWT) | Stateless token-based auth shared across all clients |

---

## Monorepo Repository Structure

```
Cartify/
│
├── backend/            # Django REST Framework backend application
│   ├── config/         # Core settings, routing, Celery, WSGI/ASGI
│   ├── apps/           # Modular domain applications (users, products, orders, etc.)
│   ├── manage.py       # Django CLI entrypoint
│   └── requirements.txt# Backend Python dependencies
│
├── website/            # Next.js responsive web application
│   ├── src/app/        # App router layouts, pages, and components
│   ├── package.json    # Website dependencies and scripts
│   └── tailwind.config.ts # Tailwind CSS configuration
│
├── mobile/             # Android application using Flutter (placeholder)
├── ios/                # iOS application using Swift/SwiftUI (placeholder)
│
├── docs/               # System architecture, API specs, and engineering guides
│   ├── architecture/   # Architectural design records and component diagrams
│   ├── api/            # API design standards, versioning, and endpoints
│   ├── database/       # Database schemas, indexing rules, and migration policies
│   ├── security/       # Security standards, auth flow, and vulnerability defense
│   └── development/    # Contribution guides, branching strategy, and code reviews
│
├── .gitignore          # Repository-wide ignore rules
├── .env.example        # Environment variable definitions template
└── README.md           # Workspace root documentation
```

---

## Development Philosophy

1. **Stateless REST Architecture**: The backend maintains no session state, allowing horizontal scaling behind load balancers.
2. **Single Source of Truth**: All business logic and domain rules reside in the backend. Clients are lightweight presentation layers.
3. **Modular Monolith**: Organized into decoupled domain apps (`users`, `products`, `orders`, `cart`, etc.) to prevent premature microservice complexity while allowing straightforward evolution.
4. **Security by Default**: Strict CORS policies, CSRF controls, parameterized SQL, rate-limiting, and zero hardcoded secrets.
5. **Continuous Verification**: High automated test coverage, linting, and strict type safety across Python and TypeScript.

---

## Planned Applications & Modules

- [x] **Module 1.1**: Project & Repository Foundation (Current)
- [ ] **Module 1.2**: Core Backend Infrastructure & Production Settings
- [ ] **Module 2**: Authentication & User Identity Management
- [ ] **Module 3**: Category & Product Catalog Engine
- [ ] **Module 4**: Cart & Wishlist System
- [ ] **Module 5**: Order Processing & Inventory Management
- [ ] **Module 6**: Payment Gateway Integration
- [ ] **Module 7**: Customer Reviews & Ratings
- [ ] **Module 8**: Promotions, Coupons & Discounts
- [ ] **Module 9**: Multi-Vendor Seller System
- [ ] **Module 10**: Real-time Notifications & Alerts
- [ ] **Module 11**: Next.js Storefront Implementation
- [ ] **Module 12**: iOS SwiftUI Native Application
- [ ] **Module 13**: Android Flutter Application

---

## Backend Architecture

The backend is built with Django and Django REST Framework using a modular design:
- **`config/`**: Contains global configuration, environment ingestion via `django-environ`, logging, database pooling, Celery integration, and root URL routing.
- **`apps/common/`**: Houses cross-cutting concerns including standardized exception handling, pagination, health checks, and base utilities.
- **`apps/<domain>/`**: Independent domain applications encapsulating models, views, serializers, tests, and business logic.
- **API Versioning**: All API endpoints are namespaced under `/api/v1/`, while system monitoring uses `/api/health/`.

---

## Frontend Architecture

The web application is built with Next.js App Router:
- **Server Components by Default**: High-speed initial load and SEO optimization for catalog pages.
- **Client Components for Interactivity**: Carts, search filters, checkouts, and customer account portals.
- **Tailwind CSS**: Utility-first styling with design system tokens tailored for an upscale fashion e-commerce brand.
- **Unified API Client**: Type-safe HTTP client communicating with `/api/v1/`.

---

## Setup Instructions (Placeholder)

Detailed local development setup instructions will be provided in upcoming modules as runtime services are configured.

- **Prerequisites**: Python 3.12+, Node.js 20+, PostgreSQL 16+, Redis 7+
- **Documentation**: See [docs/development/](docs/development/README.md) for workflow details.
