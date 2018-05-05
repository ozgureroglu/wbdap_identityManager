from identityManager.models import IMRole, IMGroup, IMUser

__author__ = 'ozgur'

from rest_framework import serializers



class IMUserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="api:imuser-detail")

    class Meta:
        model=IMUser
        fields = ('id','url','username','first_name','last_name','email','last_login','is_superuser','is_active','is_staff')

class MemberGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=IMGroup
        fields = ('name',)

class IMGroupSerializer(serializers.HyperlinkedModelSerializer):
    # answer = serializers.StringRelatedField(many=True)
    # memberUsers = IMUserSerializer(read_only=True,many=True)
    # memberGroups = MemberGroupSerializer(read_only=False,many=True)
    url = serializers.HyperlinkedIdentityField(view_name="v1:imgroup-detail")

    class Meta:
        model=IMGroup
        fields = ('id','url','name','description','active')

        def __str__(self):
            return self.name

class IMRoleSerializer(serializers.HyperlinkedModelSerializer):
    # answer = serializers.StringRelatedField(many=True)
    class Meta:
        model=IMRole
        fields = ('id','name','description')

