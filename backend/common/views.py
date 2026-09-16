"""Common views for Cartify, including system health check, API root, and error handlers."""
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .responses import success_response


class HealthCheckView(APIView):
    """
    Lightweight health check endpoint.
    Used by orchestrators, load balancers, and monitoring systems to verify service uptime.
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()
    throttle_classes = ()

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "status": "ok",
                "service": "cartify-api",
            },
            status=status.HTTP_200_OK,
        )


class APIVersionView(APIView):
    """
    Version 1 API root status endpoint.
    Verifies that the /api/v1/ namespace is active and reachable across all clients.
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return success_response(
            data={
                "version": "v1",
                "status": "online",
            },
            message="Cartify REST API v1 active",
            status_code=status.HTTP_200_OK,
        )


def custom_404_view(request, exception=None):
    """Fallback JSON 404 handler for routes not caught by REST Framework."""
    return JsonResponse(
        {
            "success": False,
            "message": "The requested endpoint was not found.",
            "errors": {},
        },
        status=status.HTTP_404_NOT_FOUND,
    )


def custom_500_view(request):
    """Fallback JSON 500 handler for unexpected server-level exceptions."""
    return JsonResponse(
        {
            "success": False,
            "message": "An unexpected server error occurred. Please try again later.",
            "errors": {},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
