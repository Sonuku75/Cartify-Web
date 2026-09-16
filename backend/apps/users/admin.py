"""Admin registration for Users domain."""
from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from .models import User, UserRole


class CartifyUserCreationForm(forms.ModelForm):
    """Custom form for creating a user in Django admin."""

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password_confirmation = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_('Enter the same password as before, for verification.'),
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', _("Passwords don't match."))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CartifyUserChangeForm(forms.ModelForm):
    """Custom form for updating a user in Django admin."""

    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=_(
            'Raw passwords are not stored. A user can change their password '
            'using the password reset endpoint or Django admin password reset.'
        ),
    )

    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for Cartify User model."""

    form = CartifyUserChangeForm
    add_form = CartifyUserCreationForm

    list_display = (
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_verified',
        'is_staff',
        'created_at',
    )
    list_filter = ('role', 'is_active', 'is_verified', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (
            _('Permissions & Role'),
            {
                'fields': (
                    'role',
                    'is_active',
                    'is_verified',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'role',
                    'password',
                    'password_confirmation',
                ),
            },
        ),
    )
