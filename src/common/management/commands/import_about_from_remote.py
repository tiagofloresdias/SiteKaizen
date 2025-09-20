"""
Importa conteúdo da página Quem Somos do site remoto e atualiza a AboutPage
do Wagtail local. Extrai títulos e parágrafos principais e tenta capturar
uma imagem hero. Publica uma nova revisão ao final.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.files.base import ContentFile
from django.utils.text import slugify
from io import BytesIO
import re

import requests
from bs4 import BeautifulSoup


REMOTE_URL = "https://novosite.agenciakaizen.com.br/quem-somos/"


class Command(BaseCommand):
    help = "Importa conteúdo de 'Quem Somos' do site remoto e atualiza AboutPage"

    @transaction.atomic
    def handle(self, *args, **options):
        # Garante a existência da página
        from django.core.management import call_command
        call_command("ensure_about_page")

        # Buscar HTML remoto com User-Agent e fallback
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        }
        try:
            resp = requests.get(REMOTE_URL, timeout=20, headers=headers)
            resp.raise_for_status()
        except Exception:
            resp = requests.get(REMOTE_URL, timeout=25, headers=headers)
            resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # Heurísticas de extração
        def text_or_none(el):
            return el.get_text(strip=True) if el else None

        # Hero title/subtitle
        hero_title = None
        hero_subtitle = None

        h1 = soup.find("h1")
        if h1:
            hero_title = text_or_none(h1)

        # Buscar um parágrafo logo após o h1
        if h1:
            next_p = h1.find_next("p")
            if next_p:
                hero_subtitle = next_p.get_text(" ", strip=True)

        # Se não achou, fallback para meta description
        if not hero_subtitle:
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                hero_subtitle = meta_desc["content"].strip()

        # Seções por headings comuns
        def find_heading_text(contains):
            regex = re.compile(contains, re.I)
            for tag in soup.find_all(["h2", "h3", "h4"]):
                if regex.search(tag.get_text(" ", strip=True)):
                    return tag.get_text(" ", strip=True)
            return None

        def find_section_paragraph_after(heading_contains):
            regex = re.compile(heading_contains, re.I)
            for tag in soup.find_all(["h2", "h3", "h4"]):
                if regex.search(tag.get_text(" ", strip=True)):
                    # concatenar alguns parágrafos subsequentes
                    texts = []
                    for sib in tag.find_all_next(["p", "li"], limit=6):
                        text = sib.get_text(" ", strip=True)
                        if text:
                            texts.append(text)
                        if len(" ".join(texts)) > 800:
                            break
                    return "\n\n".join(texts)
            return None

        results_title = find_heading_text("Resultados|Cases|Nossos resultados") or "Resultados"
        results_subtitle = find_section_paragraph_after("Resultados|Cases|Nossos resultados") or ""

        history_title = find_heading_text("História|Nossa história|Quem somos") or "Nossa história"
        history_text_plain = find_section_paragraph_after("História|Nossa história|Quem somos") or ""

        team_title = find_heading_text("Time|Equipe|Liderança") or "Nosso time"
        team_text_plain = find_section_paragraph_after("Time|Equipe|Liderança") or ""

        # Converter textos simples em RichText mínimo (parágrafos)
        def to_richtext(paragraphs_text: str) -> str:
            if not paragraphs_text:
                return ""
            parts = [f"<p>{p}</p>" for p in paragraphs_text.split("\n\n") if p.strip()]
            return "".join(parts)

        # Tentar capturar imagem hero
        hero_image_url = None
        # Heurística: procurar img próxima do h1
        if h1:
            img = h1.find_next("img")
            if img and img.get("src"):
                hero_image_url = img["src"]

        # Normalizar URL relativa
        def absolutize(url: str | None) -> str | None:
            if not url:
                return None
            if url.startswith("http://") or url.startswith("https://"):
                return url
            return requests.compat.urljoin(REMOTE_URL, url)

        hero_image_url = absolutize(hero_image_url)

        # Atualizar modelo
        from home.models import AboutPage
        from wagtail.images import get_image_model

        about = AboutPage.objects.filter(slug="quem-somos").first()
        if not about:
            self.stdout.write(self.style.ERROR("AboutPage não encontrada."))
            return

        if hero_title:
            about.hero_title = hero_title
        if hero_subtitle:
            about.hero_subtitle = to_richtext(hero_subtitle)
        if results_title:
            about.results_title = results_title
        if results_subtitle:
            about.results_subtitle = results_subtitle
        if history_title:
            about.history_title = history_title
        if history_text_plain:
            about.history_text = to_richtext(history_text_plain)
        if team_title:
            about.team_title = team_title
        if team_text_plain:
            about.team_text = to_richtext(team_text_plain)

        # Baixar imagem hero e salvar no Wagtail Images
        if hero_image_url:
            try:
                img_resp = requests.get(hero_image_url, timeout=20)
                img_resp.raise_for_status()
                image_bytes = img_resp.content
                Image = get_image_model()
                filename = slugify(hero_title or "quem-somos-hero") + ".jpg"
                wagtail_image = Image(title=hero_title or "Quem Somos Hero")
                wagtail_image.file.save(filename, ContentFile(image_bytes), save=True)
                about.hero_image = wagtail_image
            except Exception:
                # Se falhar o download, mantém sem imagem
                pass

        # SEO básicos
        about.seo_title = about.title or "Quem Somos"
        if not getattr(about, "meta_description", ""):
            about.meta_description = (hero_subtitle or results_subtitle or "").strip()[:160]

        # Publicar
        about.save()
        about.save_revision().publish()

        self.stdout.write(self.style.SUCCESS("Conteúdo importado do site remoto e publicado."))


