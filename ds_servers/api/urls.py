"""
Defines the urls for the views defined in the Server api.
"""
from django.urls import path
from django.urls.conf import include

from ds_servers.api.views import (AddBlockView, AddCameraView,
                                  DSServerConfigsListCreateDestroyView,
                                  DSServerConfigsRetrieveUpdateDestroyView,
                                  DSServersListCreateDestroyView,
                                  DSServersRetrieveUpdateDestroyView,
                                  RemoveBlockView, RemoveCameraView)

ds_serverpk_urlpatterns = [
    path(
        'config/', include([
            path(
                '',
                DSServerConfigsListCreateDestroyView.as_view(),
                name='ds_server_config_list_create_delete'),
            path(
                '<pk>/',
                DSServerConfigsRetrieveUpdateDestroyView.as_view(),
                name='ds_server_config_retrieve_update_destroy'),
            path(
                '<pk>/cameras/add',
                AddCameraView.as_view(),
                name='ds_server_config_add_camera'),
            path(
                '<pk>/cameras/remove',
                RemoveCameraView.as_view(),
                name='ds_server_config_remove_camera'),
            path(
                '<pk>/blocks/add',
                AddBlockView.as_view(),
                name='ds_server_config_add_block'),
            path(
                '<pk>/blocks/remove',
                RemoveBlockView.as_view(),
                name='ds_server_config_remove_block'),
        ])),
]

urlpatterns = [
    path(
        '',
        DSServersListCreateDestroyView.as_view(),
        name='ds_servers_list_create_delete'),
    path(
        '<pk>/',
        DSServersRetrieveUpdateDestroyView.as_view(),
        name='ds_servers_retrieve_update_delete'),
    path('<ds_server>/', include(ds_serverpk_urlpatterns))
]
