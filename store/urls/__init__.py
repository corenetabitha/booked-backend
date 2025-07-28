from django.urls import path, include

urlpatterns = [
    path('', include('store.urls.auth_urls')),
    path('admin/', include('store.urls.admin_urls')),
]
