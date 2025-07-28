from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, OrderViewSet, LendingRequestViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'lendings', LendingRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
