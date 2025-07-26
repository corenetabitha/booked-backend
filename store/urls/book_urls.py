from django.urls import path
from .views import book_views

urlpatterns = [
    path('', book_views.list_books),
    path('add/', book_views.add_book),
]