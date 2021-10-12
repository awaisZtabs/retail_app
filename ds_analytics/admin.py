"""
Registers the models to the admin interface.
"""

from django.contrib import admin

from core.admin import BaseAdmin, list_display_fn, list_filter_fn

from .models import BlockAnalyticsConfig, CameraAnalyticsConfig, PLAConfig


class CameraAnalyticsConfigAdmin(BaseAdmin):
    """
    Defines custom admin interface view
    """
    list_display = list_display_fn(())
    list_filter = list_filter_fn(())


class BlockAnalyticsConfigAdmin(BaseAdmin):
    """
    Defines custom admin interface view
    """
    list_display = list_display_fn(())
    list_filter = list_filter_fn(())


class PLAConfigAdmin(BaseAdmin):
    """
    Defines custom admin interface view
    """
    list_display = list_display_fn(())
    list_filter = list_filter_fn(())


admin.site.register(PLAConfig, PLAConfigAdmin)
