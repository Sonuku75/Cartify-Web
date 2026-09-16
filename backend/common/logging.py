"""
Security logging filters and sanitizers for Cartify.
Ensures that credentials, tokens, passwords, and sensitive financial/PII data
are never exposed in application logs.
"""
import logging
import re
from typing import Any

# Sensitive key patterns in JSON / dictionaries
JSON_SENSITIVE_PATTERN = re.compile(
    r'(?i)(["\']?(?:password|passwd|secret|access_token|refresh_token|token|api_key|apiKey|cvv|cvc|card_number)["\']?\s*[:=]\s*["\'])([^"\']+)(["\'])'
)

# Sensitive parameters in URLs or query strings
QUERY_SENSITIVE_PATTERN = re.compile(
    r'(?i)(password|passwd|secret|token|api_key|apiKey)=([^&\s]+)'
)

# Bearer authorization header patterns
BEARER_TOKEN_PATTERN = re.compile(
    r'(?i)(Bearer\s+)[A-Za-z0-9_\-\.]+'
)

# Credit card number patterns (13 to 19 digits with optional hyphens/spaces)
CREDIT_CARD_PATTERN = re.compile(
    r'\b(?:\d[ -]*?){13,19}\b'
)


def sanitize_message(message: Any) -> str:
    """Sanitizes sensitive information from a string message."""
    if not isinstance(message, str):
        message = str(message)

    # Mask Bearer tokens
    message = BEARER_TOKEN_PATTERN.sub(r'\1[REDACTED_TOKEN]', message)

    # Mask JSON sensitive fields
    message = JSON_SENSITIVE_PATTERN.sub(r'\1[REDACTED]\3', message)

    # Mask query parameters
    message = QUERY_SENSITIVE_PATTERN.sub(r'\1=[REDACTED]', message)

    # Mask credit card numbers
    message = CREDIT_CARD_PATTERN.sub(r'[REDACTED_CARD]', message)

    return message


class SensitiveDataFilter(logging.Filter):
    """
    Logging filter that sanitizes sensitive data from log records.
    Applied across console and persistent handlers.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            if isinstance(record.msg, str):
                record.msg = sanitize_message(record.msg)

            if record.args:
                if isinstance(record.args, dict):
                    record.args = {
                        k: sanitize_message(v) if isinstance(v, str) else v
                        for k, v in record.args.items()
                    }
                elif isinstance(record.args, tuple):
                    record.args = tuple(
                        sanitize_message(arg) if isinstance(arg, str) else arg
                        for arg in record.args
                    )
        except Exception:
            # Fallback safely: never break the logging pipeline on filter errors
            pass

        return True
