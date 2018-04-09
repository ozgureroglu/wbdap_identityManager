__author__ = 'ozgur'

from django.urls import path, include
from identityManager.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()



# # --------------------------------------------------------------------
#
# # Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register('users', IMUserViewSet,base_name="users")
# router.register('groups', IMGroupViewSet,base_name="groups")
# router.register('roles', IMRoleViewSet)
#


app_name='identityManager'

urlpatterns = [


    # path('',index_page,name='index'),
    path('',landing_page,name='landing-page'),
    path('user/', imUser, name='imUser'),
    path('user/add/', add_imuser, name='addUser'),
    path('user/make_superuser/<int:pk>/', make_superuser, name='make_superuser'),
    path('user/make_staff/<int:pk>/', make_staff, name='make_staff'),
    path('user/lock/<int:pk>/', lock, name='lock'),
    path('user/update/<int:pk>/', UserUpdate.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', delete_user, name='deleteUser'),
    path('user/autocompleteUsers/',autocompleteUsers,name='autocompleteUsers'),
    # ------------------------------------------------------------

    path('imgroup/',imGroup,name='imGroup'),
    path('imgroup/<int:pk>/', imgroup_home, name='imgroup_home'),
    path('imgroup/<int:pk>/memberUser/add/', addMemberUser, name='addMemberUser'),
    path('imgroup/<int:pk>/memberUser/remove/<id>/', removeMemberUser, name='removeMemberUser'),
    path('imgroup/<int:pk>/memberGroup/add/', addMemberGroup, name='addMemberGroup'),
    path('imgroup/<int:pk>/memberGroup/remove/<id>/', removeMemberGroup, name='removeMemberGroup'),
    path('imgroup/add/', add_group, name='addGroup'),
    path('imgroup/delete/<int:pk>/', delete_imgroup, name='deleteIMGroup'),
    path('imgroup/autocompleteGroups/',autocompleteGroups,name='autocompleteGroups'),
    # ------------------------------------------------------------

    path('role/', imRole, name='imRole'),
    path('role/<int:pk>/', imRole_home, name='imRole_home'),
    path('role/<int:pk>/assignedUser/add', assignUsersToRole, name='assignUsersToRole'),
    path('role/<int:pk>/assignedGroup/add', assignGroupsToRole, name='assignGroupsToRole'),
    path('role/<int:pk>/permission/add', addPermissionToRole, name='addPermissionToRole'),
    path('role/<int:pk>/permission/remove/<id>/', removePermissionFromRole, name='removePermissionFromRole'),
    path('role/add/', add_imrole, name='add_imrole '),
    path('role/delete/<int:pk>/', delete_imrole, name='deleteIMRole'),

    # ------------------------------------------------------------
    path('permission/autocompletePermissions/',autocompletePermissions,name='autocompletePermissions'),

    # ------------------------------------------------------------

    path('getusers/', get_user_list, name='getUsers'),
    path('changepassword/', changePassword, name='changepassword'),

    # ------------------------------------------------------------

    path('dashboard/',user_dashboard,name='dashboard'),

    # User'lari id degerlerine gore istiyorum
    # Asagidaki ikinci RE opsiyonel bir d bolumu iceriyor.
    # path('profile/<int:pk>/',user_profile_page,name='profile'),

    # path('prot/', ProfileWizard.as_view([AddressForm, ExperienceForm,EducationForm,ProjectsForm]))
    # ------------------------------------------------------------

    path('profile/<int:pk>/', view_user_profile, name='profileView'),
    path('profile/edit/<int:pk>/', ProfileWizard.as_view(FORMS))

]
