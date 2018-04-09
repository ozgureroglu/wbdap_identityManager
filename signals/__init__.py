__author__ = 'ozgur'


import django.dispatch

user_created = django.dispatch.Signal(providing_args=["test","application"])
user_removed = django.dispatch.Signal(providing_args=["test","application"])
user_creation_failed = django.dispatch.Signal(providing_args=["test","application"])