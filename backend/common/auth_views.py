"""
Standardized JWT Authentication views for Cartify.
Subclasses SimpleJWT views to enforce consistent API envelopes, rate throttling,
and security logging.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .responses import success_response
from .throttling import AuthBurstRateThrottle


class CartifyTokenObtainPairView(TokenObtainPairView):
    """
    Standardized JWT token obtain endpoint (POST /api/v1/auth/token/).
    Validates user credentials, issues access/refresh tokens, and wraps them in
    the Cartify API envelope.
    """
    throttle_classes = [AuthBurstRateThrottle]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return success_response(
                data=response.data,
                message="Authentication successful",
                status_code=status.HTTP_200_OK,
            )
        return response


class CartifyTokenRefreshView(TokenRefreshView):
    """
    Standardized JWT token refresh endpoint (POST /api/v1/auth/token/refresh/).
    Accepts a valid refresh token, rotates tokens according to security policy,
    and returns the new access token in the standard envelope.
    """
    throttle_classes = [AuthBurstRateThrottle]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return success_response(
                data=response.data,
                message="Token refreshed successfully",
                status_code=status.HTTP_200_OK,
            )
        return response


class CartifyTokenVerifyView(TokenVerifyView):
    """
    Standardized JWT token verification endpoint (POST /api/v1/auth/token/verify/).
    Validates whether a given token is active, unexpired, and not blacklisted.
    """
    throttle_classes = [AuthBurstRateThrottle]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return success_response(
                data={},
                message="Token is valid",
                status_code=status.HTTP_200_OK,
            )
        return response
