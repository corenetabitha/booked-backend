# /home/corene/project-backend/backend/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# NEW: Import GenreViewSet
from .views import BookViewSet, UserRegisterLoginViewSet, GenreViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
# NEW: Register GenreViewSet
router.register(r'genres', GenreViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', UserRegisterLoginViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/login/', UserRegisterLoginViewSet.as_view({'post': 'login'}), name='login'),
]