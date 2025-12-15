"""
Modelos SQLAlchemy para Blog - Migrado de Django/Wagtail
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, Date, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db import Base

# Tabela de associação Many-to-Many para tags
article_tags = Table(
    'article_tags',
    Base.metadata,
    Column('article_id', UUID(as_uuid=True), ForeignKey('articles.id'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True),
)

# Tabela de associação Many-to-Many para categorias (artigos podem ter múltiplas categorias)
article_categories_assoc = Table(
    'article_categories_assoc',
    Base.metadata,
    Column('article_id', UUID(as_uuid=True), ForeignKey('articles.id'), primary_key=True),
    Column('category_id', UUID(as_uuid=True), ForeignKey('article_categories.id'), primary_key=True),
)


class Tag(Base):
    """Tags para artigos do blog"""
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    articles = relationship("Article", secondary=article_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag {self.name}>"


# ArticleCategory e Article já estão definidos em app.models.article
# Não duplicar aqui - usar os modelos de article.py
# As tabelas de associação (article_tags, article_categories_assoc) são usadas pelos modelos de article.py

