
"""
Defines the REST API views for measurement frames models.
"""


from app_organizations.permissions import OrganizationDjangoModelPermissions
from core import views
from stream_analytics.api.serializers import (StreamAnalyticCreateSerializer,
                                              StreamAnalyticListSerializer)
from stream_analytics.models import StreamAnalytic


class StreamAnalyticsListCreateDestroyView(
    views.CoreListAPIView,
    views.CoreCreateAPIView,
    views.CoreListDestroyAPIView,
):

    """
    Defines the   StreamAnalytics list-create-destroy view.
    """

    queryset = StreamAnalytic.objects.none()
    permission_classes = (OrganizationDjangoModelPermissions,)
    ordering_fields = ['id', 'frame_id']
    filterset_fields = {
        'frame_id': ['exact', 'icontains'],
    }
    order_by = 'frame_id'
    list_serializer = StreamAnalyticListSerializer
    create_serializer = StreamAnalyticCreateSerializer


# class MeasurementFramesRetrieveUpdateDestroyView(
#         views.CoreRetrieveAPIView,
#         views.CoreUpdateAPIView,
#         views.CoreDestroyAPIView,
#         BaseBlockRetrieveGetQuerySet):
#     """
#     Defines the MeasurementFrames list-create-destroy view.
#     """

#     queryset = MeasurementFrame.objects.none()  # Added for model permissions
#     permission_classes = (OrganizationDjangoModelPermissions,)
#     retrieve_serializer = MeasurementFrameRetrieveSerializer
#     update_serializer = MeasurementFrameUpdateSerializer
