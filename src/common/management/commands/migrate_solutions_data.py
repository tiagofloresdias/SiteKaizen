"""
Comando para migrar dados de soluções do SQLite para PostgreSQL
"""
import sqlite3
from django.core.management.base import BaseCommand
from django.db import transaction
from solutions.models import ServiceIcon, Service, SolutionSection


class Command(BaseCommand):
    help = 'Migra dados de soluções do SQLite para PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument('--sqlite-db', type=str, default='/var/www/agenciakaizen/src/db.sqlite3',
                            help='Path to the SQLite database file.')

    def handle(self, *args, **options):
        sqlite_db_path = options['sqlite_db']
        
        try:
            # Conectar ao SQLite
            sqlite_conn = sqlite3.connect(sqlite_db_path)
            sqlite_cursor = sqlite_conn.cursor()
            
            with transaction.atomic():
                # Migrar ícones
                self.stdout.write('Migrando ícones...')
                sqlite_cursor.execute("SELECT id, name, icon_class, description FROM solutions_serviceicon")
                icons_data = sqlite_cursor.fetchall()
                
                for icon_data in icons_data:
                    icon, created = ServiceIcon.objects.get_or_create(
                        id=icon_data[0],
                        defaults={
                            'name': icon_data[1],
                            'icon_class': icon_data[2],
                            'description': icon_data[3] or ''
                        }
                    )
                    if created:
                        self.stdout.write(f'Ícone migrado: {icon.name}')
                
                # Migrar serviços
                self.stdout.write('Migrando serviços...')
                sqlite_cursor.execute("SELECT id, title, description, custom_icon_class, is_featured, \"order\" FROM solutions_service")
                services_data = sqlite_cursor.fetchall()
                
                for service_data in services_data:
                    service, created = Service.objects.get_or_create(
                        id=service_data[0],
                        defaults={
                            'title': service_data[1],
                            'description': service_data[2],
                            'custom_icon_class': service_data[3] or '',
                            'is_featured': bool(service_data[4]),
                            'order': service_data[5] or 0
                        }
                    )
                    if created:
                        self.stdout.write(f'Serviço migrado: {service.title}')
                
                # Migrar seções
                self.stdout.write('Migrando seções...')
                sqlite_cursor.execute("""
                    SELECT id, title, subtitle, background_color, \"order\", is_active, cta_text, cta_url 
                    FROM solutions_solutionsection
                """)
                sections_data = sqlite_cursor.fetchall()
                
                for section_data in sections_data:
                    section, created = SolutionSection.objects.get_or_create(
                        id=section_data[0],
                        defaults={
                            'title': section_data[1],
                            'subtitle': section_data[2],
                            'background_color': section_data[3] or 'bg-dark',
                            'order': section_data[4] or 0,
                            'is_active': bool(section_data[5]),
                            'cta_text': section_data[6] or 'Converse com um especialista',
                            'cta_url': section_data[7] or '/contato/'
                        }
                    )
                    if created:
                        self.stdout.write(f'Seção migrada: {section.title}')
                        
                        # Migrar relacionamentos serviços-seções
                        sqlite_cursor.execute("""
                            SELECT service_id FROM solutions_solutionsection_services 
                            WHERE solutionsection_id = ?
                        """, (section_data[0],))
                        service_ids = [row[0] for row in sqlite_cursor.fetchall()]
                        
                        for service_id in service_ids:
                            try:
                                service = Service.objects.get(id=service_id)
                                section.services.add(service)
                            except Service.DoesNotExist:
                                self.stdout.write(f'Aviso: Serviço com ID {service_id} não encontrado para seção {section.title}')
                
                self.stdout.write(self.style.SUCCESS('Migração de soluções concluída!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante migração: {e}'))
        finally:
            sqlite_conn.close()
