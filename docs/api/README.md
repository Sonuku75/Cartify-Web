# API Standards & Specifications

This directory contains specifications, contracts, and guidelines for Cartify's REST APIs.

## Guidelines
- **Versioning**: All public domain endpoints are versioned under `/api/v1/`.
- **System Monitoring**: Base health checks reside at `/api/health/`.
- **Payload Format**: Standard JSON requests and responses.
- **Error Format**:
  ```json
  {
    "success": false,
    "message": "Human-readable description of error",
    "errors": {}
  }
  ```
- **Authentication**: `Authorization: Bearer <access_token>` headers via SimpleJWT.
