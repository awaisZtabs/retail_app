"""
Defines the urls for the views defined in the api.
"""

from django.urls import path

from stream_analytics.api.views import StreamAnalyticsListCreateDestroyView

urlpatterns = [
    path(
        '',
        StreamAnalyticsListCreateDestroyView.as_view(),
        name='stream_analytics_list_create_delete'),
    # path(
    #     '<pk>/',
    #     MeasurementFramesRetrieveUpdateDestroyView.as_view(),
    #     name='frames_retrieve_update_delete'),
]
