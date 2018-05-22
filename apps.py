from django.core.management import call_command
from django.db import connection
import logging
logger = logging.getLogger('wbdap.debug')

__author__ = 'ozgur'

from django.apps import AppConfig

class UserManagementAppConfig(AppConfig):
    name = 'identityManager'
    verbose_name = "identityManager App"
    yvar = "yvar"

    appName ='identityManager'
    verbose_name = 'identityManager'
    url = 'identityManager'
    namedUrl = 'identityManager'
    active = True
    readmeContent = "Readme file"

    # Sadece bir kere uygulama baslatildiginda calistirilmakta

    def db_table_exists(self, prefix):
        for table_name in connection.introspection.table_names():
            if prefix in table_name:
                return True
        return False

    # Sadece bir kere uygulama baslatildiginda calistirilmakta
    def ready(self):

        import identityManager.signals.handlers

        if not self.db_table_exists('identityManager_'):
            try:
                call_command('migrate', 'identityManager')
                call_command('loaddata', 'identityManager/fixtures/initial_data.json')
            except:
                logger.fatal('unable to migrate blog app ')

