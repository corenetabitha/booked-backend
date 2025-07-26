from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Order(models.Model):
    user_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')  
    date = models.DateField(auto_now_add=True)


class LendingRequest(models.Model):
    user_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending') 
    date = models.DateField(auto_now_add=True)