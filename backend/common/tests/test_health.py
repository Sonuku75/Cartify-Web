"""Test suite for the Cartify health check endpoint and core configuration."""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class HealthCheckTests(TestCase):
    """Test suite for GET /api/health/."""

    def setUp(self):
        self.client = APIClient()

    def test_health_check_endpoint_returns_ok(self):
        """Verify GET /api/health/ returns status 200 and expected payload."""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "service": "cartify-api",
            },
        )

    def test_health_check_content_type_json(self):
        """Verify the health check endpoint returns JSON content type."""
        response = self.client.get('/api/health/')
        self.assertTrue(response['Content-Type'].startswith('application/json'))
