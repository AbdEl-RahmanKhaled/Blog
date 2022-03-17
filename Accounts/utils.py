from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.backends import ModelBackend
from .models import Account


class EmailVerificationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{timestamp}{user.is_verified_email}'


token_generator = EmailVerificationToken()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    This is a ModelBacked that allows authentication with either a username or an email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(Account().EMAIL_FIELD)
            if username is not None:
                kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        if username is None or password is None:
            return
        try:
            user = Account.objects.get(**kwargs)
        except Account.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            Account().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
