"""Standardized API response utilities for Cartify REST APIs."""
from typing import Any, Optional
from rest_framework.response import Response
from rest_framework import status


def success_response(
    data: Optional[Any] = None,
    message: str = "Request successful",
    status_code: int = status.HTTP_200_OK,
    **kwargs: Any
) -> Response:
    """
    Constructs a standardized success response.
    
    Format:
    {
        "success": true,
        "message": "Request successful",
        "data": {}
    }
    """
    payload = {
        "success": True,
        "message": message,
        "data": data if data is not None else {},
    }
    return Response(payload, status=status_code, **kwargs)


def error_response(
    errors: Optional[Any] = None,
    message: str = "Something went wrong",
    status_code: int = status.HTTP_400_BAD_REQUEST,
    **kwargs: Any
) -> Response:
    """
    Constructs a standardized error response.
    
    Format:
    {
        "success": false,
        "message": "Something went wrong",
        "errors": {}
    }
    """
    payload = {
        "success": False,
        "message": message,
        "errors": errors if errors is not None else {},
    }
    return Response(payload, status=status_code, **kwargs)
