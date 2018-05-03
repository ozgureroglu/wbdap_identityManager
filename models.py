from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Uygulamanin asil kullanicisina dogrudan bagli olan tek field bu olacak.
class IMUser(User):
    ss = models.CharField(max_length=10, blank=True)

    # def createProfile(self, user):
    #     self.user = user
    #     self.save()
    #     userProfile = UserProfile()
    #     userProfile.user = self
    #     userProfile.save()

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'IM User'
        verbose_name_plural = 'IM Users'


@admin.register(IMUser)
class IMUserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name')


# class Hider(object):
#     def __get__(self,instance,owner):
#         raise AttributeError("Hidden attribute")
#
#     def __set__(self, obj, val):
#         raise AttributeError("Hidden attribute")
#


class IMGroup(Group):
    memberGroups = models.ManyToManyField('self', blank=True, null=True, symmetrical=False, related_name='member_groups')
    memberUsers = models.ManyToManyField(IMUser, blank=True, null=True, related_name='member_users')
    description = models.CharField(max_length=200, null=False, blank=False)
    active = models.BooleanField(null=False, blank=True, default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print('saving object')
        super().save(force_insert, force_update, using, update_fields)

    # TODO: Bu sinifin asagaidaki gibi permissions'a yazmasi engellenmeli

    # def __getattribute__(self, name):
    #     if name in ("permissions"):
    #         # print("Immutable value of "+name)
    #         # return super().__getattribute__(name)
    #         raise AttributeError("%s is an immutable attribute.")
    #     else:
    #         # This should trigger the default behavior for any other
    #         # attribute name.
    #         # raise AttributeError()
    #         return super().__getattribute__(name)
    #
    # def __setattr__(self, name, value):
    #     if name in self.getAttributes():
    #         super().__setattr__(name, value)
    #     else:
    #         # How do I request the default behavior?
    #         raise AttributeError("%s is an immutable attribute.")
    #
    #
    # def __getattr__(self, name):
    #     if name in ("permissions"):
    #         print('getting permissions attribute')
    #         return super().__getattribute__(name)
    #     else:
    #         # How do I request the default behavior?
    #         super().__getattr__(self,name)


    def __str__(self):
        return self.name


@admin.register(IMGroup)
class IMGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active',)
    exclude = ('permissions',)


# class IMGroup(models.Model):
#     # group = models.OneToOneField(Group, related_name="im_group")
#     name = models.CharField(max_length=80, null=False, blank=False)
#     member = models.ManyToManyField(IMUser, blank=True, symmetrical=True)
#     group = models.ManyToManyField('self', blank=True, symmetrical=False)
#     description = models.CharField(max_length=200, null=False, blank=False)
#     active = models.BooleanField(null=False, blank=True, default=False)
#
#     def __str__(self):
#         return self.name
#
#     def get_members(self):
#         for im_group in self.group.all():
#             print(im_group.name)
#
#
# @admin.register(IMGroup)
# class IMGroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description', 'active',)


class IMRole(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    # permission = models.ManyToManyField(Permission, related_name="im_role")
    memberGroups = models.ManyToManyField(IMGroup, related_name='group_roles', blank=True)
    memberUsers = models.ManyToManyField(IMUser, related_name='user_roles', blank=True)

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
    address = models.TextField(max_length=500, null=True, blank=True)
    cellularPhone = models.TextField(max_length=500, null=True, blank=True)
    siteUrl = models.URLField(max_length=50, null=True, blank=True)
    company = models.URLField(max_length=50, null=True, blank=True)
    gender = models.NullBooleanField(blank=True)

    def __str__(self):
        return self.owner.first_name


@admin.register(IMUserProfile)
class IMUserProfileAdmin(admin.ModelAdmin):
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
    name = models.CharField(max_length=100, null=False, blank=False)
    abbreviation = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)


class Education(models.Model):
    school = models.ForeignKey(School, related_name='schoolin_educations',on_delete=models.CASCADE)
    field = models.CharField(max_length=50, null=False, blank=True)
    degree = models.ForeignKey(Degree, related_name='in_educations',on_delete=models.CASCADE)
    grade = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(4)],blank=True,null=True)
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


class RoleManager(models.Manager):
    """
    Lets us do querysets limited to families that have
    currently enrolled students, e.g.:
        Family.has_students.all()
    """

    def get_query_set(self):
        return super(RoleManager, self).get_query_set().filter(student__enrolled=True).distinct()


class Role(Group):
    notes = models.TextField(blank=True)

    # Two managers for this model - the first is default
    # (so all families appear in the admin).
    # The second is only invoked when we call
    # Family.has_students.all()
    objects = models.Manager()
    has_students = RoleManager()

    class Meta:
        verbose_name_plural = "Families"
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('notes',)
