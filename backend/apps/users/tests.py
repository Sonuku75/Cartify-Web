"""Unit and integration tests for Cartify custom User model and role foundation."""
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.users.models import UserRole

User = get_user_model()


class CustomUserModelTests(TestCase):
    """Test suite for Cartify custom User model and UserManager."""

    def test_create_user_successful(self):
        """User can be created with valid email and password."""
        user = User.objects.create_user(
            email='customer@cartify.com',
            password='SecurePassword123!',
            first_name='Jane',
            last_name='Doe',
            phone='+1234567890',
        )

        self.assertIsInstance(user.id, uuid.UUID)
        self.assertEqual(user.email, 'customer@cartify.com')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.phone, '+1234567890')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.role, UserRole.CUSTOMER)
        self.assertTrue(user.is_customer)
        self.assertFalse(user.is_seller)
        self.assertFalse(user.is_admin_role)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_create_user_email_normalization(self):
        """Email domain must be normalized to lowercase by UserManager."""
        user = User.objects.create_user(
            email='TestUser@EXAMPLE.COM',
            password='Password123!',
        )
        self.assertEqual(user.email, 'TestUser@example.com')

    def test_create_user_without_email_raises_error(self):
        """Creating a user without an email raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            User.objects.create_user(email='', password='Password123!')
        self.assertIn('Email field must be set', str(ctx.exception))

        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='Password123!')

    def test_email_must_be_unique(self):
        """Duplicate emails must trigger database IntegrityError."""
        User.objects.create_user(
            email='duplicate@cartify.com',
            password='Password123!',
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='duplicate@cartify.com',
                password='AnotherPassword123!',
            )

    def test_password_is_hashed_and_not_stored_plaintext(self):
        """Password must be securely hashed and check_password must verify it."""
        raw_password = 'SecretPassPhrase2026!'
        user = User.objects.create_user(
            email='hashcheck@cartify.com',
            password=raw_password,
        )

        self.assertNotEqual(user.password, raw_password)
        self.assertTrue(user.password.startswith('pbkdf2_sha256$') or '$' in user.password)
        self.assertTrue(user.check_password(raw_password))
        self.assertFalse(user.check_password('WrongPassPhrase'))

    def test_default_role_is_customer(self):
        """When not specified, the default role must be CUSTOMER."""
        user = User.objects.create_user(
            email='defaultrole@cartify.com',
            password='Password123!',
        )
        self.assertEqual(user.role, UserRole.CUSTOMER)

    def test_create_user_with_explicit_roles(self):
        """Users can be created with SELLER or ADMIN roles."""
        seller = User.objects.create_user(
            email='seller@cartify.com',
            password='Password123!',
            role=UserRole.SELLER,
        )
        self.assertEqual(seller.role, UserRole.SELLER)
        self.assertTrue(seller.is_seller)
        self.assertFalse(seller.is_customer)

        admin = User.objects.create_user(
            email='admin@cartify.com',
            password='Password123!',
            role=UserRole.ADMIN,
        )
        self.assertEqual(admin.role, UserRole.ADMIN)
        self.assertTrue(admin.is_admin_role)
        # Admin role automatically grants staff status
        self.assertTrue(admin.is_staff)

    def test_create_superuser_successful(self):
        """Superuser creation sets all elevated privileges and SUPERADMIN role."""
        superuser = User.objects.create_superuser(
            email='super@cartify.com',
            password='SuperSecretPassword123!',
            first_name='Super',
            last_name='Admin',
        )

        self.assertEqual(superuser.email, 'super@cartify.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_verified)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.role, UserRole.SUPERADMIN)
        self.assertTrue(superuser.is_admin_role)

    def test_create_superuser_invalid_staff_flag(self):
        """Attempting to create superuser with is_staff=False raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            User.objects.create_superuser(
                email='badsuper1@cartify.com',
                password='Password123!',
                is_staff=False,
            )
        self.assertIn('Superuser must have is_staff=True', str(ctx.exception))

    def test_create_superuser_invalid_superuser_flag(self):
        """Attempting to create superuser with is_superuser=False raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            User.objects.create_superuser(
                email='badsuper2@cartify.com',
                password='Password123!',
                is_superuser=False,
            )
        self.assertIn('Superuser must have is_superuser=True', str(ctx.exception))

    def test_user_string_representation(self):
        """String representation of user must return email."""
        user = User.objects.create_user(
            email='strrepr@cartify.com',
            password='Password123!',
        )
        self.assertEqual(str(user), 'strrepr@cartify.com')

    def test_get_full_name_and_get_short_name(self):
        """Verify get_full_name and get_short_name behaviors."""
        user = User.objects.create_user(
            email='names@cartify.com',
            password='Password123!',
            first_name='Alex',
            last_name='Morgan',
        )
        self.assertEqual(user.get_full_name(), 'Alex Morgan')
        self.assertEqual(user.get_short_name(), 'Alex')

        # Fallback when names are blank
        nameless = User.objects.create_user(
            email='nameless@cartify.com',
            password='Password123!',
        )
        self.assertEqual(nameless.get_full_name(), 'nameless@cartify.com')
        self.assertEqual(nameless.get_short_name(), 'nameless@cartify.com')

    def test_role_choices_integrity(self):
        """Verify that UserRole enum contains expected fashion e-commerce roles."""
        expected_roles = {'CUSTOMER', 'SELLER', 'ADMIN', 'SUPERADMIN'}
        actual_roles = {choice[0] for choice in UserRole.choices}
        self.assertEqual(expected_roles, actual_roles)
