from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """
    Custom permission for Projects:
    - Safe methods (GET, HEAD, OPTIONS) allowed for anyone.
    - Write methods (POST, PUT, PATCH, DELETE) only allowed for superuser.
    """
    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or bool(request.user and request.user.is_superuser)
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Custom permission for Portfolio Assignment Section (Interest):
    - Visitors (anonymous): Read-only (GET, HEAD, OPTIONS).
    - Regular users: Read-only for list/detail.
    - Editor (Group 'Editor' or perm 'change_interest'): Can read and update (PUT/PATCH),
      but cannot create (POST) or delete (DELETE).
    - Superuser (Owner): Full permissions (create, read, update, delete).
    """
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and (
                request.user.groups.filter(name="Editor").exists()
                or request.user.has_perm("main.change_interest")
            )
        )
