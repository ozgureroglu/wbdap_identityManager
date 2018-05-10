import logging

import simplejson
from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import resolve
from django.views.generic import UpdateView
from formtools.wizard.views import SessionWizardView
from rest_framework import viewsets


from .forms import *
from .models import IMUser, IMGroup, IMRole, IMUserProfile
from rest_framework.response import Response
import django_filters.rest_framework
from rest_framework import filters



#Get an instance of the logger: Name should be the name of the logger in settings LOGGING field
from .serializers import *
from projectCore.datatable_viewset import ModifiedViewSet

logger = logging.getLogger('django.request')

# -------------------------------------------------------------

@login_required()
def index_page(request):
    users = IMUser.objects.all()
    return render(request,
        'identityManager/index.html', {}
    )

@login_required()
def landing_page(request):
    return render(request,
        'identityManager/landing.html', {}
    )

@login_required()
def imUser(request):
    user_list = IMUser.objects.all()
    paginator=Paginator(user_list, 30)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request,
        'identityManager/index.html',
        # 'identityManager/index2.html', {'users': users, 'form': AddUserForm}
    )


@login_required()
def add_imuser(request):
    if request.method == 'POST':
        logger.info(request.POST)
        form = AddUserForm(request.POST)
        if form.is_valid():
            logger.info('Form is valid')

            try:
                user = IMUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email'],
                )
                user.save();
                logger.info("User has been created with user id : " + str(user.id))
            except:
                logger.warning("User clould not be created")

            user.first_name = form.cleaned_data['first_name'];
            user.last_name = form.cleaned_data['last_name'];
            user.is_superuser = False;
            user.save();

            # Create a profile for each created user and connect them 1-to-1
            try:
                IMUserProfile.objects.get_or_create(owner=user);
            except:
                logger.warning('failed to create profile or imuser')

            user.save();
            # return http.HttpResponseRedirect('/identityManager/')
            # return http.HttpResponseRedirect('identityManager/index_page')
        else:
            logger.warning('Form is invalid')
            print(form.errors)
            print(form.errors.as_json())
            # return HttpResponse(form.errors.as_json())
    else:
        logger.info('Bad requerst: GET not allowed')
        form = AddUserForm()
    users = User.objects.all()
    variables = {'form': form, 'users': users}
    return render(request, 'identityManager/modal/addIdentity_ModalContent.html', variables)


@login_required()
def imGroup(request):
    imgroups = IMGroup.objects.all()
    return render(request,
        'identityManager/index.html', {'imgroups':imgroups}
    )

@login_required()
def delete_imgroup(request, pk):
    imgroup = IMGroup.objects.get(id=pk)
    imgroup.delete()
    return http.HttpResponseRedirect('/identityManager/imgroup/')

@login_required()
def imgroup_home(request, pk):
    imgroup = IMGroup.objects.get(id=pk)
    return render(request, 'identityManager/imgroup_home.html',
                  {'imgroup':imgroup,
                   })



@login_required()
def imRole_home(request, pk):
    imrole = IMRole.objects.get(id=pk)
    return render(request, 'identityManager/imrole_home.html',
                  {'imrole':imrole,
                   # 'groups': imrole.memberGroups.all(),
                   # 'users': imrole.memberUsers.all(),
                   # 'permissions': imrole.permissions.all(),
                   })



@login_required()
def addMemberUser(request,pk):

    if request.method=='POST':

        imgroup = IMGroup.objects.get(id=pk)

        users=request.POST['users']

        user_list=str(users).strip(' ').strip(',')
        user_list=user_list.split(',')

        for user in user_list:
            user_data=(user.strip()).split(' ')
            if user_data.__len__() == 2:
                imgroup.memberUsers.add(IMUser.objects.get(first_name=user_data[0],last_name=user_data[1]))
            elif user_data.__len__() > 2:
                imgroup.memberUsers.add(IMUser.objects.get(first_name=user_data[0]+" "+user_data[1], last_name=user_data[2]))
            else:
                return HttpResponse(status=500)

    else:
        pass
    return HttpResponseRedirect('/identityManager/imgroup/'+str(pk)+"/")


@login_required()
def assignUsersToRole(request,pk):
    if request.method=='POST':

        imrole = IMRole.objects.get(id=pk)

        users=request.POST['users']

        user_list=str(users).strip(' ').strip(',')
        user_list=user_list.split(',')

        for user in user_list:
            name_surname=(user.strip()).split(' ')
            imrole.memberUsers.add(IMUser.objects.get(first_name=name_surname[0],last_name=name_surname[1]))

    else:
        pass
    return HttpResponseRedirect('/identityManager/role/'+str(pk)+"/")


@login_required()
def assignGroupsToRole(request,pk):
    if request.method=='POST':

        imrole = IMRole.objects.get(id=pk)

        groups=request.POST['groups']

        group_list=str(groups).strip(' ').strip(',')
        group_list=group_list.split(',')

        for group in group_list:
            groupName=(group.strip()).split(':')
            imrole.memberGroups.add(IMGroup.objects.get(name=groupName[0]))

    else:
        pass
    return HttpResponseRedirect('/identityManager/role/'+str(pk)+"/")




@login_required()
def addMemberGroup(request,pk):
    if request.method=='POST':

        imgroup = IMGroup.objects.get(id=pk)

        groups=request.POST['groups']

        group_list=str(groups).strip(' ').strip(',')
        group_list=group_list.split(',')

        for group in group_list:
            groupName=(group.strip()).split(':')
            print(groupName[0])
            imgroup.memberGroups.add(IMGroup.objects.get(name=groupName[0]))

    else:
        pass
    return HttpResponseRedirect('/identityManager/imgroup/'+str(pk)+"/")


@login_required()
def addPermissionToRole(request,pk):
    if request.method=='POST':

        imrole = IMRole.objects.get(id=pk)

        permissions=request.POST['permissions']
        if permissions=='all':
            for perm in Permission.objects.get(content_type__app_label=resolve(request.path).app_name):
                imrole.permissions.add(perm)
        else:
            perm_list=str(permissions).strip(' ').strip(',')
            perm_list=perm_list.split(',')

            for perm in perm_list:
                permParsed=(perm.strip()).split(':')
                imrole.permissions.add(Permission.objects.get(codename=permParsed[1]))

    else:
        pass
    return HttpResponseRedirect('/identityManager/role/'+str(pk)+"/")


@login_required()
def removePermissionFromRole(request,pk,id):
    try:
        imrole = IMRole.objects.get(id=pk)
        imrole.permissions.remove(Permission.objects.get(id=id))
    except:
        logger.warning("Unable to remove permission from role")
    return HttpResponseRedirect('/identityManager/role/'+str(pk)+"/")





@login_required()
def removeMemberUser(request,pk,id):
    try:
        imgroup = IMGroup.objects.get(id=pk)
        imgroup.memberUsers.remove(IMUser.objects.get(id=id))
    except:
        logger.warning("Unable to remove users from group")
    return HttpResponseRedirect('/identityManager/imgroup/'+str(pk)+"/")


@login_required()
def removeMemberGroup(request,pk,id):
    try:
        imgroup = IMGroup.objects.get(id=pk)
        imgroup.memberGroups.remove(IMGroup.objects.get(id=id))
    except:
        logger.warning("Unable to remove group from group")
    return HttpResponseRedirect('/identityManager/imgroup/'+str(pk)+"/")

@login_required()
def autocompleteUsers(request):
    search_qs = IMUser.objects.filter(username__startswith=request.GET['term'])

    results = []
    for r in search_qs:
        person = {}
        person['username']=r.username
        person['first_name'] = r.first_name
        person['last_name'] = r.last_name
        results.append(person)

    resp = request.GET['callback'] + '(' + simplejson.dumps(results) + ');'

    return HttpResponse(resp, content_type='application/json')


@login_required()
def autocompleteGroups(request):
    search_qs = IMGroup.objects.filter(name__startswith=request.GET['term'])
    results = []
    for r in search_qs:
        grp = {}
        grp['name'] = r.name
        grp['description'] = r.description
        results.append(grp)

    resp = request.GET['callback'] + '(' + simplejson.dumps(results) + ');'
    return HttpResponse(resp, content_type='application/json')




@login_required()
def autocompletePermissions(request):
    search_qs = Permission.objects.filter(content_type__app_label__startswith=request.GET['term'])
    results = []
    for permi in search_qs:
        perm ={}
        perm['app_label'] = permi.content_type.app_label
        perm['codename'] = permi.content_type.model
        perm['name'] = permi.name
        results.append(perm)

    resp = request.GET['callback'] + '(' + simplejson.dumps(results) + ');'

    return HttpResponse(resp, content_type='application/json', status=200)





@login_required()
def add_group(request):
    if request.method == 'POST':
        logger.info(request.POST)
        form = AddGroupForm(request.POST)
        if form.is_valid():
            logger.info('Form is valid')

            imgroup, status = IMGroup.objects.get_or_create(
                name=form.cleaned_data['name'],
                description = form.cleaned_data['description']
            )
            if status == True:
                logger.info("Created group")
            else:
                logger.warning("create group failed")

            # imgroup.memberUser = form.cleaned_data["memberUsers"];
            # imgroup.memberGroup = form.cleaned_data["memberGroups"];
            imgroup.active = False;

            imgroup.save();

            logger.info("IMGroup has been created with group id : " + str(imgroup.id))

    else:
        logger.info('Bad request: GET not allowed')
        form = AddGroupForm()
    imgroups = IMGroup.objects.all()
    variables = {'form': form, 'imgroups': imgroups}
    return render(request, 'identityManager/modal/addIdentity_ModalContent.html', variables)


@login_required()
def imRole(request):
    imroles = IMRole.objects.all()
    return render(request,
        'identityManager/index.html', {'imroles':imroles}
    )

@login_required()
def add_imrole(request):
    if request.method == 'POST':
        logger.info(request.POST)
        form = AddRoleForm(request.POST)

        print(request.POST)
        if form.is_valid():
            logger.info('Form is valid')

            role,ok = IMRole.objects.get_or_create(
                name = form.cleaned_data['roleName']+"_role",
                roleName=form.cleaned_data['roleName'],
                description=form.cleaned_data['description'],
            )
            print(ok)
            if ok==True:
                role.save();
                logger.info("Role has been created : " + str(role.id))
            else:
                logger.info("Role could not be created : " + str(role.id))

    else:
        logger.info('GET request')
        form = AddRoleForm()
    imroles = IMRole.objects.all()
    variables = {'form': form, 'roles': imroles}
    return render(request, 'identityManager/modal/addIdentity_ModalContent.html', variables)

@login_required()
def delete_imrole(request, pk):
    imrole = IMRole.objects.get(id=pk)
    imrole.delete()
    return http.HttpResponseRedirect('/identityManager/role/')

@login_required()
def get_user_list(request):

    users = User.objects.all()

    json_users = serializers.serialize('json', users)
    # dictionaries = [obj for obj in users]
    #
    # print(serializers.deserialize('json',json_users))
    # response = HttpResponse(json_users)
    # return response
    return render(request,
        'identityManager/user_list.html',{'users':users}
    )


@login_required()
def lock(request,pk):
    user = User.objects.get(id=pk)

    if not user.is_active:
        user.is_active = True
    else:
        user.is_active = False
    user.save()
    return HttpResponseRedirect('/identityManager/user/')



@login_required()
def make_superuser(request,pk):
    user = User.objects.get(id=pk)

    if not user.is_superuser:
        user.is_superuser = True
    else:
        if not user == User.objects.get(username='ozgur'):
            user.is_superuser = False
    user.save()
    return HttpResponseRedirect('/identityManager/user/')



@login_required()
def make_staff(request,pk):
    user = User.objects.get(id=pk)

    if not user.is_staff:
        user.is_staff = True
    else:
        if not user == User.objects.get(username='ozgur'):
            user.is_staff = False
    user.save()
    return HttpResponseRedirect('/identityManager/user/')


@login_required()
def changePassword(request):
    variables = {'users': User.objects.all()}
    return render(request,'user_list.html', variables)


@login_required()
def delete_user(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return http.HttpResponseRedirect('/identityManager/user/')

@login_required()
def user_edit_profile(request, id):
    user = User.objects.get(id=id)
    form = AddUserForm()
    variables={'user':user,'form':form}
    return render(request,'user_profile.html',variables)


@login_required
def user_dashboard(request):

    if request.user.is_authenticated:
        loggedInUser = request.user

        variables = {
            'username': loggedInUser.username,
        }

        return render(request,'identityManager/user_dashboard.html', variables)
    else:
        return render(request,'login')



# TODO : Profillerin gorunmesi icin login gerekli olmayabilir: ornegin Linkedin public profile secenegi var.
@login_required
def view_user_profile(request, pk):

    """
    Kullaniciya ait profil sayfasini gosteren method
    @param request:
    @return:
    """
    logger.info("Profile request for user "+str(pk)+" has been received")

    if request.user.is_authenticated:

        requestingUser = request.user
        # requestingImUser = requestingUser.im_user
        # print(requestingImUser.id)

        # Eger url'e herhangi bir pk degeri gecmemisse kullanicinin  kendi sayfasina donelim.
        if(pk is None):
            pk = requestingUser.id

        # print("PK of the user is "+ str(pk))

        profile_owner = IMUser.objects.get(id=pk)

        # Eger userprofile var ise
        if(IMUserProfile.objects.filter(owner_id=pk).exists()):
            logger.info("User has profile")
            # Lets create a profile for this user, however it should already have one while registering
            profile = profile_owner.user_profile

        else:
            # If user does not have a profile create one
            logger.warning("User has no profile; creating")
            profile=IMUserProfile(owner_id=pk)
            profile.save()

        educationalRec = profile.education_set.all()
        workExperienceRec = profile.workexperience_set.all()



        variables =  {
            'username': requestingUser.username,

            'profile':profile,
            'profileOwner' : profile_owner,
            'educationalRec':educationalRec,
            'workExperienceRec': workExperienceRec,
            # 'extendeduserdata':extendeduserdata,
            # 'ownedTasks': getOwnedTasks(loggedInUser),
            # 'assignedTasks': getUserTasks(loggedInUser),
            # 'object_list': blog.views.getAllBlogsOfMe(request.user),
            # 'tags':blog.views.getTagsOfPosts(blog.views.getAllBlogsOfMe(request.user))
        }

        return render(request,
            'identityManager/user_profile_page.html', variables)
    else:
        return render(request,'login')



def editProfile():
    pass



TEMPLATES={"address": "examApp/forms/addressForm.html",
           "education": "examApp/forms/addressForm.html",
           "experience": "examApp/forms/addressForm.html",
           "projects": "examApp/forms/addressForm.html"}

FORMS = [("address", AddressForm),
         ("education", EducationForm),
         ("experience", ExperienceForm),
         ("projects", ProjectsForm)]


def prot(ProfileWizard):
    pass

class ProfileWizard(SessionWizardView):
    # form_list = [ProfileForm1,ProfileForm2,ProfileForm3,ProfileForm4]
    def get_template_names(self):
        logger.info(self.steps.current)
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):

        # do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('/examApp/profile/')


class UserUpdate(UpdateView):
    model = User
    form_class = SimpleUserUpdate
    # fields = ['first_name','last_name','email',]
    template_name = 'identityManager/user_update_form.html'
    # template_name_suffix = '_update_form'
    success_url = '/identityManager/user/'

    # def post(self, request, *args, **kwargs):
    #     return http.HttpResponseRedirect('/identityManager/')