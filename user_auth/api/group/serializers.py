"""
Defines the serializers used in user REST api views.
"""
from django.contrib.auth import get_user_model
# pylint: disable=missing-class-docstring
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import exceptions, serializers

from app_organizations import permissions
from user_auth.models import DefaultUserGroups, UserGroup

USER_MODEL = get_user_model()


class GroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = ['id', 'name', 'authority']


class PermissionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

#  10.7.212.58


class GroupCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = ['name', 'authority', 'permissions']
        # fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'authority': {'required': True},
            'permissions': {'required': False}
        }

    def validate_authority(self, authority):
        # authority of new groups cannot be greater than existing free user
        if authority < DefaultUserGroups.FREE_USER.value:
            raise exceptions.ValidationError("Can only be greater than or equal to {}".format(
                DefaultUserGroups.FREE_USER.value))
        return authority

    def create(self, validated_data):
        i = 0
        perms = validated_data["permissions"]
        try:
            instance, _ = self.Meta.model.objects.update_or_create(
                name=validated_data.get('name'), authority=validated_data.get('authority'))
            for permissions in perms:
                instance.permissions.add(permissions.id)
            return instance
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})


class GroupRetrieveAppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ['id']


class GroupRetrieveSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    # permissions = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        fields = ['name', 'authority', 'users', 'permissions']
        # extra_kwargs = {
        #     'permissions': {'read_only': True},
        # }

    def get_users(self, instance):
        return GroupRetrieveAppUserSerializer(
            instance.user_set.all(), many=True, context=self.context).data
# for adding permission object to group data

    # def get_permissions(self, instance):
    #     return PermissionListSerializer(
    #         instance.permissions.all(), many=True, context=self.context).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        users = []
        # permissionss = []
        for user in data['users']:
            users.append(user['id'])
        # for permission in data['permissions']:
        #     permissionss.append(permission['name'])
        data['users'] = users
        # data['permissions'].name = permissionss
        return data


class GroupUpdateSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        fields = ['name', 'authority', 'users', 'permissions']
        extra_kwargs = {
            "name": {"required": False},
            "authority": {"required": False},
        }

    def validate_authority(self, authority):
        # authority of new groups cannot be greater than existing free user
        if authority < DefaultUserGroups.FREE_USER.value:
            raise exceptions.ValidationError(
                "Can only be greater than or equal to {}".format(
                    DefaultUserGroups.FREE_USER.value))
        return authority

    def get_users(self, instance):
        return GroupRetrieveAppUserSerializer(
            instance.user_set.all(), many=True, context=self.context).data

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})

    def to_representation(self, instance):
        data = super().to_representation(instance)
        users = []
        for user in data['users']:
            users.append(user['id'])
        data['users'] = users
        return data


class AddRemoveUserSerializerBase(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    user = serializers.UUIDField(required=True, write_only=True)

    class Meta:
        model = UserGroup
        fields = ['name', 'authority', 'users', 'user']
        extra_kwargs = {
            'name': {'read_only': True},
            'authority': {'read_only': True},
        }

    def get_users(self, instance):
        return GroupRetrieveAppUserSerializer(
            instance.user_set.all(), many=True, context=self.context).data

    def validate_user(self, user):
        try:
            user_to_be_added = USER_MODEL.objects.get(pk=user)

            # make sure the request user has authority to add pk
            # user to the group
            request_user = self.context['request'].user

            # note that authority is highest with lowest value
            if user_to_be_added.highest_group:  # user's not in any group
                if user_to_be_added.highest_group.authority < \
                        request_user.highest_group.authority:
                    raise exceptions.ValidationError(
                        "You are unathorized to make changes to this user.")
            return user_to_be_added
        except USER_MODEL.DoesNotExist:
            raise exceptions.ValidationError("User does not exist.")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        users = []
        for user in data['users']:
            users.append(user['id'])
        data['users'] = users
        return data


class AddUserSerializer(AddRemoveUserSerializerBase):

    def update(self, instance, validated_data):
        try:
            instance.user_set.add(validated_data['user'])
            return instance
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})


class RemoveUserSerializer(AddRemoveUserSerializerBase):

    def update(self, instance, validated_data):
        try:
            instance.user_set.remove(validated_data['user'])
            return instance
        except IntegrityError as ex:
            raise serializers.ValidationError({"detail": ex.__cause__})
