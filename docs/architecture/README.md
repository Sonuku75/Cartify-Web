# System Architecture Documentation

This directory contains architectural decisions, system blueprints, and component diagrams for the Cartify platform.

## Key Principles
- **Unified Backend Monolith**: A shared Django REST Framework application servicing Web, iOS, and Android.
- **Stateless & Scalable**: Authentication uses JWT tokens; background workloads run via Celery workers backed by Redis.
- **Decoupled Business Domains**: Clear boundaries between product catalog, orders, payments, users, and notifications.
