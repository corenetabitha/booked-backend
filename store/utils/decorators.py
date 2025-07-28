
from functools import wraps
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication

def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        user = None
        try:
            jwt_auth = JWTAuthentication()
            user_auth_tuple = jwt_auth.authenticate(request)
            if user_auth_tuple is None:
                return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)
            user, _ = user_auth_tuple
        except Exception:
            return JsonResponse({'detail': 'Invalid token.'}, status=401)

        if user.role != 'admin':
            return JsonResponse({'detail': 'Admin access required.'}, status=403)

        request.user = user
        return view_func(request, *args, **kwargs)
    return wrapped_view
