from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from identityManager.models import IMRole, IMGroup, IMUser

__author__ = 'ozgur'

from rest_framework import serializers



class IMUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="identityManager-api:imuser-detail")

    class Meta:
        model=IMUser
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email', 'last_login', 'is_superuser', 'is_active', 'is_staff')

class MemberGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=IMGroup
        fields = ('name',)

class IMGroupSerializer(serializers.HyperlinkedModelSerializer):
    # answer = serializers.StringRelatedField(many=True)
    # memberUsers = IMUserSerializer(read_only=True,many=True)
    # memberGroups = MemberGroupSerializer(read_only=False,many=True)
    url = serializers.HyperlinkedIdentityField(view_name="identityManager-api:imgroup-detail")

    class Meta:
        model=IMGroup
        fields = ('id', 'url', 'name', 'description', 'active')

        def __str__(self):
            return self.name

class IMRoleSerializer(serializers.HyperlinkedModelSerializer):
    # answer = serializers.StringRelatedField(many=True)
    class Meta:
        model=IMRole
        fields = ('id', 'name', 'description')




class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('app_label', 'model')




class IMPermissionSerializer(serializers.ModelSerializer):

    content_type = ContentTypeSerializer(many=False, read_only=True)
    # content_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='app_label')

    class Meta:
        model = Permission
        fields = ('name', 'content_type')


