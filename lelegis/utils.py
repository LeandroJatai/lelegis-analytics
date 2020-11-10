from django.conf import settings

from django.template.loaders.filesystem import Loader


def get_settings_auth_user_model():
    return getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class LelegisLoader(Loader):

    def get_dirs(self):
        return self.dirs if self.dirs is not None else self.engine.dirs
