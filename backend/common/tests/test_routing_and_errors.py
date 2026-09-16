"""Tests for API routing, status codes, and exception sanitization."""
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.urls import path


class MockAuthenticatedView(APIView):
    """Protected endpoint for testing unauthenticated access."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return APIView().http_method_not_allowed(request)


class MockValidationFailView(APIView):
    """Endpoint for testing validation error handling."""
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        raise ValidationError({"email": ["Invalid email address format."]})


class MockCrashingView(APIView):
    """Endpoint for testing unhandled 500 error sanitization."""
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        # Simulate unexpected database/internal failure
        raise RuntimeError("CRITICAL_DATABASE_CRASH: table /var/postgres/cartify.db corrupt")


# Test URLs for routing & error checks
urlpatterns = [
    path('test-protected/', MockAuthenticatedView.as_view()),
    path('test-validation/', MockValidationFailView.as_view()),
    path('test-crash/', MockCrashingView.as_view()),
]


class RoutingAndErrorHandlingTests(TestCase):
    """Verifies API routing and standardized error responses."""

    def setUp(self):
        self.client = APIClient()

    def test_health_check_routing(self):
        """GET /api/health/ resolves and responds with lightweight status."""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "service": "cartify-api",
            },
        )

    def test_api_v1_root_routing(self):
        """GET /api/v1/ resolves and responds with standardized API v1 status."""
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Cartify REST API v1 active")
        self.assertEqual(data["data"]["version"], "v1")
        self.assertEqual(data["data"]["status"], "online")

    def test_unmapped_api_route_404(self):
        """GET to non-existent endpoint returns standardized 404 error envelope."""
        response = self.client.get('/api/v1/non-existent-endpoint/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("not found", data["message"].lower())
        self.assertIsInstance(data["errors"], dict)

    def test_method_not_allowed_405(self):
        """POST to GET-only endpoint returns standardized 405 error envelope."""
        response = self.client.post('/api/v1/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("not allowed", data["message"].lower())
        self.assertIn("detail", data["errors"])

    @override_settings(ROOT_URLCONF=__name__)
    def test_unauthenticated_request_401(self):
        """Protected endpoint returns standardized 401 error envelope when token is missing."""
        response = self.client.get('/test-protected/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("detail", data["errors"])
        self.assertIn("credentials were not provided", str(data["errors"]["detail"]).lower())

    @override_settings(ROOT_URLCONF=__name__)
    def test_validation_error_400(self):
        """Endpoint throwing ValidationError returns standardized 400 error envelope."""
        response = self.client.post('/test-validation/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Validation failed for one or more fields.")
        self.assertIn("email", data["errors"])
        self.assertEqual(data["errors"]["email"], ["Invalid email address format."])

    @override_settings(ROOT_URLCONF=__name__)
    def test_unhandled_500_exception_sanitization(self):
        """Unhandled server exception returns 500 without leaking stack traces or internal paths."""
        # Suppress test runner logging the simulated crash
        with self.assertLogs('common.exceptions', level='ERROR') as cm:
            response = self.client.get('/test-crash/')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(
            data["message"],
            "An unexpected server error occurred. Please try again later.",
        )
        self.assertEqual(data["errors"], {})

        # Ensure raw exception details are NOT exposed to the client
        raw_response_text = response.content.decode('utf-8')
        self.assertNotIn("CRITICAL_DATABASE_CRASH", raw_response_text)
        self.assertNotIn("/var/postgres", raw_response_text)
        self.assertNotIn("Traceback", raw_response_text)

        # Ensure the error was captured in internal server logs
        self.assertTrue(any("CRITICAL_DATABASE_CRASH" in msg for msg in cm.output))
