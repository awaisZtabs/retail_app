"""
Defines the urls for the views defined in the cameras api.
"""
from django.urls import path
from django.urls.conf import include

from cameras.api.views import (CamerasListCreateDestroyView,
                               CamerasRetrieveUpdateDestroyView)
from ds_analytics.api.urls import camera_analytics_urlpatterns

urlpatterns = [
    path(
        '',
        CamerasListCreateDestroyView.as_view(),
        name='cameras_list_create_delete'),
    path(
        '<pk>/',
        CamerasRetrieveUpdateDestroyView.as_view(),
        name='cameras_retrieve_update_delete'),
    path('<camera>/', include([
        path('analytics/', include(camera_analytics_urlpatterns))
    ]))
]
