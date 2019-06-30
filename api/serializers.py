from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password

from identityManager.models import IMRole, IMGroup, IMUser

__author__ = 'ozgur'

from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedIdentityField, ModelSerializer

from .imuser_serializer import *
from .imgroup_serializer import *
from .imrole_serializer import *