from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, BookViewSet

router = DefaultRouter()
router.register('items', CartItemViewSet)
router.register('books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
