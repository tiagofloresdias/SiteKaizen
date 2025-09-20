from django.shortcuts import render
from wagtail.models import Page

class StandardPageView:
    """View para páginas padrão/evergreen"""
    
    @staticmethod
    def as_view():
        def view(request, *args, **kwargs):
            # Esta view será chamada pelo Wagtail automaticamente
            return render(request, 'pages/standard_page.html', {
                'page': request.page
            })
        return view

