"""
Defines the models of this application.
"""
from django.db import models
from django.db.models.constraints import Q, UniqueConstraint
from safedelete.models import SafeDeleteModel

# Create your models here.
# pylint: disable=pointless-string-statement


class StreamAnalytic(SafeDeleteModel):
    """
    A model for stream analytics associated with camera.
    """

    """Frame with witch this stream is captured."""
    frame_id = models.FloatField(blank=False)

    """Tracking id of stream"""
    tracking_id = models.FloatField(blank=False)

    """coordinates of the frame."""
    x_coordinate = models.FloatField(blank=False)
    y_coordinate = models.FloatField(blank=False)

    """Time during which this frame is captured."""
    time = models.DateTimeField(blank=False)

    """Camera with which this frame is associated."""
    camera = models.ForeignKey(
        'cameras.Camera',
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        proxy = False
        verbose_name = ("Stream Analytic")
        verbose_name_plural = ("Stream Analytics")

    def __str__(self):
        """
        String serializer of the model
        """
        return "Analytic={}, {}, {},{},{}".format(
            self.frame_id,
            self.tracking_id,
            self.x_coordinate,
            self.y_coordinate,
            str(self.camera),)
