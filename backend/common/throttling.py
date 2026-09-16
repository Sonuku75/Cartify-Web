"""
Security throttling classes for Cartify REST APIs.
Protects endpoints against brute-force attacks, credential stuffing, and DoS.
"""
from rest_framework.throttling import ScopedRateThrottle, SimpleRateThrottle


class AuthBurstRateThrottle(SimpleRateThrottle):
    """
    Burst rate limiter for authentication endpoints.
    Protects against automated credential-stuffing and rapid brute-force attacks.
    """
    scope = 'auth_burst'

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }


class AuthSustainedRateThrottle(SimpleRateThrottle):
    """
    Sustained rate limiter for authentication endpoints.
    Limits aggregate attempts over longer evaluation windows.
    """
    scope = 'auth_sustained'

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }
