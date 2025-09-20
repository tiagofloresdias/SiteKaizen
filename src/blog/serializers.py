"""
Serializers para API REST do Blog
"""
from rest_framework import serializers
from .models import BlogPage, BlogIndexPage


class BlogPageSerializer(serializers.ModelSerializer):
    """
    Serializer para posts do blog
    """
    url = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPage
        fields = [
            'id', 'title', 'slug', 'intro', 'body', 'date', 
            'url', 'author', 'first_published_at', 'last_published_at',
            'live', 'seo_title', 'search_description'
        ]
        read_only_fields = ['id', 'slug', 'first_published_at', 'last_published_at']
    
    def get_url(self, obj):
        """Retorna a URL completa do post"""
        if hasattr(self.context.get('request'), 'build_absolute_uri'):
            return obj.get_url(request=self.context['request'])
        return f"/blog/{obj.slug}/"
    
    def get_author(self, obj):
        """Retorna informações do autor"""
        if obj.owner:
            return {
                'id': obj.owner.id,
                'username': obj.owner.username,
                'first_name': obj.owner.first_name,
                'last_name': obj.owner.last_name,
            }
        return None


class BlogPageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de posts do blog
    """
    class Meta:
        model = BlogPage
        fields = [
            'title', 'intro', 'body', 'date', 'seo_title', 
            'search_description', 'live'
        ]
    
    def create(self, validated_data):
        """Cria um novo post do blog"""
        # Busca a página índice do blog
        blog_index = BlogIndexPage.objects.first()
        if not blog_index:
            raise serializers.ValidationError("Blog index page not found")
        
        # Cria o post como filho da página índice
        post = BlogPage(
            parent=blog_index,
            **validated_data
        )
        post.save()
        return post


class BlogIndexSerializer(serializers.ModelSerializer):
    """
    Serializer para a página índice do blog
    """
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogIndexPage
        fields = ['id', 'title', 'slug', 'intro', 'posts_count', 'url']
    
    def get_posts_count(self, obj):
        """Retorna o número de posts publicados"""
        return obj.get_children().live().count()
    
    def get_url(self, obj):
        """Retorna a URL completa da página"""
        if hasattr(self.context.get('request'), 'build_absolute_uri'):
            return obj.get_url(request=self.context['request'])
        return "/blog/"
