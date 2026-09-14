# Security Standards & Policies

This directory outlines the security architecture and defensive engineering practices for Cartify.

## Core Rules
- **Secrets Management**: No credentials, passwords, or keys in source control. All configuration must be provided via environment variables.
- **Transport Security**: HTTPS everywhere; HSTS enabled in production environments.
- **CORS & CSRF**: Explicit allowed origins for frontend applications; CSRF protection where cookies are employed.
- **Input Validation**: Strict serializers on all incoming API requests to prevent injection vulnerabilities.
- **Data Protection**: Passwords hashed using Argon2/PBKDF2; sensitive fields excluded from logs and error responses.
