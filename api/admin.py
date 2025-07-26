# /home/corene/project-backend/backend/api/admin.py

from django.contrib import admin
from .models import Book, Genre # NEW: Import Genre

# Register your models here.
admin.site.register(Book)
admin.site.register(Genre) # NEW: Register Genre