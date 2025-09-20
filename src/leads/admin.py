from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'phone', 'status', 'monthly_revenue', 
        'business_area', 'created_at', 'confirmation_email_sent'
    ]
    list_filter = [
        'status', 'monthly_revenue', 'business_area', 
        'confirmation_email_sent', 'created_at'
    ]
    search_fields = ['name', 'email', 'phone', 'main_challenge']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Dados Básicos', {
            'fields': ('name', 'email', 'phone', 'status')
        }),
        ('Informações do Negócio', {
            'fields': ('monthly_revenue', 'business_area', 'main_challenge', 'website_social')
        }),
        ('Agendamento', {
            'fields': ('calendly_event_id', 'scheduled_date', 'confirmation_email_sent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
