from rest_framework_nested import routers

from .views import (
    IMUserCreateAPIView,
    IMUserListAPIView,
    IMUserDetailAPIView,
    IMUserUpdateAPIView,
    IMUserDeleteAPIView
)

from .views import IMUserViewSet,IMGroupViewSet, IMRoleViewSet

from django.urls import include, path
app_name = 'identityManager-api'

# ------ Identity Manager Router Configuration-----------------------------------------------------------
# Router conf. gives us the luxury to not define paths manually, instead router enables all CRUD paths with accordance
# to a predifined path structure.

# identitymanager_router = routers.DefaultRouter()
# identitymanager_router.register('imusers', IMUserViewSet)
# identitymanager_router.register('imgroups', IMGroupViewSet)
# identitymanager_router.register('imroles', IMRoleViewSet)
#
# imgroups_router = routers.NestedSimpleRouter(identitymanager_router, 'imgroups', lookup='imgroup')
# imgroups_router.register('memberusers', IMGroupMemberUserViewSet, base_name='imgroup-memberusers')
# imgroups_router.register('membergroups', IMGroupMemberGroupViewSet, base_name='imgroup-membergroups')
#
# imroles_router = routers.NestedSimpleRouter(identitymanager_router, 'imroles', lookup='imrole')
# imroles_router.register('permissions', IMRolePermissionViewSet, base_name='imrole-permissions')
# imroles_router.register('assignedusers', IMRoleAssignedUserViewSet, base_name='imrole-assignedusers')
# imroles_router.register('assignedgroups', IMRoleAssignedGroupViewSet, base_name='imrole-assignedgroups')

urlpatterns = [

    # --------- Router Based Paths ------------
    # path('', include(identitymanager_router.urls)),

    # --------- Custom paths -------------------
    # Following paths are just for imuser API
    path('imuser/', IMUserListAPIView.as_view(), name='imuser-list'),
    path('imuser/create/', IMUserCreateAPIView.as_view(), name='imuser-create'),
    path('imuser/<int:pk>/', IMUserDetailAPIView.as_view(), name="imuser-detail"),
    path('imuser/<int:pk>/edit/', IMUserUpdateAPIView.as_view(), name="imuser-edit"),
    path('imuser/<int:pk>/delete/', IMUserDeleteAPIView.as_view(), name="imuser-delete"),
]
