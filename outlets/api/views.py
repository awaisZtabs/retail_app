"""
Defines the REST API views for organizations models.
"""


from app_organizations.permissions import OrganizationDjangoModelPermissions
from app_organizations.views import (BaseOrganizationListGetQuerySet,
                                     BaseOrganizationRetrieveGetQuerySet)
from core import views
from outlets.api.serializers import (OutletCreateSerializer,
                                     OutletListSerializer,
                                     OutletRetrieveSerializer,
                                     OutletUpdateSerializer,
                                     OutletUserCreateSerializer,
                                     OutletUserListSerializer,
                                     OutletUserRetrieveSerializer,
                                     OutletUserUpdateSerializer)
from outlets.models import Outlet, OutletUser
from outlets.views import (BaseOutletListGetQuerySet,
                           BaseOutletRetrieveGetQuerySet)


class OutletsListCreateDestroyView(
    views.CoreListAPIView,
    views.CoreCreateAPIView,
    views.CoreListDestroyAPIView, BaseOrganizationListGetQuerySet
):

    """
    Defines the organizations list-create-destroy view.
    """

    queryset = Outlet.objects.none()
    permission_classes = (OrganizationDjangoModelPermissions,)
    ordering_fields = ['id', 'name']
    order_by = 'name'
    filterset_fields = {
        'name': ['exact', 'icontains'],
    }
    list_serializer = OutletListSerializer
    create_serializer = OutletCreateSerializer

    def _get_list_queryset_user(self):
        """
        Returns the list of all outlets this user belongs to
        """
        return super()._get_list_queryset_user().filter(
            users=self.request.user)


class OutletsRetrieveUpdateDestroyView(
        views.CoreRetrieveAPIView,
        views.CoreUpdateAPIView,
        views.CoreDestroyAPIView, BaseOrganizationRetrieveGetQuerySet):
    """
    Defines the organizations retrieve-update-destroy view.
    """

    queryset = Outlet.objects.none()  # Added for model permissions
    permission_classes = (OrganizationDjangoModelPermissions,)
    retrieve_serializer = OutletRetrieveSerializer
    update_serializer = OutletUpdateSerializer

    def _get_retrieve_queryset_user(self):
        """
        Returns the list of all outlets this user belongs to
        """
        return super()._get_retrieve_queryset_user().filter(
            users=self.request.user)


class OutletUsersListCreateDestroyView(
        views.CoreListAPIView,
        views.CoreCreateAPIView,
        views.CoreListDestroyAPIView, BaseOutletListGetQuerySet):

    """
    Defines the organization users list-create-destroy view.
    """

    queryset = OutletUser.objects.none()
    permission_classes = (OrganizationDjangoModelPermissions,)
    # list destroy is not allowed
    ordering_fields = ['id']
    order_by = 'id'
    filterset_fields = {
        'id': ['exact', 'icontains'],
    }
    list_serializer = OutletUserListSerializer
    create_serializer = OutletUserCreateSerializer


class OutletUsersRetrieveUpdateDestroyView(
        views.CoreRetrieveAPIView,
        views.CoreUpdateAPIView,
        views.CoreDestroyAPIView,
        BaseOutletRetrieveGetQuerySet):
    """
    Defines the organization users retrieve-update-destroy view.
    """

    queryset = OutletUser.objects.none()  # Added for model permissions
    permission_classes = (OrganizationDjangoModelPermissions,)
    retrieve_serializer = OutletUserRetrieveSerializer
    update_serializer = OutletUserUpdateSerializer
