from crispy_forms.layout import ButtonHolder, Fieldset, Submit, Reset


from identityManager.models import IMRole, IMGroup, IMUser


__author__ = 'ozgur'

from crispy_forms.helper import FormHelper,Layout

from django.contrib.auth.models import User
from django.forms import *
from django import forms


class AddUserForm(ModelForm):
    # username = forms.CharField()
    # is_active = forms.BooleanField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = "/identityManager/user/add/"
    helper.form_id = "form-id-addIdentityObject"
    # helper.add_input(Button('createUser', 'Create User',css_class='btn-primary'))

    class Meta:
        model = IMUser
        # widgets = {
        #     'username': TextInput(attrs={'class':'form-control input-md','required':''}),
        # }
        # exclude = ('is_staff', 'last_login', 'date_joined', 'groups', 'user_permissions')
        fields = ('username','password','first_name','last_name','email',)

class AddGroupForm(ModelForm):
    # username = forms.CharField()
    # is_active = forms.BooleanField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = "/identityManager/imgroup/add/"
    helper.form_id = "form-id-addIdentityObject"
    # helper.add_input(Button('createUser', 'Create User',css_class='btn-primary'))


    class Meta:
        model = IMGroup
        # widgets = {
        #     'username': TextInput(attrs={'class':'form-control input-md','required':''}),
        # }
        # exclude = ('is_staff', 'last_login', 'date_joined', 'groups', 'user_permissions')
        fields = ('name','description',)



class AddRoleForm(ModelForm):
    # username = forms.CharField()
    # is_active = forms.BooleanField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = "/identityManager/role/add/"
    helper.form_id = "form-id-addIdentityObject"
    # helper.add_input(Button('createUser', 'Create User',css_class='btn-primary'))


    class Meta:
        model = IMRole
        # widgets = {
        #     'username': TextInput(attrs={'class':'form-control input-md','required':''}),
        # }
        # exclude = ('is_staff', 'last_login', 'date_joined', 'groups', 'user_permissions')
        fields = ('roleName','description')




class AddressForm(forms.Form):
    username = forms.CharField()
    is_active = forms.BooleanField()

    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions')



class EducationForm(forms.Form):
    username = forms.CharField()
    is_active = forms.BooleanField()

    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions')


class ExperienceForm(forms.Form):
    username = forms.CharField()
    is_active = forms.BooleanField()

    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions')


class ProjectsForm(forms.Form):
    username = forms.CharField()
    is_active = forms.BooleanField()

    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions')


class SimpleUserUpdate(ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(('Edit User Data'), 'first_name', 'last_name', 'email'),
            ButtonHolder(
                Submit('save', ('Submit'), css_class='btn btn-primary '),
                Reset('reset', ('Cancel'), css_class='btn')
            )
        )

        # self.helper.add_input(Submit('submit', 'Submit'))
        super(SimpleUserUpdate, self).__init__(*args, **kwargs)

    class Meta:
        model = IMUser
        fields = ['first_name', 'last_name', 'email']


