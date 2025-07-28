from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from store.views.auth_views import (
    RegisterView,
    CustomTokenObtainPairView,
    MeView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
]
