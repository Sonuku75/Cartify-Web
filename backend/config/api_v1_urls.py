"""Version 1 API URL routing for Cartify."""
from django.urls import path, re_path
from common.views import APIVersionView, custom_404_view
from common.auth_views import (
    CartifyTokenObtainPairView,
    CartifyTokenRefreshView,
    CartifyTokenVerifyView,
)

app_name = 'api_v1'

urlpatterns = [
    # Version 1 API Root & Status
    path('', APIVersionView.as_view(), name='api-v1-root'),

    # Authentication Infrastructure (JWT)
    path('auth/token/', CartifyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', CartifyTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', CartifyTokenVerifyView.as_view(), name='token_verify'),

    # Business domain routes will be mounted here in upcoming modules:
    # path('users/', include('apps.users.urls')),
    # path('products/', include('apps.products.urls')),
    # path('categories/', include('apps.categories.urls')),
    # path('brands/', include('apps.brands.urls')),
    # path('inventory/', include('apps.inventory.urls')),
    # path('cart/', include('apps.cart.urls')),
    # path('orders/', include('apps.orders.urls')),

    # Fallback for unmapped /api/v1/ routes to return standardized JSON error
    re_path(r'^.*$', custom_404_view, name='api-v1-not-found'),
]
