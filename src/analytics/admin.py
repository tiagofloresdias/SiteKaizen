from django.contrib import admin
from .models import CustomEvent


@admin.register(CustomEvent)
class CustomEventAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'category', 'is_conversion', 'is_active', 'created_at']
    list_filter = ['category', 'is_conversion', 'is_active', 'created_at']
    search_fields = ['name', 'display_name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
