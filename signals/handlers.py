from applicationManager.signals import application_created

__author__ = 'ozgur'

import logging
from identityManager.signals import *


# from django.core.signals import request_finished
from django.dispatch import receiver

logger= logging.getLogger("wbdap.debug")


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

@receiver(application_created)
def my_callback(sender, **kwargs):
    logger.info('\nApp create captured from identity manager')

