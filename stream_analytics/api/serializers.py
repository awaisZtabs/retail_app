"""
Defines the serializers used in the locations api.
"""

from django.db import IntegrityError
from rest_framework import serializers

from stream_analytics.models import StreamAnalytic


# pylint: disable=missing-class-docstring
class StreamAnalyticListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamAnalytic
        fields = ('id', 'frame_id', 'tracking_id',
                  'x_coordinate', 'y_coordinate', 'time')


class StreamAnalyticCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamAnalytic
        fields = ('id', 'frame_id', 'tracking_id',
                  'x_coordinate', 'y_coordinate', 'time')
        extra_kwargs = {
            'id': {'required': True},
            'frame_id': {'required': True},
            'tracking_id': {'required': True},
            'x_coordinate': {'required': True},
            'y_coordinate': {'required': True},
        }

    def create(self, validated_data):
        try:
            validated_data['camera'] = self.context['view'].validate_kwargs()
            return super().create(validated_data)
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})
