from rest_framework.routers import DefaultRouter
from .views import BookViewSet, GenreViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = router.urls