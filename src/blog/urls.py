from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('categorias/<slug:slug>/', views.blog_category, name='blog_category'),
    path('tags/<slug:slug>/', views.blog_tag, name='blog_tag'),
    path('<slug:slug>/', views.blog_post, name='blog_post'),
    path('api/', include('blog.api_urls')),
]
