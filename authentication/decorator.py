from functools import wraps

from django.contrib.auth.models import Permission, Group, User
from django.http import JsonResponse


def user_passes_test(test_func):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            return JsonResponse({
                'code': 400,
                'message': 'You are not authorized to access the endpoint.'
            })

        return _wrapped_view

    return decorator


def permission_required(perm, raise_exception=True):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        # print(user.user_permissions.all())
        user_username = User.objects.get(id=user.id)
        if Permission.objects.filter(user__username=user_username, codename__in=perms).exists():
            return True
        # In case the 403 handler should be called raise the exception
        # if raise_exception:
        #     raise PermissionDenied
        # As the last resort, show the login form
        return False

    return user_passes_test(check_perms)


