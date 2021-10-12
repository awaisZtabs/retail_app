"""
Defines the mixins related to the api.
"""
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from .models import DSServer


class GetDSServerMixin:
    """Mixin used like a SingleObjectMixin to fetch an ds_server"""

    @cached_property
    def ds_server(self):
        return get_object_or_404(
            DSServer, pk=self.kwargs.get("ds_server", None))

    def get_ds_server(self):
        return self.ds_server
