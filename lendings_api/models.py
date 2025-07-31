from django.db import models
from users_api.models import CustomUser
from books_api.models import Book
from datetime import date, timedelta

class Lending(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lendings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    lending_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Lent', 'Lent'),
        ('Returned', 'Returned'),
        ('Overdue', 'Overdue'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        if not self.pk: 
            self.due_date = date.today() + timedelta(days=14) 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lending of '{self.book.title}' by {self.user.username} (Status: {self.status})"

    class Meta:
        ordering = ['-lending_date']
        unique_together = ('user', 'book')
 