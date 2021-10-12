"""
Defines the REST API views for organizations models.
"""


from rest_framework import exceptions

from app_organizations.views import (BaseOrganizationListGetQuerySet,
                                     BaseOrganizationRetrieveGetQuerySet)
from core.utils import field_not_found_error
from outlets.mixins import GetOutletMixin
from outlets.models import Outlet


class BaseOutletListGetQuerySet(
        BaseOrganizationListGetQuerySet, GetOutletMixin):
    def _get_list_queryset(self, model=None):
        outlet = self.validate_kwargs()
        if model:
            return model.objects.filter(outlet=outlet.id)
        else:
            return self.model.objects.filter(outlet=outlet.id)

    def _get_list_queryset_user(self):
        outlet = self.validate_kwargs()

        # if its a normal user make sure he exists within the outlet
        if not outlet.users.filter(id=self.request.user).exists():
            raise exceptions.ValidationError({
                "outlet": field_not_found_error()
            })

        return self._get_list_queryset()

    def validate_kwargs(self):
        organization = super().validate_kwargs()
        outlet = self.get_outlet()
        if outlet.organization.id != organization.id:
            raise exceptions.ValidationError({
                "outlet": field_not_found_error()
            })
        return outlet


class BaseOutletRetrieveGetQuerySet(
        BaseOrganizationRetrieveGetQuerySet, GetOutletMixin):

    def _get_retrieve_queryset(self, model=None):
        outlet = self.validate_kwargs()

        if model:
            return model.objects.filter(outlet=outlet.id)
        else:
            return self.model.objects.filter(outlet=outlet.id)

    def _get_retrieve_queryset_user(self):
        outlet = self.validate_kwargs()

        # if its a normal user make sure he exists within the outlet
        if not outlet.users.filter(id=self.request.user).exists():
            raise exceptions.ValidationError({
                "outlet": field_not_found_error()
            })

        return self._get_retrieve_queryset()

    def validate_kwargs(self):
        organization = super().validate_kwargs()
        outlet = self.get_outlet()
        if outlet.organization.id != organization.id:
            raise exceptions.ValidationError({
                "outlet": field_not_found_error()
            })
        return outlet
