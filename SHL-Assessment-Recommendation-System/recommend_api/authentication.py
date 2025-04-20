from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-KEY')

        # Optional: allow skipping auth in DEBUG mode for local dev
        if settings.DEBUG and not api_key:
            return (None, None)

        if not api_key or api_key != getattr(settings, 'API_KEY', None):
            raise AuthenticationFailed('Invalid or missing API Key')

        return (None, None)  # No user object, just says “authenticated”
