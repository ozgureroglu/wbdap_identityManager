from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedIdentityField, ModelSerializer
from identityManager.models import IMRole, IMGroup, IMGroup, IMUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


# --------- CRUD Serializers -----------------------------
# https://www.youtube.com/watch?v=dfIB-LthIpE&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=9


class IMGroupCreateSerializer(ModelSerializer):
    class Meta:
        model = IMGroup
        fields = ('name', 'description', 'active')
        # Following kwarg avoids the password to be returned
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        This method overrides the ModelSerializers create method, so that model creation behaves differently than
        the default one. If we want to change the create behaviour at APIView level this method will be defined as
        perform_create() which overrides the perform_create() method of CreateModelMixin and this method simply calls
        serializer.save(). So we can pass parameters to save method to override data fields
        such as serializer.save(user=self.request.user)

        to serializer.save
        :param validated_data:
        :return:
        """
        group = IMGroup.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name'],
            # email=validated_data['email'],
            # password=make_password(validated_data['password'])
        )
        return group


class IMGroupListSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="identityManager-api:imgroup-detail")

    class Meta:
        model = IMGroup
        fields = ('id', 'url', 'name', 'active', 'description')


class IMGroupDetailSerializer(ModelSerializer):

    class Meta:
        model = IMGroup
        fields = ('id', 'name', 'description', 'active')


# ---------------------------------------------------------------

# Serializer to serialize the member users of a group
class IMGroupMemberUserListSerializer(ModelSerializer):
    class Meta:
        model = IMUser
        fields = ('username',)


# Serializer to serialize the member users of a group
class IMGroupMemberUserCreateSerializer(ModelSerializer):
    class Meta:
        model = IMUser
        fields = ('username',)


class IMGroupSerializer(HyperlinkedModelSerializer):
    # answer = serializers.StringRelatedField(many=True)
    # memberUsers = IMGroupListSerializer(read_only=True,many=True)
    # memberGroups = MemberGroupSerializer(read_only=False,many=True)
    url = HyperlinkedIdentityField(view_name="identityManager-api:imgroup-detail")

    class Meta:
        model = IMGroup
        fields = ('id', 'url', 'name', 'description', 'active')

        def __str__(self):
            return self.name


class IMRoleSerializer(HyperlinkedModelSerializer):
    # answer = serializers.StringRelatedField(many=True)
    class Meta:
        model = IMRole
        fields = ('id', 'name', 'description')


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('app_label', 'model')


class IMPermissionSerializer(ModelSerializer):
    content_type = ContentTypeSerializer(many=False, read_only=True)
    # content_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='app_label')

    class Meta:
        model = Permission
        fields = ('name', 'content_type')

