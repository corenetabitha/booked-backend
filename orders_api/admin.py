from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 
    readonly_fields = ('book', 'quantity', 'price_at_purchase') 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_amount', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'order_date', 'total_amount') 
    actions = ['mark_approved', 'mark_rejected', 'mark_completed']

    def mark_approved(self, request, queryset):
        queryset.update(status='Approved')
    mark_approved.short_description = "Mark selected orders as Approved"

    def mark_rejected(self, request, queryset):
        queryset.update(status='Rejected')
    mark_rejected.short_description = "Mark selected orders as Rejected"

    def mark_completed(self, request, queryset):
        queryset.update(status='Completed')
    mark_completed.short_description = "Mark selected orders as Completed"


