"""
Defines the serializers used in the DSServers api.
"""

from django.db import IntegrityError
from rest_framework import exceptions, serializers

from cameras.models import Camera
from ds_servers.models import (DSDiagnostics, DSLogEntry, DSServer,
                               DSServerConfig)
from locations.models import Block


# pylint: disable=missing-class-docstring
class DSServerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DSServer
        fields = ('id', 'ip_addr')


class DSServerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DSServer
        fields = ('id', 'ip_addr')
        extra_kwargs = {
            'ip_addr': {'required': True}
        }

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})


class LogEntryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = DSLogEntry
        fields = ('id', 'message', 'received_at', 'ds_server')


class DiagnosticsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = DSDiagnostics
        fields = (
            'id', 'ds_server', 'cpu_utilization',
            'gpu_utilization', 'memory_usage',
            'gpu_memory_usage', 'temperature', 'received_at')


class DSServerRetrieveSerializer(serializers.ModelSerializer):
    log_entries = serializers.SerializerMethodField()
    diagnostics = serializers.SerializerMethodField()

    def get_log_entries(self, server):
        """
        Returns the log entries of server.
        """
        log_entries = DSLogEntry.objects.filter(
            ds_server__id=server.id)
        return \
            LogEntryDetailSerializer(
                log_entries, many=True, context=self.context).data

    def get_diagnostics(self, server):
        """
        Returns the diagnostics of server.
        """
        diagnostics = DSDiagnostics.objects.filter(
            ds_server__id=server.id)
        return \
            DiagnosticsDetailSerializer(
                diagnostics, many=True, context=self.context).data

    class Meta:
        model = DSServer
        fields = (
            'id',
            'ip_addr',
            'status',
            'last_echo_at',
            'log_entries',
            'diagnostics')


class DSServerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DSServer
        fields = ('id', 'ip_addr')

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})


class DSServerConfigCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DSServerConfig
        fields = ('id', 'ds_server')
        extra_kwargs = {
            'ds_server': {'required': True}
        }

    def create(self, validated_data):
        try:
            validated_data['ds_server'] = \
                self.context['view'].validate_kwargs()
            return super().create(validated_data)
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})


class DSServerConfigRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = DSServerConfig
        fields = ('id', 'cameras', 'blocks')


class AddRemoveCamerasSerializerBase(serializers.ModelSerializer):
    camera = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = DSServerConfig
        fields = ('id', 'cameras', 'blocks', 'camera')
        extra_kwargs = {
            'cameras': {'read_only': True},
            'blocks': {'read_only': True},
        }

    def validate_camera(self, camera):
        try:
            return Camera.objects.get(pk=camera)
        except Camera.DoesNotExist:
            raise exceptions.ValidationError("Camera does not exist.")


class AddCameraSerializer(AddRemoveCamerasSerializerBase):

    def update(self, instance, validated_data):
        try:
            instance.cameras.add(validated_data['camera'])
            return instance
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})


class RemoveCameraSerializer(AddRemoveCamerasSerializerBase):

    def update(self, instance, validated_data):
        try:
            instance.cameras.remove(validated_data['camera'])
            return instance
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})


class AddRemoveBlocksSerializerBase(serializers.ModelSerializer):
    block = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = DSServerConfig
        fields = ('id', 'cameras', 'blocks', 'block')
        extra_kwargs = {
            'cameras': {'read_only': True},
            'blocks': {'read_only': True},
        }

    def validate_block(self, camera):
        try:
            return Block.objects.get(pk=camera)
        except Block.DoesNotExist:
            raise exceptions.ValidationError("Block does not exist.")


class AddBlockSerializer(AddRemoveBlocksSerializerBase):

    def update(self, instance, validated_data):
        try:
            instance.blocks.add(validated_data['block'])
            return instance
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})


class RemoveBlockSerializer(AddRemoveBlocksSerializerBase):

    def update(self, instance, validated_data):
        try:
            instance.blocks.remove(validated_data['block'])
            return instance
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})
