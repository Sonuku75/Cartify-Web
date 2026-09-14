"""Root URL configuration for Cartify backend."""
from django.urls import path, include

urlpatterns = [
    # System health check endpoint
    path('api/health/', include('common.urls')),

    # Version 1 API namespace for future business domain routes
    path('api/v1/', include('config.api_v1_urls')),
]
