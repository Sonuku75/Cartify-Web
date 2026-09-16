"""
Automated tests for Cartify Security Foundation.
Validates Django security defaults, JWT token lifecycle, permission boundaries,
sensitive data logging redaction, and file upload validation.
"""
import io
import logging
from django.test import SimpleTestCase, TestCase, RequestFactory
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse

User = get_user_model()
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from common.logging import SensitiveDataFilter, sanitize_message
from common.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsStaffUser, PublicEndpoint
from common.file_security import (
    sanitize_filename,
    generate_secure_filename,
    detect_mime_from_magic_bytes,
    validate_image_file,
    MAX_IMAGE_FILE_SIZE,
)


class DummyProtectedView(APIView):
    """Temporary test view for verifying JWT authentication boundaries."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"user": request.user.get_username()})


class DummyOwnerObject:
    """Mock object for testing ownership permissions."""
    def __init__(self, user):
        self.user = user


class TestDjangoSecuritySettings(SimpleTestCase):
    """Verifies security middleware, headers, cookies, and upload constraints."""

    def test_security_middleware_configured(self):
        """Ensure SecurityMiddleware and CorsMiddleware are properly ordered."""
        self.assertIn('django.middleware.security.SecurityMiddleware', settings.MIDDLEWARE)
        self.assertIn('corsheaders.middleware.CorsMiddleware', settings.MIDDLEWARE)
        sec_idx = settings.MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
        cors_idx = settings.MIDDLEWARE.index('corsheaders.middleware.CorsMiddleware')
        self.assertLess(sec_idx, cors_idx, "SecurityMiddleware should execute before CorsMiddleware.")

    def test_cookie_security_flags(self):
        """Ensure cookies are protected against XSS and cross-site requests."""
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, 'Lax')
        self.assertEqual(settings.CSRF_COOKIE_SAMESITE, 'Lax')

    def test_security_headers_enabled(self):
        """Ensure browser defense headers are configured."""
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertEqual(settings.X_FRAME_OPTIONS, 'DENY')
        self.assertEqual(settings.SECURE_REFERRER_POLICY, 'strict-origin-when-cross-origin')
        self.assertEqual(settings.SECURE_CROSS_ORIGIN_OPENER_POLICY, 'same-origin')
        self.assertEqual(settings.SECURE_PROXY_SSL_HEADER, ('HTTP_X_FORWARDED_PROTO', 'https'))

    def test_upload_and_body_limits(self):
        """Ensure denial-of-service protections via request body and file upload limits."""
        self.assertLessEqual(settings.DATA_UPLOAD_MAX_MEMORY_SIZE, 10 * 1024 * 1024)
        self.assertLessEqual(settings.FILE_UPLOAD_MAX_MEMORY_SIZE, 10 * 1024 * 1024)
        self.assertEqual(settings.DATA_UPLOAD_MAX_NUMBER_FIELDS, 1000)
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)


class TestJWTSecurityAndLifecycle(TestCase):
    """Verifies JWT token issuance, verification, rotation, and authorization enforcement."""

    def setUp(self):
        cache.clear()
        self.email = 'security@cartify.com'
        self.password = 'ComplexPassw0rd!2026'
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
        )
        self.factory = RequestFactory()

    def test_jwt_token_obtain_success(self):
        """Valid credentials return access and refresh tokens wrapped in Cartify envelope."""
        url = reverse('api_v1:token_obtain_pair')
        response = self.client.post(
            url,
            {'email': self.email, 'password': self.password},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('message'), "Authentication successful")
        self.assertIn('access', data.get('data', {}))
        self.assertIn('refresh', data.get('data', {}))

    def test_jwt_token_obtain_failure_standardized(self):
        """Invalid credentials return standardized 401 error envelope without leaking details."""
        url = reverse('api_v1:token_obtain_pair')
        response = self.client.post(
            url,
            {'email': self.email, 'password': 'WrongPassword123'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        data = response.json()
        self.assertFalse(data.get('success'))
        self.assertIn('errors', data)

    def test_jwt_token_refresh_and_rotation(self):
        """Refreshing a token returns a new access token and rotates the refresh token."""
        url_obtain = reverse('api_v1:token_obtain_pair')
        obtain_res = self.client.post(
            url_obtain,
            {'email': self.email, 'password': self.password},
            format='json',
        )
        refresh_token = obtain_res.json()['data']['refresh']

        url_refresh = reverse('api_v1:token_refresh')
        refresh_res = self.client.post(
            url_refresh,
            {'refresh': refresh_token},
            format='json',
        )
        self.assertEqual(refresh_res.status_code, status.HTTP_200_OK)
        data = refresh_res.json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('message'), "Token refreshed successfully")
        self.assertIn('access', data.get('data', {}))

    def test_jwt_token_verify(self):
        """Token verify endpoint confirms validity in standard envelope."""
        url_obtain = reverse('api_v1:token_obtain_pair')
        obtain_res = self.client.post(
            url_obtain,
            {'email': self.email, 'password': self.password},
            format='json',
        )
        access_token = obtain_res.json()['data']['access']

        url_verify = reverse('api_v1:token_verify')
        verify_res = self.client.post(
            url_verify,
            {'token': access_token},
            format='json',
        )
        self.assertEqual(verify_res.status_code, status.HTTP_200_OK)
        data = verify_res.json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('message'), "Token is valid")

    def test_authentication_boundary_enforcement(self):
        """Protected views accept valid Bearer tokens and reject unauthenticated requests."""
        url_obtain = reverse('api_v1:token_obtain_pair')
        obtain_res = self.client.post(
            url_obtain,
            {'email': self.email, 'password': self.password},
            format='json',
        )
        access_token = obtain_res.json()['data']['access']

        view = DummyProtectedView.as_view()

        # Unauthenticated request
        req_unauth = self.factory.get('/test-protected/')
        res_unauth = view(req_unauth)
        self.assertEqual(res_unauth.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated request with Bearer header
        req_auth = self.factory.get(
            '/test-protected/',
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
        )
        res_auth = view(req_auth)
        self.assertEqual(res_auth.status_code, status.HTTP_200_OK)
        self.assertEqual(res_auth.data.get('user'), self.email)

    def test_auth_burst_throttling(self):
        """Repeated requests beyond the auth_burst limit trigger HTTP 429 Too Many Requests."""
        url = reverse('api_v1:token_obtain_pair')
        payload = {'email': self.email, 'password': self.password}

        # Issue 5 requests (the default burst limit)
        for _ in range(5):
            res = self.client.post(url, payload, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)

        # 6th request must be throttled
        throttled_res = self.client.post(url, payload, format='json')
        self.assertEqual(throttled_res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        data = throttled_res.json()
        self.assertFalse(data.get('success'))
        self.assertIn('throttled', data.get('message', '').lower())



class TestPermissionsFramework(TestCase):
    """Verifies standard permission boundaries."""

    def setUp(self):
        self.factory = RequestFactory()
        self.regular_user = User.objects.create_user(email='regular_user@cartify.com', password='pass')
        self.staff_user = User.objects.create_user(email='staff_user@cartify.com', password='pass', is_staff=True)

    def test_is_admin_or_read_only(self):
        """Safe methods allowed for all; write methods require staff."""
        permission = IsAdminOrReadOnly()

        # GET request from anonymous
        req_get = self.factory.get('/items/')
        req_get.user = None
        self.assertTrue(permission.has_permission(req_get, None))

        # POST request from regular user
        req_post_reg = self.factory.post('/items/')
        req_post_reg.user = self.regular_user
        self.assertFalse(permission.has_permission(req_post_reg, None))

        # POST request from staff user
        req_post_staff = self.factory.post('/items/')
        req_post_staff.user = self.staff_user
        self.assertTrue(permission.has_permission(req_post_staff, None))

    def test_is_staff_user(self):
        """Only staff users are granted permission."""
        permission = IsStaffUser()

        req_reg = self.factory.get('/admin-api/')
        req_reg.user = self.regular_user
        self.assertFalse(permission.has_permission(req_reg, None))

        req_staff = self.factory.get('/admin-api/')
        req_staff.user = self.staff_user
        self.assertTrue(permission.has_permission(req_staff, None))

    def test_is_owner_or_read_only(self):
        """Only the owner can modify the resource."""
        permission = IsOwnerOrReadOnly()
        owner_obj = DummyOwnerObject(user=self.regular_user)

        # Other user cannot modify
        req_put = self.factory.put('/items/1/')
        req_put.user = self.staff_user
        self.assertFalse(permission.has_object_permission(req_put, None, owner_obj))

        # Owner can modify
        req_put_owner = self.factory.put('/items/1/')
        req_put_owner.user = self.regular_user
        self.assertTrue(permission.has_object_permission(req_put_owner, None, owner_obj))


class TestLoggingSanitizer(SimpleTestCase):
    """Verifies that SensitiveDataFilter masks credentials and sensitive values."""

    def test_bearer_token_redaction(self):
        raw = "Handling request with Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.signature"
        sanitized = sanitize_message(raw)
        self.assertNotIn("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", sanitized)
        self.assertIn("Bearer [REDACTED_TOKEN]", sanitized)

    def test_password_json_redaction(self):
        raw = '{"username": "john_doe", "password": "SuperSecretPassword123!"}'
        sanitized = sanitize_message(raw)
        self.assertNotIn("SuperSecretPassword123!", sanitized)
        self.assertIn('"password": "[REDACTED]"', sanitized)

    def test_credit_card_redaction(self):
        raw = "Processing charge for card: 4111 2222 3333 4444 on gateway"
        sanitized = sanitize_message(raw)
        self.assertNotIn("4111 2222 3333 4444", sanitized)
        self.assertIn("[REDACTED_CARD]", sanitized)

    def test_logging_filter_applied(self):
        logger = logging.getLogger('test.security.logger')
        record = logging.LogRecord(
            name='test.security.logger',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='User login attempt with password="SecretPassword999"',
            args=(),
            exc_info=None,
        )
        flt = SensitiveDataFilter()
        flt.filter(record)
        self.assertNotIn('SecretPassword999', record.msg)
        self.assertIn('[REDACTED]', record.msg)


class TestFileSecurityFoundation(SimpleTestCase):
    """Verifies safe filename generation and magic byte validation for future uploads."""

    def test_sanitize_filename_traversal_removal(self):
        """Ensure path traversal sequences and null bytes are stripped."""
        self.assertEqual(sanitize_filename('../../etc/passwd'), 'passwd')
        self.assertEqual(sanitize_filename('..\\..\\windows\\system32\\cmd.exe'), 'cmd.exe')
        self.assertEqual(sanitize_filename('product\x00_image.jpg'), 'product_image.jpg')

    def test_generate_secure_filename(self):
        """Generated filename must be unique hex with permitted extension."""
        name = generate_secure_filename('summer-dress-v1.JPEG')
        self.assertTrue(name.endswith('.jpeg'))
        self.assertEqual(len(name), 32 + len('.jpeg'))

        # Unsupported or executable extension defaults to safe .jpg
        dangerous_name = generate_secure_filename('exploit.php')
        self.assertTrue(dangerous_name.endswith('.jpg'))

    def test_magic_byte_detection(self):
        """Inspects magic bytes for JPEG, PNG, and WebP."""
        jpeg_bytes = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00'
        png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
        webp_bytes = b'RIFF\x20\x00\x00\x00WEBPVP8 '
        script_bytes = b'#!/bin/bash\necho "exploit"'

        self.assertEqual(detect_mime_from_magic_bytes(jpeg_bytes), 'image/jpeg')
        self.assertEqual(detect_mime_from_magic_bytes(png_bytes), 'image/png')
        self.assertEqual(detect_mime_from_magic_bytes(webp_bytes), 'image/webp')
        self.assertIsNone(detect_mime_from_magic_bytes(script_bytes))

    def test_validate_image_file_rejects_spoofed_content(self):
        """A text/script file masquerading with a .jpg extension must be rejected."""
        fake_file = io.BytesIO(b'<?php phpinfo(); ?>')
        fake_file.name = 'innocent_look.jpg'

        with self.assertRaises(ValidationError) as ctx:
            validate_image_file(fake_file)
        self.assertIn('valid, permitted image format', str(ctx.exception))

    def test_validate_image_file_rejects_oversized_file(self):
        """Files exceeding the maximum limit must be rejected."""
        large_file = io.BytesIO(b'\xff\xd8\xff' + b'0' * (MAX_IMAGE_FILE_SIZE + 100))
        large_file.name = 'huge_image.jpg'

        with self.assertRaises(ValidationError) as ctx:
            validate_image_file(large_file, max_size=MAX_IMAGE_FILE_SIZE)
        self.assertIn('exceeds the maximum allowed limit', str(ctx.exception))

    def test_validate_image_file_accepts_valid_image(self):
        """A genuine JPEG header and valid size passes validation."""
        valid_file = io.BytesIO(b'\xff\xd8\xff\xe0\x00\x10JFIF' + b'\x00' * 50)
        valid_file.name = 'real_product.jpg'

        # Should not raise
        validate_image_file(valid_file)
