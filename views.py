import logging
import os
import random

import simplejson
from django import http
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import resolve, reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import UpdateView
from faker import Faker
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK

from applicationManager.models import Application
from .forms import *
from .models import IMUser, IMGroup, IMRole, IMUserProfile, School, Degree

#Get an instance of the logger: Name should be the name of the logger in custom_settings LOGGING field

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
    paginator = Paginator(user_list, 30)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)


    #permissions test
    # u = IMUser.objects.get(id='2')
    #
    # perms = u.get_all_permissions()
    # print(perms)


    # return render(request,
    #     'identityManager/index.html',{}
    # )

    return render(request,
        'identityManager/imuser.html',{}
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
def generate_user_data(request):
    # with open("bin/dataGenerator/names") as names:
        import string
        from random import randint
        from random import choice

        for x in range(1, 5):
            with open(os.path.join(settings.SITE_ROOT,'bin/dataGenerator/names')) as names:
                with open(os.path.join(settings.SITE_ROOT, 'bin/dataGenerator/surnames')) as surnames:
                    name = random.choice(names.readlines()).strip('\n')
                    surname = random.choice(surnames.readlines()).strip('\n')
                    print(name)
                    print(surname)

                    # min_char = 3
                    # max_char = 14
                    # allchar = string.ascii_letters + string.digits

                    # name = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
                    # surname = "".join(choice(allchar) for x in range(randint(min_char, max_char)))

                    user = IMUser()
                    user.username = name[0].lower() + surname.lower()
                    print(user.username)
                    user.email = user.username + '@wbdap.test.com'
                    print(user.email)
                    user.first_name = name
                    user.last_name = surname
                    user.password = surname
                    user.is_superuser = False
                    user.dummy = True
                    user.save()
        return redirect('identityManager:imUser')


def delete_generated_user_data(request):
    IMUser.objects.filter(dummy=True).delete()
    return redirect('identityManager:imUser')

@login_required()
def generate_group_data(request):
    imgroups = IMGroup.objects.all()


@login_required()
def generate_role_data(request):
    imgroups = IMGroup.objects.all()




@login_required()
def imGroup(request):
    imgroups = IMGroup.objects.all()

    #
    # root = IMGroup.objects.get(name='G1')
    # print(root._get_descendent_groups())
    #
    # print(root._get_descendent_users())
    #

    return render(request,
        'identityManager/imgroup.html', {'imgroups':imgroups}
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
                  {'imgroup': imgroup,
                   })


@login_required()
def imRole_home(request, pk):
    imrole = IMRole.objects.get(id=pk)
    return render(request, 'identityManager/imrole_home.html',
                  {'imrole':imrole, })


@login_required()
def addMemberUser(request, pk):

    if request.method=='POST':

        imgroup = IMGroup.objects.get(id=pk)

        users = request.POST['users']

        user_list = str(users).strip(' ').strip(',')
        user_list = user_list.split(',')

        for user in user_list:
            user_data=(user.strip()).split(' ')
            if user_data.__len__() == 2:
                imgroup.memberUsers.add(IMUser.objects.get(first_name=user_data[0], last_name=user_data[1]))
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



def cleandefs(request):
    #TODO: Find a decoupled solution
    for app in Application.objects.all():
        print(app.app_name)
        IMRole.objects.filter(name=app.app_name+'_app_admin').delete()
        IMRole.objects.filter(name=app.app_name + '_app_user').delete()

        IMGroup.objects.filter(name=app.app_name + '_app_admins').delete()
        IMGroup.objects.filter(name=app.app_name + '_app_users').delete()

    return redirect('identityManager:imUser')


def gendefs(request):
    #TODO: Find a decoupled solution
    for app in Application.objects.all():
        print(app.app_name)

        adm_grp, st = IMGroup.objects.get_or_create(name=app.app_name + '_app_admins',
                                     description='Admin group of ' + app.app_name + ' application', active=True )
        adm_grp.memberUsers.add(IMUser.objects.get(username='ake'))

        user_grp, st = IMGroup.objects.get_or_create(name=app.app_name + '_app_users',
                                                    description='User group of ' + app.app_name + ' application',
                                                    active=True)
        user_grp.memberUsers.add(IMUser.objects.get(username='ozge'))
        user_grp.memberGroups.add(adm_grp)

        role, success = IMRole.objects.get_or_create(name=app.app_name+'_app_admin', description='A role with full privileges on '+app.app_name+' application')
        role.assigned_users.add(IMUser.objects.get(username='ozgur'))
        role.assigned_groups.add(user_grp)

        for x in Permission.objects.filter(content_type__app_label=app.app_name):
            role.permissions.add(x)

        role, success = IMRole.objects.get_or_create(name=app.app_name + '_app_user', description='A role with least privileges on '+app.app_name+' application')
        role.assigned_users.add(IMUser.objects.get(username='ozgur'))

        for x in Permission.objects.filter(content_type__app_label=app.app_name, content_type__permission__codename__contains='read'):
            role.permissions.add(x)

        role.assigned_groups.add(user_grp)

    return redirect('identityManager:imRole')

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
        'identityManager/imrole.html', {'imroles':imroles}
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
@require_http_methods(['POST'])
def changePassword(request):
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash

    if request.method == 'POST':
        print(request.POST)
        user = User.objects.get(id = request.POST['user_id'])
        passwd = request.POST['passwd']

        try:
            user.set_password(passwd)
            user.save()
            update_session_auth_hash(request, user)  # Important!
            message = 'Your password was successfully updated!'
            data = {'status': 'true', 'message': message}
            return JsonResponse(data, status=HTTP_200_OK)
        except Exception as e:
            data = {'status': 'false', 'message': e}
            return JsonResponse(data, status=HTTP_500_INTERNAL_SERVER_ERROR)


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
def dashboard(request):

    print(get_current_site(request))
    if request.user.is_authenticated:
        loggedInUser = request.user

        variables = {
            'username': loggedInUser.username,
            'users': IMUser.objects.count(),
            'groups': IMGroup.objects.count(),
            'roles': IMRole.objects.count(),
        }

        return render(request, 'identityManager/dashboard.html', variables)
    else:
        return render(request, 'login')

# TODO : Profillerin gorunmesi icin login gerekli olmayabilir: ornegin Linkedin public profile secenegi var.


def fillprofile(profile: IMUserProfile):
    """
    Generate Fake Profile Data
    """
    faker = Faker()

    profile.aboutMe = faker.text()
    profile.cellularPhone = faker.phone_number()
    # profile.company = faker.company()
    profile.gender = random.choice([True, False, None])
    profile.dateOfBirth = faker.date()
    # profile.jobTitle = faker.job()
    profile.siteUrl = faker.domain_name()
    print(profile)

    for i in range(3):
        address = Address()
        address.profile = profile
        address.default =True
        address.name = random.choice(['home','work','school'])
        address.address1 = faker.street_address()
        address.address2 = None
        address.zip_code = faker.postcode()
        address.city = faker.city()
        address.country = faker.country()
        address.save()

    for i in range(4):
        wexp = WorkExperience()
        wexp.profile = profile
        wexp.company = faker.company()
        wexp.sector = faker.word()
        wexp.location = faker.city()
        wexp.title = faker.job()
        wexp.technology = faker.text()
        wexp.startDate = faker.date()
        wexp.finishDate = faker.date()
        wexp.description = faker.text()
        wexp.save()

    for i in range(2):
        ed = Education()
        ed.profile = profile
        with open(os.path.join(settings.SITE_ROOT, 'bin/dataGenerator/uni_en')) as names:
            sch = School()
            sch.name = random.choice(names.readlines()).strip('\n')
            sch.abbreviation = sch.name[0:5].replace(' ','')
            sch.country = faker.country()
            sch.description = faker.text()
            sch.save()
            ed.school = sch

        with open(os.path.join(settings.SITE_ROOT, 'bin/dataGenerator/degrees')) as names:
            deg = Degree()
            deg.name = random.choice(names.readlines()).strip('\n')
            deg.abbreviation = deg.name[0:4].replace(' ','')
            deg.save()
            ed.degree = deg
            ed.field = ed.degree.name

        ed.grade = random.uniform(0.0,4.0)
        ed.startDate = faker.date()
        ed.finishDate = faker.date()
        ed.activities = random.choice(['ski','painting','football','baseball','riding','stamp collection'])
        ed.description = faker.text()
        ed.save()


    return profile



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

        # Eger url'e herhangi bir pk degeri gecmemisse kullanicinin kendi sayfasina donelim.
        # Bu ancak kullanici profile sayfasina manuel olarak erismeye calisiyorsa olacaktir.
        if(pk is None):
            pk = requestingUser.id

        # print("PK of the user is "+ str(pk))
        try:
            profile_owner = IMUser.objects.get(id=pk)
        except Exception as e:
            msg = "Requested user profile does not exist"
            logger.warning(msg)
            messages.add_message(request, messages.ERROR, msg)
            raise Http404(msg)
            # return render(request, 'identityManager/dashboard.html')


        profile, created = IMUserProfile.objects.get_or_create(owner_id=pk)

        print("created :"+str(created))
        if created and profile_owner.dummy :
            profile = fillprofile(profile)
            profile.save()
        educationalRec = profile.education_set.all()
        workExperienceRec = profile.workexperience_set.all()

        variables =  {
            'username': requestingUser.username,

            'profile': profile,
            'profileOwner': profile_owner,
            'educationalRec': educationalRec,
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

FORMS = [("address", AddressForm),
         ("education", EducationForm),
         ("experience", ExperienceForm),
         ("projects", CompletedProjectsForm)]


TEMPLATES = {"address": "identityManager/forms/wizard_form.html",
           "education": "identityManager/forms/wizard_form.html",
           "experience": "identityManager/forms/wizard_form.html",
           "projects": "identityManager/forms/wizard_form.html"}


class ProfileWizard(SessionWizardView):
    # form_list = [ProfileForm1,ProfileForm2,ProfileForm3,ProfileForm4]
    def get_template_names(self):
        logger.info(self.steps.current)
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        print(kwargs['pk'])
        # do_something_with_the_form_data(form_list)
        return HttpResponseRedirect(reverse('identityManager:profileView'))

class UserUpdate(UpdateView):
    model = User
    form_class = SimpleUserUpdate
    # fields = ['first_name','last_name','email',]
    template_name = 'identityManager/user_update_form.html'
    # template_name_suffix = '_update_form'
    success_url = '/identityManager/user/'

    # def post(self, request, *args, **kwargs):
    #     return http.HttpResponseRedirect('/identityManager/')