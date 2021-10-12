"""
Defines the model of deepstream servers
"""
import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils import timezone
from safedelete.config import HARD_DELETE, SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


class DSLogEntry(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE

    """Message stored in the log entry"""
    message = models.CharField(max_length=500, blank=True, default="")

    """Time at which the log message was received."""
    received_at = models.DateTimeField(default=timezone.now)

    """Server with which the log info is associated with."""
    ds_server = models.ForeignKey(
        'ds_servers.DSServer',
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        """
        String serializer of the model
        """
        if self.ds_server:
            return "{}: [{}] {}".format(
                self.received_at, self.ds_server.id, self.message)
        else:
            return "{}: {}".format(
                self.received_at, self.message)


class DSDiagnostics(SafeDeleteModel):
    """
    A model of a deepstream server diagnostics information
    """
    _safedelete_policy = HARD_DELETE

    """Server with which the diagnostics info is associated with."""
    ds_server = models.ForeignKey(
        'ds_servers.DSServer',
        on_delete=models.CASCADE,
    )

    """CPU Utilization of the server."""
    cpu_utilization = \
        models.PositiveIntegerField(
            validators=[MaxValueValidator(100), ])

    """GPU Utilization of the server."""
    gpu_utilization = \
        models.PositiveIntegerField(
            validators=[MaxValueValidator(100), ])

    """Memory usage of the server."""
    memory_usage = \
        models.PositiveIntegerField(
            validators=[MaxValueValidator(100), ])

    """GPU Memory of the server."""
    gpu_memory_usage = \
        models.PositiveIntegerField(
            validators=[MaxValueValidator(100), ])

    """Temperature of the server."""
    temperature = models.IntegerField()

    """Time at which the diagnostics were received."""
    received_at = models.DateTimeField(null=True, blank=True)


class DSServer(SafeDeleteModel):
    """
    A model of a deepstream server associated with a block.
    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    ONLINE = 'online'
    IDLE = 'online-idle'
    IN_ERROR = 'online-in-error'
    STREAMING = 'online-streaming'
    OFFLINE = 'offline'
    STATUS = (
        (ONLINE, 'On-line'),
        (IDLE, 'On-line Idle'),
        (IN_ERROR, 'On-line In Error'),
        (STREAMING, 'On-line Streaming'),
        (OFFLINE, 'Off-line'),
    )

    """Ip address of the server."""
    ip_addr = models.CharField(max_length=120)

    """Status of the server whether it is currently online or offline"""
    status = models.CharField(
        max_length=20, choices=STATUS,
        default=OFFLINE
    )

    """Time field that is updated whenever the associated server is
        disconnected"""
    last_echo_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Don't allow non-unique ip addresses."""
        constraints = [
            UniqueConstraint(fields=["ip_addr"], condition=Q(
                deleted__isnull=True), name='unique_ds_if_not_deleted')
        ]


class DSServerConfig(SafeDeleteModel):
    """
    A model of a deepstream server config that defines its behavior
    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    """Server with which this config is associated."""
    ds_server = models.OneToOneField(
        "ds_servers.DSServer",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    """Map of all the cameras attached to this server for analytics
        generation."""
    cameras = models.ManyToManyField("cameras.Camera", blank=True)

    """Map of all the blocks attached to this server for analytics
        generation."""
    blocks = models.ManyToManyField("locations.Block", blank=True)
