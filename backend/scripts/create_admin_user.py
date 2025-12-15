#!/usr/bin/env python3
"""
Script para criar usuário admin inicial
Uso: python scripts/create_admin_user.py
"""
import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models.user import User
from app.core.auth import get_password_hash
from app.db import Base

def create_admin_user():
    """Cria usuário admin inicial"""
    # Criar tabelas se não existirem
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verificar se já existe admin
        admin = db.query(User).filter(User.is_admin == True).first()
        if admin:
            print(f"❌ Já existe um usuário admin: {admin.username}")
            return
        
        # Criar admin
        username = input("Digite o username do admin: ").strip()
        email = input("Digite o email do admin: ").strip()
        password = input("Digite a senha do admin: ").strip()
        full_name = input("Digite o nome completo (opcional): ").strip() or None
        
        # Verificar se username ou email já existe
        existing = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing:
            print(f"❌ Username ou email já existe!")
            return
        
        # Criar usuário
        hashed_password = get_password_hash(password)
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_admin=True,
            is_superuser=True,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✅ Usuário admin criado com sucesso!")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   ID: {admin_user.id}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar usuário: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()

