"""
Defines the serializers used in the DSServers api.
"""

from django.core import exceptions
from django.db import IntegrityError
from rest_framework import serializers

from ds_analytics.models import CameraAnalyticsConfig, PLAConfig
from measurement_frames.models import MeasurementFrame


# pylint: disable=missing-class-docstring
class PLAConfigListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PLAConfig
        fields = (
            'id',
            'ground_frame',
            'point_coords_in_ground_frame',
            'point_coords_in_image')


class CameraAnalyticsConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAnalyticsConfig
        abstract = True

    def create(self, validated_data):
        try:
            validated_data['camera'] = self.context['view'].validate_kwargs()
            validated_data = self._updated_data(validated_data)
            return super().create(validated_data)
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})

    def _updated_data(self, validated_data):
        raise NotImplementedError()


class PLAConfigCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PLAConfig
        fields = (
            'id',
            'ground_frame',
            'point_coords_in_ground_frame',
            'point_coords_in_image')
        extra_kwargs = {
            'id': {'readonly': True},
            'ground_frame': {'required': True},
            'point_coords_in_ground_frame': {'required': True},
            'point_coords_in_image': {'required': True},
        }

    def validate_ground_frame(self, ground_frame):
        try:
            MeasurementFrame.objects.get(id=ground_frame)
            camera = self.context['view'].validate_kwargs()

            # make sure ground frame exists within the same block
            if ground_frame.block == camera.block:
                return ground_frame
        except MeasurementFrame.DoesNotExist:
            raise exceptions.ValidationError("Frame does not exist.")

    def _updated_data(self, validated_data):
        return validated_data


class PLAConfigRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = PLAConfig
        fields = (
            'id',
            'ground_frame',
            'point_coords_in_ground_frame',
            'point_coords_in_image')


class PLAConfigUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PLAConfig
        fields = (
            'id',
            'ground_frame',
            'point_coords_in_ground_frame',
            'point_coords_in_image')

    def validate_ground_frame(self, ground_frame):
        try:
            MeasurementFrame.objects.get(id=ground_frame)
            camera = self.context['view'].validate_kwargs()

            # make sure ground frame exists within the same block
            if ground_frame.block == camera.block:
                return ground_frame
        except MeasurementFrame.DoesNotExist:
            raise exceptions.ValidationError("Frame does not exist.")

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})
