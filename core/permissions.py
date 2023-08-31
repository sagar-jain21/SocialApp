from rest_framework.permissions import BasePermission


class IsAuthenticatedOwner(BasePermission):
    def has_permission(self, request, view):
        if "user" in request.data:
            return bool(
                request.user
                and request.user.is_authenticated
                and (int(request.data["user"]) == int(request.user.id))
            )
        return bool(request.user and request.user.is_authenticated)
