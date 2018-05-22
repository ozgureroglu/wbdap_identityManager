from django.contrib.auth.models import User

from identityManager.models import IMGroup, IMUser, IMRole

__author__ = 'ozgur'

import logging
from identityManager.signals.signals import *
from applicationManager.signals.signals import application_created_signal, application_removed_signal
from django.dispatch import receiver

logger = logging.getLogger(name="identitymanager.signals.handlers")


@receiver(user_created)
def my_callback(sender, **kwargs):
    # logger.info("application_created signal receieved")
    # # print(kwargs['test'])
    # # print(kwargs['application'].active)
    # djAppC = DjangoApplicationCreator(kwargs['application'])
    #
    # djAppC.createApplication()
    pass


@receiver(user_creation_failed)
def rollback_setup(sender, **kwargs):
    # logger.warning("Application creating steps will be roll-backed")
    #
    # djAppC = DjangoApplicationCreator(kwargs['application'])
    # djAppC.rollback()
    pass


@receiver(user_removed)
def removeApplication(sender, **kwargs):
    # logger.warning("Application removing process started")
    #
    # djAppC = DjangoApplicationRemover(kwargs['application'])
    # djAppC.removeApp()
    pass


# Called when he application is created
@receiver(application_created_signal)
def application_created(sender, **kwargs):
    print('\n---------------\nApp create event captured from identity manager')
    app_name = kwargs['application'].app_name

    app_user_group = IMGroup(name=app_name + '_users')
    app_user_group.save()

    app_user_group.memberUsers.add(IMUser.objects.get(id='1'))
    app_user_group.description = app_name+" application users"
    app_user_group.save()


    app_admin_group = IMGroup(name=app_name + '_admins')
    app_admin_group.save()

    app_admin_group.memberUsers.add(IMUser.objects.get(id='1'))
    app_admin_group.description = app_name + " application admin users"
    app_admin_group.save()


    app_admin_role = IMRole(name=app_name + '_admin')
    app_admin_role.save()

    app_admin_role.assigned_groups.add(app_admin_group)
    app_admin_role.description = app_name+" admin role"
    app_admin_role.save()



# Called when the application is deleted
@receiver(application_removed_signal)
def application_removed(sender, **kwargs):
    print('\n---------------\nApp delete event captured from identity manager')
    app_name = kwargs['application'].app_name

    app_user_group = IMGroup.objects.get(name = app_name+'_users')
    app_user_group.delete()

    app_admin_group = IMGroup.objects.get(name=app_name + '_admins')
    app_admin_group.delete()

    app_admin_role = IMRole.objects.get(name=app_name + '_admin')
    app_admin_role.delete()
