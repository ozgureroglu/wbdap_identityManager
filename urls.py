__author__ = 'ozgur'

from django.urls import path, include
from .views import *

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
    path('', landing_page, name='landing-page'),
    path('imuser/', imUser, name='imUser'),
    path('imuser/gen/', generate_user_data, name=' generate-user-data'),
    path('imuser/delgen/', delete_generated_user_data, name='delete-generated-user-data'),
    path('imuser/add/', add_imuser, name='addUser'),
    path('imuser/make_superuser/<int:pk>/', make_superuser, name='make_superuser'),
    path('imuser/make_staff/<int:pk>/', make_staff, name='make_staff'),
    path('imuser/lock/<int:pk>/', lock, name='lock'),
    path('imuser/update/<int:pk>/', UserUpdate.as_view(), name='user-update'),
    path('imuser/delete/<int:pk>/', delete_user, name='deleteUser'),
    path('imuser/autocompleteUsers/', autocompleteUsers,name='autocompleteUsers'),
    # ------------------------------------------------------------

    path('imgroup/', imGroup, name='imGroup'),
    path('imuser/gen/', generate_group_data, name=' generate-group-data'),
    path('imgroup/<int:pk>/', imgroup_home, name='imgroup_home'),
    path('imgroup/<int:pk>/memberUser/add/', addMemberUser, name='addMemberUser'),
    path('imgroup/<int:pk>/memberUser/remove/<int:id>/', removeMemberUser, name='removeMemberUser'),
    path('imgroup/<int:pk>/memberGroup/add/', addMemberGroup, name='addMemberGroup'),
    path('imgroup/<int:pk>/memberGroup/remove/<int:id>/', removeMemberGroup, name='removeMemberGroup'),
    path('imgroup/add/', add_group, name='addGroup'),
    path('imgroup/delete/<int:pk>/', delete_imgroup, name='deleteIMGroup'),
    path('imgroup/autocompleteGroups/', autocompleteGroups, name='autocompleteGroups'),
    # ------------------------------------------------------------

    path('imrole/', imRole, name='imRole'),
    path('imrole/<int:pk>/', imRole_home, name='imRole_home'),
    path('imuser/gen/', generate_role_data, name=' generate-role-data'),
    path('imrole/<int:pk>/assignedUser/add', assignUsersToRole, name='assignUsersToRole'),
    path('imrole/<int:pk>/assignedGroup/add', assignGroupsToRole, name='assignGroupsToRole'),
    path('imrole/<int:pk>/permission/add', addPermissionToRole, name='addPermissionToRole'),
    path('imrole/<int:pk>/permission/remove/<int:id>/', removePermissionFromRole, name='removePermissionFromRole'),
    path('imrole/add/', add_imrole, name='add_imrole '),
    path('imrole/delete/<int:pk>/', delete_imrole, name='deleteIMRole'),
    path('imrole/autocompletePermissions/', autocompletePermissions, name='autocompletePermissions'),



    # ------------------------------------------------------------
    path('permission/autocompletePermissions/', autocompletePermissions,name='autocompletePermissions'),

    # ------------------------------------------------------------

    path('getusers/', get_user_list, name='getUsers'),
    path('changepassword/', changePassword, name='changepassword'),

    # ------------------------------------------------------------

    path('dashboard/', dashboard, name='dashboard'),

    # User'lari id degerlerine gore istiyorum
    # Asagidaki ikinci RE opsiyonel bir d bolumu iceriyor.
    # path('profile/<int:pk>/',user_profile_page,name='profile'),

    # path('prot/', ProfileWizard.as_view([AddressForm, ExperienceForm,EducationForm,ProjectsForm]))
    # ------------------------------------------------------------

    path('profile/<int:pk>/', view_user_profile, name='profileView'),
    path('profile/<int:pk>/edit/', ProfileWizard.as_view(FORMS), name='edit-profile'),


    path('cleandefs/', cleandefs, name='cleandefs'),
    path('gendefs/', gendefs, name='gendefs'),


]
