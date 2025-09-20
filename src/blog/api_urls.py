from django.urls import path
from . import api_views

app_name = 'blog_api'

urlpatterns = [
    path('load-more/', api_views.load_more_posts, name='load_more_posts'),
    path('search/', api_views.search_posts, name='search_posts'),
    path('categories/', api_views.get_categories, name='get_categories'),
]