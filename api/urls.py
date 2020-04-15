from rest_framework_nested import routers

from .views import (
    IMUserCreateAPIView,
    IMUserListAPIView,
    IMUserDetailAPIView,
    IMUserUpdateAPIView,
    IMUserDeleteAPIView,
    IMGroupCreateAPIView,
    IMGroupListAPIView,
    IMGroupDetailAPIView,
    IMGroupUpdateAPIView,
    IMGroupDeleteAPIView,
    IMRoleCreateAPIView,
    IMRoleListAPIView,
    IMRoleDetailAPIView,
    IMRoleUpdateAPIView,
    IMRoleDeleteAPIView,
    IMGroupMemberUserListAPIView, IMGroupMemberUserUpdateAPIView, IMGroupMemberUserDeleteAPIView,
    IMGroupMemberGroupUpdateAPIView, IMGroupMemberGroupListAPIView, IMGroupMemberGroupDeleteAPIView,
    IMRolePermissionListAPIView, IMRolePermissionCreateAPIView, IMRoleAssignedUserListAPIView,
    IMRoleAssignedGroupListAPIView, IMRoleAssignedUserCreateAPIView, IMRoleAssignedGroupCreateAPIView,
    IMRoleAssignedUserDeleteAPIView, IMRoleAssignedGroupDeleteAPIView, IMRolePermissionDeleteAPIView)

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
    # Asagidaki yontem ile API olusturulmasi islemi Class Based Generic View'ler
    # araciligi ile API olusturulmasini sagliyor.
    # Following paths are just for imuser API
    path('imuser/', IMUserListAPIView.as_view(), name='imuser-list'),
    path('imuser/create/', IMUserCreateAPIView.as_view(), name='imuser-create'),
    path('imuser/<int:pk>/', IMUserDetailAPIView.as_view(), name="imuser-detail"),
    path('imuser/<int:pk>/edit/', IMUserUpdateAPIView.as_view(), name="imuser-edit"),
    path('imuser/<int:pk>/delete/', IMUserDeleteAPIView.as_view(), name="imuser-delete"),

    # Following paths are just for imgroup API
    path('imgroup/', IMGroupListAPIView.as_view(), name='imgroup-list'),
    path('imgroup/create/', IMGroupCreateAPIView.as_view(), name='imgroup-create'),
    path('imgroup/<int:pk>/', IMGroupDetailAPIView.as_view(), name="imgroup-detail"),
    path('imgroup/<int:pk>/edit/', IMGroupUpdateAPIView.as_view(), name="imgroup-edit"),
    path('imgroup/<int:pk>/delete/', IMGroupDeleteAPIView.as_view(), name="imgroup-delete"),

    path('imgroup/<int:pk>/memberuser/', IMGroupMemberUserListAPIView.as_view(), name="imgroup-users"),
    path('imgroup/<int:pk>/memberuser/add/', IMGroupMemberUserUpdateAPIView.as_view(), name="imgroup-user-add"),
    path('imgroup/<int:pk>/memberuser/<int:userpk>/remove/', IMGroupMemberUserDeleteAPIView.as_view(), name="imgroup-user-remove"),

    path('imgroup/<int:pk>/membergroup/', IMGroupMemberGroupListAPIView.as_view(), name="imgroup-users"),
    path('imgroup/<int:pk>/membergroup/add/', IMGroupMemberGroupUpdateAPIView.as_view(), name="imgroup-user-add"),
    path('imgroup/<int:pk>/membergroup/<int:grouppk>/remove/', IMGroupMemberGroupDeleteAPIView.as_view(),
         name="imgroup-user-remove"),


    # Following paths are just for imrole API
    path('imrole/', IMRoleListAPIView.as_view(), name='imrole-list'),
    path('imrole/create/', IMRoleCreateAPIView.as_view(), name='imrole-create'),
    path('imrole/<int:pk>/', IMRoleDetailAPIView.as_view(), name="imrole-detail"),
    path('imrole/<int:pk>/edit/', IMRoleUpdateAPIView.as_view(), name="imrole-edit"),
    path('imrole/<int:pk>/delete/', IMRoleDeleteAPIView.as_view(), name="imrole-delete"),


    path('imrole/<int:pk>/permission/', IMRolePermissionListAPIView.as_view(), name="imrole-permission-list"),
    path('imrole/<int:pk>/permission/add/', IMRolePermissionCreateAPIView.as_view(), name="imrole-permission-create"),
    # path('imrole/<int:pk>/permission/<int:perm_id>/', IMRolePermissionListAPIView.as_view(), name="imrole-permission-list"),
    # path('imrole/<int:pk>/permission/<int:perm_id>/edit/', IMRolePermissionListAPIView.as_view(), name="imrole-permission-list"),
    path('imrole/<int:pk>/permission/<int:id>/delete/', IMRolePermissionDeleteAPIView.as_view(), name="imrole-permission-list"),


    path('imrole/<int:pk>/user/', IMRoleAssignedUserListAPIView.as_view(), name="imrole-assigneduser-list"),
    path('imrole/<int:pk>/user/add/', IMRoleAssignedUserCreateAPIView.as_view(), name="imrole-assigneduser-create"),
    path('imrole/<int:pk>/user/<int:id>/delete/', IMRoleAssignedUserDeleteAPIView.as_view(), name="imrole-assigneduser-delete"),

    path('imrole/<int:pk>/group/', IMRoleAssignedGroupListAPIView.as_view(), name="imrole-assignedgroup-list"),
    path('imrole/<int:pk>/group/add/', IMRoleAssignedGroupCreateAPIView.as_view(), name="imrole-assignedgroup-create"),
    path('imrole/<int:pk>/group/<int:id>/delete/', IMRoleAssignedGroupDeleteAPIView.as_view(), name="imrole-assignedgroup-delete"),
]
