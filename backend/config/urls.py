"""Root URL configuration for Cartify backend."""
from django.urls import path, include

urlpatterns = [
    # Lightweight system health check endpoint for infrastructure
    path('api/health/', include('common.urls')),

    # Version 1 API namespace for all client platforms (Web, iOS, Android)
    path('api/v1/', include('config.api_v1_urls')),
]

# Standard JSON error handlers for unmatched routes and server errors
handler404 = 'common.views.custom_404_view'
handler500 = 'common.views.custom_500_view'
