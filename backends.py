from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class IdentityManagerAuthBackend(ModelBackend):
    """
    This will only overwrite the permission related methods of ModelBackend with Identity manager Roles based Permissions
    """
    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = set()
            user_obj._perm_cache.update(self.get_user_permissions(user_obj))
            user_obj._perm_cache.update(self.get_group_permissions(user_obj))
            user_obj._perm_cache.update(self.get_role_permissions(user_obj))
        return user_obj._perm_cache

    def get_role_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from the
        groups they belong.
        """
        return self._get_permissions(user_obj, obj, 'role')


    def _get_permissions(self, user_obj, obj, from_name):
        """
        Return the permissions of `user_obj` from `from_name`. `from_name` can
        be either "group" or "user" to return permissions from
        `_get_group_permissions` or `_get_user_permissions` respectively.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = '_%s_perm_cache' % from_name
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = getattr(self, '_get_%s_permissions' % from_name)(user_obj)
            perms = perms.values_list('content_type__app_label', 'codename').order_by()
            setattr(user_obj, perm_cache_name, {"%s.%s" % (ct, name) for ct, name in perms})
        return getattr(user_obj, perm_cache_name)


    def _get_role_permissions(self, user_obj):
        print('custom backend-----------------')

        print(user_obj._meta.get_fields(include_parents=True, include_hidden=True))
        user_roles_field = user_obj._meta.get_field('roles')
        print(user_roles_field.name)
        print(user_roles_field.get_internal_type())
        print('user role field '+str(user_roles_field))

        print(Permission.objects.filter(**{'imrole__assigned_users': user_obj}))
        return Permission.objects.filter(**{'imrole__assigned_users': user_obj})