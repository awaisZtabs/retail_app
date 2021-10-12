"""
Defines the urls for the views defined in the Server api.
"""
from django.urls import path

from ds_analytics.api.views import (PLAConfigsListCreateDestroyView,
                                    PLAConfigsRetrieveUpdateDestroyView)

camera_analytics_urlpatterns = [
    path(
        'pla/config/',
        PLAConfigsListCreateDestroyView.as_view(),
        name='pla_configs_list_create_delete'),
    path(
        'pla/config/<pk>/',
        PLAConfigsRetrieveUpdateDestroyView.as_view(),
        name='pla_configs_retrieve_update_delete'),
]
