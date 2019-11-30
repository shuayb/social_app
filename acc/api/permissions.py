from rest_framework import permissions


# Please note
# has_permission() is a check made before
# calling the has_object_permission().

class OwnerCanUpdateOnly(permissions.BasePermission):
    """
    Handles permissions for users.  The basic rules are
     - owner may GET, PUT, POST, DELETE
     - nobody else can access
    """
    message = "Not an owner."

    def has_object_permission(self, request, view, obj):
        # permissions.SAFE_METHODS contains a list of HTTP methods
        # that don’t write, i.e. GET, OPTION, and HEAD.

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj


class IsSuperAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
