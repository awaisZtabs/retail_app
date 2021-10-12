"""
Defines the REST api views for deepstream servers.
"""

from core import views
from core.permissions import AppDjangoModelPermissions
from ds_servers.api.serializers import (AddBlockSerializer,
                                        AddCameraSerializer,
                                        DSServerConfigCreateSerializer,
                                        DSServerConfigRetrieveSerializer,
                                        DSServerCreateSerializer,
                                        DSServerListSerializer,
                                        DSServerRetrieveSerializer,
                                        DSServerUpdateSerializer,
                                        RemoveBlockSerializer,
                                        RemoveCameraSerializer)
from ds_servers.models import DSServer, DSServerConfig
from ds_servers.views import (BaseDSServerListGetQuerySet,
                              BaseDSServerRetrieveGetQuerySet)


class DSServersListCreateDestroyView(
        views.CoreListAPIView,
        views.CoreCreateAPIView,
        views.CoreListDestroyAPIView):

    """
    Defines the DSServers list-create-destroy view.
    """

    queryset = DSServer.objects.none()
    permission_classes = (AppDjangoModelPermissions,)
    ordering_fields = ['id', 'ip_addr']
    filterset_fields = {
        'ip_addr': ['exact', 'icontains']
    }
    order_by = 'id'
    list_serializer = DSServerListSerializer
    create_serializer = DSServerCreateSerializer


class DSServersRetrieveUpdateDestroyView(
        views.CoreRetrieveAPIView,
        views.CoreUpdateAPIView,
        views.CoreDestroyAPIView):
    """
    Defines the DSServers list-create-destroy view.
    """

    queryset = DSServer.objects.none()  # Added for model permissions
    permission_classes = (AppDjangoModelPermissions,)
    retrieve_serializer = DSServerRetrieveSerializer
    update_serializer = DSServerUpdateSerializer


class DSServerConfigsListCreateDestroyView(
        views.CoreCreateAPIView,
        BaseDSServerListGetQuerySet):
    """
    Defines the DSServers list-create-destroy view. Only create is allowed as
    this is a one-to-one field.
    """

    queryset = DSServerConfig.objects.none()
    permission_classes = (AppDjangoModelPermissions,)
    create_serializer = DSServerConfigCreateSerializer


class DSServerConfigsRetrieveUpdateDestroyView(
        views.CoreRetrieveAPIView,
        views.CoreDestroyAPIView,
        BaseDSServerRetrieveGetQuerySet):
    """
    Defines the DSServers list-create-destroy view.
    """

    queryset = DSServerConfig.objects.none()  # Added for model permissions
    permission_classes = (AppDjangoModelPermissions,)
    retrieve_serializer = DSServerConfigRetrieveSerializer


class DSServerConfigsAddRemoveBase(
        views.CoreUpdateAPIView,
        BaseDSServerRetrieveGetQuerySet):
    """
    Defines base view for add/remove cameras/blocks to the server config
    """

    queryset = DSServerConfig.objects.none()  # Added for model permissions
    permission_classes = (AppDjangoModelPermissions,)


class AddCameraView(DSServerConfigsAddRemoveBase):
    """
    Defines the view for adding cameras to the server config
    """
    update_serializer = AddCameraSerializer


class RemoveCameraView(DSServerConfigsAddRemoveBase):
    """
    Defines the view for removing cameras to the server config
    """
    update_serializer = RemoveCameraSerializer


class AddBlockView(DSServerConfigsAddRemoveBase):
    """
    Defines the view for adding blocks to the server config
    """
    update_serializer = AddBlockSerializer


class RemoveBlockView(DSServerConfigsAddRemoveBase):
    """
    Defines the view for removing blocks to the server config
    """
    update_serializer = RemoveBlockSerializer
