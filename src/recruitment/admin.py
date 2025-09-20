from django.contrib import admin
from .models import RecruitmentApplication, FoguetePage, RecruitmentPage


@admin.register(RecruitmentApplication)
class RecruitmentApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'desired_area', 'experience_years', 
        'education_level', 'status', 'created_at'
    ]
    list_filter = [
        'status', 'desired_area', 'education_level', 'availability',
        'crm_experience', 'social_media_experience', 'google_ads_experience',
        'created_at'
    ]
    search_fields = [
        'full_name', 'email', 'current_position', 'current_company',
        'technical_skills', 'motivation'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Dados Pessoais', {
            'fields': (
                'full_name', 'email', 'phone', 'birth_date', 'cpf', 'rg',
                'address', 'city', 'state', 'zip_code'
            )
        }),
        ('Informações Profissionais', {
            'fields': (
                'current_position', 'current_company', 'experience_years',
                'education_level', 'course_name', 'institution'
            )
        }),
        ('Candidatura', {
            'fields': (
                'desired_area', 'availability', 'technical_skills', 'languages',
                'certifications'
            )
        }),
        ('Experiência com Ferramentas', {
            'fields': (
                'crm_experience', 'social_media_experience', 'google_ads_experience',
                'facebook_ads_experience', 'analytics_experience', 'seo_experience',
                'content_creation_experience'
            )
        }),
        ('Motivação e Expectativas', {
            'fields': (
                'motivation', 'salary_expectation', 'career_goals'
            )
        }),
        ('Informações Adicionais', {
            'fields': (
                'linkedin_profile', 'portfolio_url', 'referral_source',
                'resume_file', 'cover_letter'
            )
        }),
        ('Status e Controle', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_reviewed', 'mark_as_interview', 'mark_as_approved', 'mark_as_rejected']
    
    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='em_analise')
        self.message_user(request, f'{queryset.count()} candidaturas marcadas como "Em Análise".')
    mark_as_reviewed.short_description = "Marcar como Em Análise"
    
    def mark_as_interview(self, request, queryset):
        queryset.update(status='entrevista')
        self.message_user(request, f'{queryset.count()} candidaturas marcadas para "Entrevista".')
    mark_as_interview.short_description = "Marcar para Entrevista"
    
    def mark_as_approved(self, request, queryset):
        queryset.update(status='aprovado')
        self.message_user(request, f'{queryset.count()} candidaturas marcadas como "Aprovadas".')
    mark_as_approved.short_description = "Marcar como Aprovadas"
    
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejeitado')
        self.message_user(request, f'{queryset.count()} candidaturas marcadas como "Rejeitadas".')
    mark_as_rejected.short_description = "Marcar como Rejeitadas"


# Registrar as páginas do Wagtail
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

# As páginas FoguetePage e RecruitmentPage são registradas automaticamente pelo Wagtail