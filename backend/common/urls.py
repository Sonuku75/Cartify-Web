"""URL patterns for common utilities and health endpoint."""
from django.urls import path
from .views import HealthCheckView

urlpatterns = [
    path('', HealthCheckView.as_view(), name='api-health'),
]
