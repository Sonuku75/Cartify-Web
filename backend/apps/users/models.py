"""Models for Users domain.

Defines the Cartify custom User model and role hierarchy.
"""
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    """Supported platform roles for Cartify users."""

    CUSTOMER = 'CUSTOMER', _('Customer')
    SELLER = 'SELLER', _('Seller')
    ADMIN = 'ADMIN', _('Admin')
    SUPERADMIN = 'SUPERADMIN', _('Superadmin')


class CartifyUserManager(BaseUserManager):
    """Custom manager for Cartify User model with email as primary identifier."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular User with an email and password."""
        if not email:
            raise ValueError(_('The Email field must be set.'))

        email = self.normalize_email(email)
        extra_fields.setdefault('role', UserRole.CUSTOMER)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a Superuser with an email and password."""
        extra_fields.setdefault('role', UserRole.SUPERADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model for Cartify fashion e-commerce platform.

    Uses UUID as primary key and normalized email as unique login identifier.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_('Unique identifier (UUID v4) for this user.'),
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=255,
        db_index=True,
        help_text=_('Primary email address used for authentication and communications.'),
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True,
        default='',
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
        default='',
    )
    phone = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        default='',
        help_text=_('Contact phone number.'),
    )
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
        db_index=True,
        help_text=_('Role assigned to the user within Cartify platform.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_('Designates whether user email has been verified.'),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        help_text=_('Date and time when the account was registered.'),
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True,
        help_text=_('Date and time when the account was last modified.'),
    )

    objects = CartifyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'cartify_users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email'], name='user_email_idx'),
            models.Index(fields=['role'], name='user_role_idx'),
            models.Index(fields=['created_at'], name='user_created_idx'),
        ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """Ensure administrative roles automatically have staff access."""
        if self.role in (UserRole.ADMIN, UserRole.SUPERADMIN) or self.is_superuser:
            self.is_staff = True
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Return the user's full name, falling back to email."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.email

    def get_short_name(self):
        """Return the user's first name, falling back to email."""
        return self.first_name if self.first_name else self.email

    @property
    def is_customer(self):
        """Check if user role is CUSTOMER."""
        return self.role == UserRole.CUSTOMER

    @property
    def is_seller(self):
        """Check if user role is SELLER."""
        return self.role == UserRole.SELLER

    @property
    def is_admin_role(self):
        """Check if user role is ADMIN or SUPERADMIN."""
        return self.role in (UserRole.ADMIN, UserRole.SUPERADMIN)
