from decimal import Decimal

from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Uygulamanin asil kullanicisina dogrudan bagli olan tek field bu olacak.
# Dolayisi ile bu alanin dumpi her alindiginda user listesi dump'ida alinmalidir.
class IMUser(User):
    ss = models.CharField(max_length=10, blank=True)
    generated = models.BooleanField(null=False, blank=True, default=False)

    def __str__(self):
        return self.first_name

    def __unicode__(self):
        return self.first_name

    class Meta(User.Meta):
        verbose_name = 'IM User'
        verbose_name_plural = 'IM Users'


@admin.register(IMUser)
class IMUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class IMGroup(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    # A group may be the member of another group, then all users of it will be the member of new group
    memberGroups = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='member_groups')
    memberUsers = models.ManyToManyField(IMUser, blank=True, related_name='member_users')
    description = models.CharField(max_length=200, null=False, blank=False)
    active = models.BooleanField(null=False, blank=True, default=False)
    permissions = None

    def _get_descendent_groups(self):
        """
        As the relations of groups and subgroups forms a graph we will use dfs or bfs to get all subgroups :
        following is the DFS

        :return: set of descendent groups
        """
        visited = set()
        stack = [self]

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(set(vertex.memberGroups.all()) - visited)
        return visited

    def _get_descendent_users(self):
        """
        Returns all of the users from the descendents
        :return: set of users
        """
        users = set()

        dgroups = self._get_descendent_groups()
        for dg in dgroups:
            for u in dg.memberUsers.all():
                users.add(u)
        return users

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print('saving object')
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


@admin.register(IMGroup)
class IMGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active',)


class IMRole(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    # permission = models.ManyToManyField(Permission, related_name="im_role")
    assigned_groups = models.ManyToManyField(IMGroup, related_name='roles', blank=True)
    assigned_users = models.ManyToManyField(IMUser, related_name='roles', blank=True)
    permissions = models.ManyToManyField(Permission, verbose_name=('permissions'), blank=True, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'IM Role'
        verbose_name_plural = 'IM Roles'


@admin.register(IMRole)
class IMRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class IMUserProfile(models.Model):
    # Bir user olusturuldugunda profili olusmaz
    owner = models.OneToOneField(IMUser, related_name='user_profile', on_delete=models.CASCADE)
    jobTitle = models.CharField(max_length=25, null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    aboutMe = models.TextField(max_length=500, null=True, blank=True)
    # address = models.TextField(max_length=500, null=True, blank=True)
    cellularPhone = models.TextField(max_length=500, null=True, blank=True)
    siteUrl = models.URLField(max_length=50, null=True, blank=True)
    company = models.URLField(max_length=50, null=True, blank=True)
    gender = models.NullBooleanField(blank=True)

    def __str__(self):
        return self.owner.first_name


@admin.register(IMUserProfile)
class IMUserProfileAdmin(admin.ModelAdmin):
    list_display = ('owner',)



class IMUserEmailAddresses(models.Model):
    # Bir user olusturuldugunda profili olusmaz
    owner = models.OneToOneField(IMUser, related_name='registered_user_email_addresses', on_delete=models.CASCADE)
    email_username = models.CharField(max_length=50, null=True, blank=True)
    email_password = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.owner.first_name


@admin.register(IMUserEmailAddresses)
class IMUserEmailAddressesAdmin(admin.ModelAdmin):
    list_display = ('owner',)





class Degree(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    abbreviation = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')


class School(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    abbreviation = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)


class Address(models.Model):
    name = models.CharField("Full name", max_length=1024, default='home address' )
    address1 = models.CharField("Address line 1", max_length=1024, default='address1')
    address2 = models.CharField("Address line 2", max_length=1024, default='address2')
    zip_code = models.CharField("ZIP / Postal code", max_length=12, default='0000')
    city = models.CharField("City", max_length=1024,default='ankara')
    country = models.CharField("Country", max_length=20, default='turkey')
    profile = models.ForeignKey(IMUserProfile, on_delete=models.CASCADE, )

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"


    def __str__(self):
        return self.profile.name + '_address'

    def __unicode__(self):
        return self.profile.name + '_address'


class Education(models.Model):
    school = models.ForeignKey(School, related_name='schoolin_educations', on_delete=models.CASCADE)
    field = models.CharField(max_length=50, null=False, blank=True)
    degree = models.ForeignKey(Degree, related_name='in_educations', on_delete=models.CASCADE)
    grade = models.DecimalField(validators=[MinValueValidator(0.01), MaxValueValidator(4.00)], blank=True, null=True,
                                max_digits=3, decimal_places=2)
    startDate = models.DateField(null=True)
    finishDate = models.DateField(null=True)
    activities = models.TextField(max_length=250, null=True, blank=True)
    description = models.TextField(max_length=250, null=True, blank=True)
    profile = models.ForeignKey(IMUserProfile, on_delete=models.CASCADE, )

    def __str__(self):
        return self.school.name

    def __unicode__(self):
        return self.school.name


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        'school',
        'field',
        'profile',
    )


class WorkExperience(models.Model):
    TITLE_CHOICES = (
        ('Other', 'Other'),
        ('SOFTWARE_ENGINEER', 'Software Engineer'),
        ('SOFTWARE_TEST_ENGINEER', 'Software Test Engineer'),
        ('SOFTWARE_ARCHITECT', 'Software Architect'),
        ('SOFTWARE_DEVELOPER', 'Software Developer'),
        ('BACHELOR_SCIENCE', 'Bachelor of Science (B.S.)'),
    )
    company = models.CharField(max_length=60, null=False, blank=False)
    sector = models.CharField(max_length=60, null=False, blank=False)
    location = models.CharField(max_length=60, null=False, blank=False)
    title = models.CharField(max_length=50, choices=TITLE_CHOICES, default=TITLE_CHOICES[0])
    technology = models.TextField(max_length=500, null=False, blank=True)
    startDate = models.DateField(null=True)
    finishDate = models.DateField(null=True)
    description = models.TextField(max_length=250, null=True, blank=True)
    profile = models.ForeignKey(IMUserProfile, on_delete=models.CASCADE, )


@admin.register(WorkExperience)
class WorkExperienceRecordAdmin(admin.ModelAdmin):
    list_display = ('company', 'sector', 'location', 'title', 'startDate', 'finishDate', 'description', 'profile',)


class CompletedProject(models.Model):
    user = models.ManyToManyField(IMUser, related_name='projects')
    pname = models.CharField(max_length=30, null=False, blank=False)
    company = models.CharField(max_length=30, null=False, blank=False)


# Decorator icin alternatif
# admin.site.register(ExtendedUserData, UserManagementAdmin)

@admin.register(CompletedProject)
class CompletedProjectAdmin(admin.ModelAdmin):
    pass
