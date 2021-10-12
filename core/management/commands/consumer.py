from importlib import import_module
from json import loads

from django.apps import apps
from django.core.management import BaseCommand, call_command
from django.utils.module_loading import module_has_submodule
from kafka import KafkaConsumer

from stream_analytics.models import StreamAnalytic


class Command(BaseCommand):
    """
    A command to setup common initialization parameters used across our
    applications
    """

    def handle(self, *args, **options):
        """
        Runs the command
        """
        consumer = KafkaConsumer(
            'quickstart-events',
            bootstrap_servers=['10.7.213.152:9092'],
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='none',
            value_deserializer=lambda x: loads(x.decode('utf-8')))
        for message in consumer:
            frame_id = message.value['analyticsModule']['Frame_ID']
            tracking_id = message.value['analyticsModule']['Tracking-ID']
            x_coordinate = message.value['analyticsModule']['X_Coordinate']
            y_coordinate = message.value['analyticsModule']['Y_Coordinate']
            camera_id = message.value['CameraID']
            time = message.value['@timestamp']

            analytics = StreamAnalytic.objects.create(
                frame_id=frame_id, tracking_id=tracking_id, x_coordinate=x_coordinate, y_coordinate=y_coordinate, time=time, camera_id=camera_id)
            # print(message.value['analyticsModule']['Frame_ID'])
