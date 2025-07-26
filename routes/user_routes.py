/backend/routes/user_routes.py
from django.urls import path
from .views import UserOrderHistoryView, UserLendingHistoryView

urlpatterns = [
    path('orders/', UserOrderHistoryView.as_view(), name='user-orders'),
    path('lendings/', UserLendingHistoryView.as_view(), name='user-lendings'),
]