from django.contrib import admin
from .models import Case


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'category', 'is_featured', 'is_published', 'order', 'created_at')
    list_filter = ('category', 'is_featured', 'is_published', 'created_at')
    search_fields = ('title', 'client_name', 'short_description')
    list_editable = ('is_featured', 'is_published', 'order')
    ordering = ('order', '-created_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'slug', 'client_name', 'client_logo', 'category')
        }),
        ('Visual e Descrição', {
            'fields': ('hero_image', 'short_description')
        }),
        ('Storytelling', {
            'fields': ('challenge', 'solution', 'results')
        }),
        ('Métricas', {
            'fields': ('main_metric_value', 'main_metric_description')
        }),
        ('Configurações', {
            'fields': ('is_featured', 'is_published', 'order')
        }),
        ('SEO', {
            'fields': ('meta_description',)
        }),
    )