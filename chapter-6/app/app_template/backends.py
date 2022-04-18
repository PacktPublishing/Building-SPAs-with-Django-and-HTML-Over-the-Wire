from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend


class EmailBackend(BaseBackend):
    """
    Email authentication backend
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on email address as the user name.
        """
        if "@" in username:
            kwargs = {"email": username}
        else:
            kwargs = {"username": username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# Future re-implementation with token for auto login
class TokenBackend(BaseBackend):
    def authenticate(self, request, token=None):
        pass
