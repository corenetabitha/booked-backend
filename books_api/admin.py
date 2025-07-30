from django.contrib import admin
from .models import Book, Genre

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'genre', 'price', 'stock_count',
        'is_available_for_purchase', 'is_available_for_lending'
    )
    list_filter = ('genre', 'is_available_for_purchase', 'is_available_for_lending')
    search_fields = ('title', 'author', 'description')
   
    raw_id_fields = ('genre',)
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'description', 'image_url')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'stock_count', 'is_available_for_purchase', 'is_available_for_lending')
        }),
        ('Categorization', {
            'fields': ('genre',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) 
        }),
    )
    readonly_fields = ('created_at', 'updated_at') 

