#!/usr/bin/env bash
# ==============================================================================
# Cartify Monorepo Unified Quality & Testing Verification Script
# Executes end-to-end verification across Django REST backend and Next.js website.
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

VENV_PYTHON="${ROOT_DIR}/backend/venv/bin/python"

if [[ ! -x "${VENV_PYTHON}" ]]; then
    echo "Error: Virtual environment python not found at ${VENV_PYTHON}"
    exit 1
fi

echo "=============================================================================="
echo "                   CARTIFY MONOREPO QUALITY CHECKS                            "
echo "=============================================================================="

# 1. Django Standard System Checks
echo ""
echo "--> [1/7] Running Django System Checks..."
"${VENV_PYTHON}" "${ROOT_DIR}/backend/manage.py" check

# 2. Django Production Deployment Security Audit
echo ""
echo "--> [2/7] Running Django Deployment Security Audit..."
DJANGO_DEBUG=False \
DJANGO_SECURE_SSL_REDIRECT=True \
DJANGO_SECRET_KEY="cartify-production-audit-secret-key-with-more-than-fifty-characters-long!" \
DJANGO_ALLOWED_HOSTS="api.cartify.com" \
"${VENV_PYTHON}" "${ROOT_DIR}/backend/manage.py" check --deploy

# 3. Backend Unit, Security & Performance Test Suite
echo ""
echo "--> [3/7] Running Backend Test Suite (Startup, DB, Health, Errors, Celery/Redis, Security, Performance, Users)..."
"${VENV_PYTHON}" "${ROOT_DIR}/backend/manage.py" test common.tests apps.users --verbosity=1

# 4. Next.js TypeScript Compilation
echo ""
echo "--> [4/7] Running Next.js TypeScript Type Check..."
(cd "${ROOT_DIR}/website" && npm run type-check)

# 5. Next.js ESLint Check
echo ""
echo "--> [5/7] Running Next.js ESLint..."
(cd "${ROOT_DIR}/website" && npm run lint)

# 6. Next.js Component, Theme, Responsive & API Client Tests
echo ""
echo "--> [6/7] Running Next.js Component & API Client Tests (Vitest)..."
(cd "${ROOT_DIR}/website" && npm run test)

# 7. Next.js Production Build
echo ""
echo "--> [7/7] Running Next.js Production Build..."
(cd "${ROOT_DIR}/website" && npm run build)

echo ""
echo "=============================================================================="
echo "      ALL 7 QUALITY CHECKS COMPLETED SUCCESSFULLY (100% PASSING)              "
echo "=============================================================================="
