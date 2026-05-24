from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return None  # No token = anonymous user, let permissions decide

        token_str = auth_header.split(' ')[1]

        try:
            from rest_framework_simplejwt.tokens import AccessToken
            from accounts.models import User
            token = AccessToken(token_str)
            user = User.objects.get(pk=token['user_id'])
            return (user, token)
        except Exception as e:
            raise AuthenticationFailed('Invalid or expired token.')

    def authenticate_header(self, request):
        return 'Bearer'