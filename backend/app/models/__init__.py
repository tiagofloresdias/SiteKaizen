"""
Modelos SQLAlchemy - Importação centralizada
"""
from app.models.article import Article, ArticleCategory, Tag
from app.models.portfolio import PortfolioItem, PortfolioCategory, PortfolioGalleryImage
from app.models.page import StandardPage
from app.models.contact import Newsletter, ContactMessage
from app.models.lead import Lead, Touchpoint, UTMParameters
from app.models.case import Case
from app.models.company import Company, CompanyCategory, CompanyFeature
from app.models.location import Location

# Importar todos os modelos para que o Alembic possa detectá-los
__all__ = [
    # Blog
    "Article",
    "ArticleCategory",
    "Tag",
    # Portfolio
    "PortfolioItem",
    "PortfolioCategory",
    "PortfolioGalleryImage",
    # Pages
    "StandardPage",
    # Contact
    "Newsletter",
    "ContactMessage",
    # Leads
    "Lead",
    "Touchpoint",
    "UTMParameters",
    # Cases
    "Case",
    # Companies
    "Company",
    "CompanyCategory",
    "CompanyFeature",
    # Locations
    "Location",
]
