from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('yourapp.routes.user_routes')),  # Adjust app name
]