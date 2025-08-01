from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import LendingViewSet, ReturnRequestView

router = DefaultRouter()
router.register(r'lendings', LendingViewSet) 

urlpatterns = router.urls + [
    path('return-request/<int:lending_id>/', ReturnRequestView.as_view(), name='return_request'),
]