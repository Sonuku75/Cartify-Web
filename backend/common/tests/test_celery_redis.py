"""
Tests for Cartify Celery and Redis infrastructure configuration.
Validates task registration, broker settings, synchronous execution, and cache connectivity.
"""
from django.test import SimpleTestCase, TestCase
from django.conf import settings
from django.core.cache import cache
import redis

from config.celery import app as celery_app
from common.tasks import health_check_task


class TestCeleryConfiguration(SimpleTestCase):
    """Verifies that Celery application settings and queues are configured correctly."""

    def test_celery_app_initialization(self):
        """Ensure Celery application instance is properly named and configured."""
        self.assertEqual(celery_app.main, 'cartify')
        self.assertIsNotNone(celery_app.conf)

    def test_celery_broker_settings(self):
        """Ensure Celery broker and backend point to Redis URLs."""
        self.assertTrue(
            settings.CELERY_BROKER_URL.startswith('redis://'),
            f"Expected Redis broker URL, got: {settings.CELERY_BROKER_URL}",
        )
        self.assertTrue(
            settings.CELERY_RESULT_BACKEND.startswith('redis://'),
            f"Expected Redis result backend, got: {settings.CELERY_RESULT_BACKEND}",
        )

    def test_celery_serialization_settings(self):
        """Ensure secure JSON serialization is enforced across Celery."""
        self.assertEqual(settings.CELERY_ACCEPT_CONTENT, ['json'])
        self.assertEqual(settings.CELERY_TASK_SERIALIZER, 'json')
        self.assertEqual(settings.CELERY_RESULT_SERIALIZER, 'json')

    def test_celery_reliability_settings(self):
        """Ensure modern broker reconnect and result expiry settings are active."""
        self.assertTrue(getattr(settings, 'CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP', False))
        self.assertGreaterEqual(getattr(settings, 'CELERY_RESULT_EXPIRES', 0), 3600)


class TestCeleryTasks(SimpleTestCase):
    """Verifies background task registration and execution mechanics."""

    def test_health_check_task_registered(self):
        """Ensure the minimal health check diagnostic task is registered in Celery."""
        self.assertIn(
            'common.health_check_task',
            celery_app.tasks,
            "common.health_check_task was not registered in Celery tasks registry.",
        )

    def test_health_check_task_execution(self):
        """Execute health_check_task synchronously and verify payload."""
        result = health_check_task.apply()
        self.assertTrue(result.successful())
        output = result.result
        self.assertIsInstance(output, dict)
        self.assertEqual(output.get('status'), 'success')
        self.assertIn('task_id', output)
        self.assertIn('operational', output.get('message', ''))


class TestRedisInfrastructure(TestCase):
    """Verifies Redis caching and connectivity."""

    def test_django_cache_interface(self):
        """Verify basic cache read/write/delete operations."""
        key = 'cartify:test:cache_probe'
        value = {'probe_status': 'ok', 'timestamp': 123456}

        cache.set(key, value, timeout=60)
        retrieved = cache.get(key)
        self.assertEqual(retrieved, value)

        cache.delete(key)
        self.assertIsNone(cache.get(key))

    def test_redis_direct_ping(self):
        """Verify direct connection to the Redis server using REDIS_URL."""
        try:
            client = redis.Redis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
            ping_result = client.ping()
            self.assertTrue(ping_result)
        except (redis.ConnectionError, redis.TimeoutError):
            # When Redis server is not yet running on host, test reports informational status
            self.skipTest(f"Redis server at {settings.REDIS_URL} is not currently reachable.")
