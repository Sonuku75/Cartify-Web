"""Tests for Django startup, app registry, and system configuration."""
from django.test import TestCase
from django.core.management import call_command
from django.conf import settings
from io import StringIO


class StartupConfigurationTests(TestCase):
    """Verifies Django application startup and system configuration."""

    def test_django_system_checks(self):
        """Verify Django system checks report 0 issues."""
        out = StringIO()
        call_command('check', stdout=out)
        output = out.getvalue()
        self.assertIn("System check identified no issues", output)

    def test_all_16_domain_apps_registered(self):
        """Verify all 16 business domain apps plus common are registered in INSTALLED_APPS."""
        expected_apps = [
            'common',
            'apps.users',
            'apps.products',
            'apps.categories',
            'apps.brands',
            'apps.inventory',
            'apps.cart',
            'apps.wishlist',
            'apps.orders',
            'apps.payments',
            'apps.shipping',
            'apps.coupons',
            'apps.reviews',
            'apps.returns',
            'apps.notifications',
            'apps.sellers',
            'apps.cms',
        ]
        for app in expected_apps:
            self.assertIn(app, settings.INSTALLED_APPS, f"App {app} is missing from INSTALLED_APPS")

    def test_rest_framework_configuration(self):
        """Verify REST Framework settings are properly configured."""
        rf_settings = settings.REST_FRAMEWORK
        self.assertIn('rest_framework_simplejwt.authentication.JWTAuthentication', rf_settings['DEFAULT_AUTHENTICATION_CLASSES'])
        self.assertIn('rest_framework.permissions.IsAuthenticated', rf_settings['DEFAULT_PERMISSION_CLASSES'])
        self.assertEqual(rf_settings['EXCEPTION_HANDLER'], 'common.exceptions.custom_exception_handler')
        self.assertEqual(rf_settings['DEFAULT_PAGINATION_CLASS'], 'common.pagination.StandardResultsSetPagination')
