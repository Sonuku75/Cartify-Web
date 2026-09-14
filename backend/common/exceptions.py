"""Custom standardized exception handler for Django REST Framework."""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Standardizes error responses across all Cartify APIs.
    Structure:
    {
        "success": false,
        "message": "Human readable message",
        "errors": {}
    }
    Prevents leakage of stack traces, internal paths, or database errors.
    """
    # Call REST framework's default exception handler first to get standard response
    response = exception_handler(exc, context)

    if response is not None:
        errors = response.data
        message = "An error occurred while processing your request."

        # Extract top-level message if present
        if isinstance(errors, dict):
            if "detail" in errors:
                message = str(errors["detail"])
                errors = {"detail": errors["detail"]}
            else:
                message = "Validation failed for one or more fields."
        elif isinstance(errors, list):
            message = "Validation failed."
            errors = {"non_field_errors": errors}

        response.data = {
            "success": false,
            "message": message,
            "errors": errors,
        }
        return response

    # Unhandled exceptions (HTTP 500)
    logger.exception("Unhandled server exception encountered: %s", exc)

    return Response(
        {
            "success": False,
            "message": "An unexpected server error occurred. Please try again later.",
            "errors": {},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
