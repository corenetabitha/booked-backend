
from django.urls import path
from store.views.admin_views import add_book

urlpatterns = [
    path('add-book/', add_book),
]
