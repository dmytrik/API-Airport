from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Custom permission to allow read-only access
    for authenticated users,
    and full access for staff (admin) users.

    Permissions:
        - If the request method is a safe method
          (GET, HEAD, or OPTIONS) and the user is authenticated,
          the user is granted permission for read-only access.
        - Admin (staff) users are granted full access
          regardless of the request method.
    """

    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )
