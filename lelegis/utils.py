from django.conf import settings


def get_settings_auth_user_model():
    return getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
