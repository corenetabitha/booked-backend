# api/models.py
from django.db import models # <--- Ensure this is django.db if using SQLite, or djongo if using MongoDB

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255) # Added author based on frontend need
    description = models.TextField(blank=True, null=True) # Added description
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Changed to DecimalField
    genre = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    is_available_for_purchase = models.BooleanField(default=True)
    is_available_for_lending = models.BooleanField(default=False)
    stock_count = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_added']