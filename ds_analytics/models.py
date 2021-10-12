"""
Defines the model of deepstream servers
"""
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q, UniqueConstraint
from safedelete.config import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


class DSAnalyticsConfig(SafeDeleteModel):
    """
    A model of a deepstream analytics configuration.
    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        abstract = True


class BlockAnalyticsConfig(DSAnalyticsConfig):
    """
    A model of a deepstream analytics configuration associated with a block.
    """

    """Block with which this config is associated with."""
    block = models.ForeignKey(
        "locations.Block",
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class CameraAnalyticsConfig(DSAnalyticsConfig):
    """
    A model of a deepstream analytics configuration associated with a camera.
    """

    """Camera with which this config is associated with."""
    camera = models.OneToOneField(
        "cameras.Camera",
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class PLAConfig(CameraAnalyticsConfig):
    """
    Short for Person Location Analytics

    A model of a deepstream analytics configuration that is required for
    generating person location on the map.

    This configuration provides the mapping of points between the image plane
    of the associated camera and the ground plane as computed with respect to
    the associated measurement frame.
    """

    """ Ground frame with which the measurements are taken from """
    ground_frame = models.ForeignKey(
        'measurement_frames.MeasurementFrame',
        on_delete=models.PROTECT
    )

    """ Coordinates of the reference points p0, p1, p2, p3 in ground plane
        wrt to the measurement frame. Data is added as
        [p0.x, p0.y, p1.x, p1.y, p2.x, p2.y, p3.x, p3.y]"""
    point_coords_in_ground_frame = ArrayField(
        models.FloatField(), size=8, null=True)

    """ Coordinates of the all the reference points in image frame Data
        is added as  [p0.x, p0.y, p1.x, p1.y, p2.x, p2.y, p3.x, p3.y]"""
    point_coords_in_image = ArrayField(
        models.IntegerField(), size=8, null=True)
