"""
Registers the models to the admin interface.
"""

from django.contrib import admin

from core.admin import BaseAdmin, list_display_fn, list_filter_fn

from .models import StreamAnalytic


class StreamAnalyticAdmin(BaseAdmin):
    """
    Defines custom admin interface view
    """
    list_display = list_display_fn(())
    list_filter = list_filter_fn(())


admin.site.register(StreamAnalytic,   StreamAnalyticAdmin)
