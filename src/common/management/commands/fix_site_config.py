"""
Comando para corrigir configuração do site
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Corrige configuração do site para HTTPS'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Atualizar porta para 443 (HTTPS)
            cursor.execute("UPDATE wagtailcore_site SET port = 443 WHERE hostname = 'www.agenciakaizen.com.br';")
            cursor.execute("UPDATE wagtailcore_site SET port = 443 WHERE hostname = 'agenciakaizen.com.br';")
            
            # Verificar resultado
            cursor.execute("SELECT hostname, port FROM wagtailcore_site;")
            sites = cursor.fetchall()
            
            self.stdout.write('Sites atualizados:')
            for site in sites:
                self.stdout.write(f'  {site[0]}:{site[1]}')
            
            self.stdout.write(self.style.SUCCESS('Configuração do site corrigida!'))
