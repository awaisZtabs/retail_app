"""
Defines the permissions handleer backend for Organization User authentication
within an organization
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission

USER_MODEL = get_user_model()


class UserAuthBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def _get_group_permissions(self, user_obj):
        user_groups_field = USER_MODEL._meta.get_field('groups')
        user_groups_query = \
            'user_group__%s' % user_groups_field.related_query_name()
        return Permission.objects.filter(**{user_groups_query: user_obj})
