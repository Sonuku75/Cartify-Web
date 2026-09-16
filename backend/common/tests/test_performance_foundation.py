"""
Automated tests for Cartify Performance Architecture Foundation.
Validates caching parameters, pagination limits, database connection reuse,
and background job configurations to ensure horizontal scaling readiness.
"""
from django.test import SimpleTestCase, RequestFactory
from django.conf import settings
from rest_framework.request import Request
from common.pagination import StandardResultsSetPagination


class TestCachingArchitecture(SimpleTestCase):
    """Verifies that caching infrastructure is structured for high throughput and isolation."""

    def test_cache_configuration_parameters(self):
        """Ensure default cache is registered and properly isolated."""
        self.assertIn('default', settings.CACHES)
        cache_config = settings.CACHES['default']
        self.assertIsNotNone(cache_config.get('BACKEND'))

    def test_redis_connection_pool_readiness(self):
        """Ensure REDIS_URL is configured for production scaling."""
        self.assertTrue(
            settings.REDIS_URL.startswith('redis://'),
            f"Expected redis:// scheme in REDIS_URL, got: {settings.REDIS_URL}",
        )


class TestPaginationArchitecture(SimpleTestCase):
    """Verifies that API pagination prevents memory exhaustion and unbounded queries."""

    def setUp(self):
        self.pagination = StandardResultsSetPagination()
        self.factory = RequestFactory()

    def test_pagination_defaults_and_caps(self):
        """Ensure standard page size is 20 and hard ceiling is 100."""
        self.assertEqual(self.pagination.page_size, 20)
        self.assertEqual(self.pagination.max_page_size, 100)
        self.assertEqual(self.pagination.page_size_query_param, 'page_size')

    def test_pagination_response_envelope(self):
        """Ensure paginated responses return count, next, previous, and results."""
        mock_data = [{'id': i, 'title': f'Product {i}'} for i in range(1, 21)]
        django_req = self.factory.get('/api/v1/products/?page=1&page_size=20')
        drf_req = Request(django_req)

        # Paginate mock queryset
        paginated_page = self.pagination.paginate_queryset(mock_data, drf_req)
        response = self.pagination.get_paginated_response(paginated_page)

        self.assertEqual(response.status_code, 200)
        envelope = response.data
        self.assertTrue(envelope['success'])
        self.assertEqual(envelope['message'], 'Request successful')

        data = envelope['data']
        self.assertIn('count', data)
        self.assertIn('next', data)
        self.assertIn('previous', data)
        self.assertIn('results', data)
        self.assertEqual(data['count'], 20)
        self.assertEqual(len(data['results']), 20)


class TestDatabaseScalingArchitecture(SimpleTestCase):
    """Verifies connection management settings designed for horizontal scalability."""

    def test_connection_max_age_persistent_connections(self):
        """Ensure CONN_MAX_AGE enables connection reuse across requests."""
        db_config = settings.DATABASES['default']
        conn_max_age = db_config.get('CONN_MAX_AGE', 0)
        self.assertGreaterEqual(
            conn_max_age,
            600,
            f"CONN_MAX_AGE should be at least 600 seconds for connection pooling, got: {conn_max_age}",
        )

    def test_connection_health_checks_enabled(self):
        """Ensure CONN_HEALTH_CHECKS is True to discard terminated connections."""
        db_config = settings.DATABASES['default']
        self.assertTrue(
            db_config.get('CONN_HEALTH_CHECKS', False),
            "CONN_HEALTH_CHECKS must be enabled for reliable connection pooling.",
        )

    def test_stateless_authentication_architecture(self):
        """Ensure REST Framework uses stateless JWT rather than database sessions by default."""
        auth_classes = settings.REST_FRAMEWORK.get('DEFAULT_AUTHENTICATION_CLASSES', ())
        self.assertIn(
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            auth_classes,
            "Stateless JWT authentication must be the default authentication class.",
        )


class TestBackgroundJobArchitecture(SimpleTestCase):
    """Verifies that background jobs scale horizontally without blocking request threads."""

    def test_celery_task_serializer_is_json(self):
        """Ensure safe and performant JSON task serialization."""
        self.assertEqual(settings.CELERY_TASK_SERIALIZER, 'json')
        self.assertEqual(settings.CELERY_RESULT_SERIALIZER, 'json')
        self.assertEqual(settings.CELERY_ACCEPT_CONTENT, ['json'])

    def test_celery_result_expires(self):
        """Ensure task results in Redis expire to prevent unbounded memory growth."""
        self.assertGreaterEqual(
            getattr(settings, 'CELERY_RESULT_EXPIRES', 0),
            3600,
            "CELERY_RESULT_EXPIRES must be set to prevent Redis memory leaks from stale task results.",
        )

    def test_celery_broker_reconnect_on_startup(self):
        """Ensure Celery retries broker connection on startup for resilience."""
        self.assertTrue(
            getattr(settings, 'CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP', False),
            "CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP must be True for worker resilience.",
        )
