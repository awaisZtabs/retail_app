"""
Defines the REST api views for deepstream servers.
"""

from core import views
from core.permissions import AppDjangoModelPermissions
from ds_analytics.api.serializers import (PLAConfigCreateSerializer,
                                          PLAConfigListSerializer,
                                          PLAConfigRetrieveSerializer,
                                          PLAConfigUpdateSerializer)
from ds_analytics.models import PLAConfig


class PLAConfigsListCreateDestroyView(
        views.CoreListAPIView,
        views.CoreCreateAPIView,
        views.CoreListDestroyAPIView):

    """
    Defines the PLAConfigs list-create-destroy view.
    """

    queryset = PLAConfig.objects.none()
    permission_classes = (AppDjangoModelPermissions,)
    ordering_fields = ['id']
    order_by = 'id'
    list_serializer = PLAConfigListSerializer
    create_serializer = PLAConfigCreateSerializer


class PLAConfigsRetrieveUpdateDestroyView(
        views.CoreRetrieveAPIView,
        views.CoreUpdateAPIView,
        views.CoreDestroyAPIView):
    """
    Defines the PLAConfigs list-create-destroy view.
    """

    queryset = PLAConfig.objects.none()  # Added for model permissions
    permission_classes = (AppDjangoModelPermissions,)
    retrieve_serializer = PLAConfigRetrieveSerializer
    update_serializer = PLAConfigUpdateSerializer
