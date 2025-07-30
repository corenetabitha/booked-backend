from django.contrib import admin
from .models import Lending

@admin.register(Lending)
class LendingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'book', 'lending_date', 'due_date',
        'returned_date', 'status'
    )
    list_filter = ('status', 'lending_date', 'due_date')
    search_fields = ('user__username', 'book__title', 'id')
    raw_id_fields = ('user', 'book')
    actions = ['mark_approved', 'mark_rejected', 'mark_lent', 'mark_returned', 'mark_overdue']

    def mark_approved(self, request, queryset):
        queryset.update(status='Approved')
    mark_approved.short_description = "Mark selected lendings as Approved"

    def mark_rejected(self, request, queryset):
        queryset.update(status='Rejected')
    mark_rejected.short_description = "Mark selected lendings as Rejected"

    def mark_lent(self, request, queryset):
        queryset.update(status='Lent')
    mark_lent.short_description = "Mark selected lendings as Lent (book with user)"

    def mark_returned(self, request, queryset):
        queryset.update(status='Returned', returned_date=admin.utils.timezone.now().date())
    mark_returned.short_description = "Mark selected lendings as Returned (book checked in)"

    def mark_overdue(self, request, queryset):
        queryset.update(status='Overdue')
    mark_overdue.short_description = "Mark selected lendings as Overdue"

