"""Common views for Cartify, including system health check."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


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
