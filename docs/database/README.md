# Database Architecture & Guidelines

This directory documents Cartify's PostgreSQL database design, schema migrations, and indexing strategies.

## Guidelines
- **RDBMS**: PostgreSQL 16+ is the primary transactional datastore.
- **ORM**: Django ORM with declarative models and migration histories.
- **Connection Management**: Persistent database connections with connection pooling (`CONN_MAX_AGE`) and health checking enabled.
- **Integrity**: Explicit foreign key constraints, indexes on query filters, and transactional atomic blocks for financial operations.
