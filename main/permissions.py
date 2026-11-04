from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Owner may do everything; an Editor may only PUT/PATCH.

    The Editor role in this project is granted through the Django
    permission ``main.change_interest`` (see ``can_update_model``), so the
    check uses ``has_perm`` instead of group membership.
    """

    message = "You do not have permission to change interests."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and request.user.has_perm("main.change_interest")
        )

