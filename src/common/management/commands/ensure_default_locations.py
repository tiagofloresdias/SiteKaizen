from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Garante localizações padrão (Porto Alegre, Curitiba, São Paulo) cadastradas como snippets Location"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        try:
            from companies.models import Location

            defaults = [
                dict(
                    name="Agência Kaizen",
                    city="Porto Alegre",
                    state="RS",
                    address="Av. Praia de Belas, 1212 - 11º Andar - Praia de Belas",
                    postal_code="90110-904",
                    country="BR",
                    phone="0800-550-8000",
                    email="contato@agenciakaizen.com.br",
                    latitude=-30.0346,
                    longitude=-51.2177,
                    maps_url="https://maps.google.com/?q=Av.+Praia+de+Belas,+1212,+Porto+Alegre",
                    opening_hours="Mo-Fr 08:00-18:00",
                    is_main_office=True,
                    is_active=True,
                    order=1,
                ),
                dict(
                    name="Agência Kaizen",
                    city="Curitiba",
                    state="PR",
                    address="Rua Comendador Araújo, 499 - 10º andar, Centro 80",
                    postal_code="80420-000",
                    country="BR",
                    phone="0800-550-8000",
                    email="contato@agenciakaizen.com.br",
                    latitude=-25.4284,
                    longitude=-49.2733,
                    maps_url="https://maps.google.com/?q=Rua+Comendador+Araújo,+499,+Curitiba",
                    opening_hours="Mo-Fr 08:00-18:00",
                    is_main_office=False,
                    is_active=True,
                    order=2,
                ),
                dict(
                    name="Agência Kaizen",
                    city="São Paulo",
                    state="SP",
                    address="Rua Olimpíadas, 205 - Vila Olímpia",
                    postal_code="04551-000",
                    country="BR",
                    phone="0800-550-8000",
                    email="contato@agenciakaizen.com.br",
                    latitude=-23.5975,
                    longitude=-46.6876,
                    maps_url="https://maps.google.com/?q=Rua+Olimpíadas,+205,+São+Paulo",
                    opening_hours="Mo-Fr 08:00-18:00",
                    is_main_office=False,
                    is_active=True,
                    order=3,
                ),
            ]

            created, updated = 0, 0
            for data in defaults:
                obj, was_created = Location.objects.update_or_create(
                    city=data["city"], state=data["state"], defaults=data
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

            self.stdout.write(self.style.SUCCESS(f"Localizações: {created} criadas, {updated} atualizadas."))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Falha ao garantir localizações padrão: {exc}"))


