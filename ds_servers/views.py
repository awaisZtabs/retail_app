from core.views import CoreListGetQuerySet, CoreRetrieveGetQueryset

from .mixins import GetDSServerMixin


class BaseDSServerListGetQuerySet(
        CoreListGetQuerySet, GetDSServerMixin):
    def _get_list_queryset(self, model=None):
        ds_server = self.validate_kwargs()
        if model:
            return model.objects.filter(ds_server=ds_server.id)
        else:
            return self.model.objects.filter(ds_server=ds_server.id)

    def validate_kwargs(self):
        return self.get_ds_server()


class BaseDSServerRetrieveGetQuerySet(
        CoreRetrieveGetQueryset, GetDSServerMixin):
    def _get_retrieve_queryset(self, model=None):
        ds_server = self.validate_kwargs()
        if model:
            return model.objects.filter(ds_server=ds_server.id)
        else:
            return self.model.objects.filter(ds_server=ds_server.id)

    def validate_kwargs(self):
        return self.get_ds_server()
