"""Custom standardized exception handler for Django REST Framework."""
import logging
from typing import Any, Dict
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


def custom_exception_handler(exc: Exception, context: Dict[str, Any]) -> Response:
    """
    Standardizes error responses across all Cartify APIs.
    
    Standardized Error Envelope:
    {
        "success": false,
        "message": "Human readable message",
        "errors": {}
    }
    
    Guarantees that sensitive information such as stack traces, database errors,
    SQL queries, filesystem paths, and internal credentials are NEVER exposed to clients.
    """
    # Call REST framework's default exception handler to get standard HTTP status & detail
    response = exception_handler(exc, context)

    if response is not None:
        errors = response.data
        message = "Something went wrong"

        if isinstance(errors, dict):
            if "detail" in errors:
                message = str(errors["detail"])
                errors = {"detail": errors["detail"]}
            else:
                message = "Validation failed for one or more fields."
        elif isinstance(errors, list):
            message = "Validation failed."
            errors = {"non_field_errors": errors}
        elif isinstance(errors, str):
            message = errors
            errors = {"detail": errors}

        response.data = {
            "success": False,
            "message": message,
            "errors": errors if isinstance(errors, dict) else {"detail": str(errors)},
        }
        return response

    # Unhandled exceptions (HTTP 500)
    # Log full traceback internally for operations/debugging without leaking to clients
    view = context.get('view')
    view_name = view.__class__.__name__ if view else 'UnknownView'
    logger.exception("Unhandled server exception in %s: %s", view_name, exc)

    return Response(
        {
            "success": False,
            "message": "An unexpected server error occurred. Please try again later.",
            "errors": {},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
