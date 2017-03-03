from rest_framework import permissions


class IsLogin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        token = request.GET.get("token", "")
        if token == "":
            token = request.data.get("token", "")

        if token != "" and token == obj.id.token:
            return True
        else:
            return False
