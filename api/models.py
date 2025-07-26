
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    stock_count = models.IntegerField(default=0)
    is_available_for_purchase = models.BooleanField(default=True)
    is_available_for_lending = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title