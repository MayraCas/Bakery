from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models import Postre
from app.schemas.postre import PostreCreate, PostreUpdate


class PostreRepository:

    @staticmethod
    def create(db: Session, postre: PostreCreate) -> Postre:
        precio_tuple = None
        if postre.precio:
            precio_tuple = (
                postre.precio.small,
                postre.precio.medium,
                postre.precio.big
            )

        db_postre = Postre(
            nombre=postre.nombre,
            descripcion=postre.descripcion,
            imagen_url=postre.imagen_url,
            tipo_postre=postre.tipo_postre.value if postre.tipo_postre else None,
            precio=precio_tuple,
            disponible=(True, True, True),  # Todos los tamaños disponibles por defecto
            ingredientes=postre.ingredientes,
            es_dulce=postre.es_dulce
        )
        
        db.add(db_postre)
        db.commit()
        db.refresh(db_postre)
        return db_postre
    
    @staticmethod
    def get_by_id(db: Session, postre_id: int) -> Optional[Postre]:
        stmt = select(Postre).where(Postre.id == postre_id)
        return db.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Postre]:
        stmt = select(Postre).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_tipo(db: Session, tipo_postre: str) -> List[Postre]:
        stmt = select(Postre).where(Postre.tipo_postre == tipo_postre)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def update(db: Session, postre_id: int, postre_update: PostreUpdate) -> Optional[Postre]:
        db_postre = PostreRepository.get_by_id(db, postre_id)
        if not db_postre:
            return None
        
        if postre_update.nombre is not None:
            db_postre.nombre = postre_update.nombre
        if postre_update.descripcion is not None:
            db_postre.descripcion = postre_update.descripcion
        if postre_update.imagen_url is not None:
            db_postre.imagen_url = postre_update.imagen_url
        if postre_update.tipo_postre is not None:
            db_postre.tipo_postre = postre_update.tipo_postre.value
        if postre_update.ingredientes is not None:
            db_postre.ingredientes = postre_update.ingredientes
        if postre_update.es_dulce is not None:
            db_postre.es_dulce = postre_update.es_dulce
        
        if postre_update.precio is not None:
            precio_tuple = (
                postre_update.precio.small,
                postre_update.precio.medium,
                postre_update.precio.big
            )
            db_postre.precio = precio_tuple
        
        if postre_update.disponible is not None:
            disponible_tuple = (
                postre_update.disponible.small,
                postre_update.disponible.medium,
                postre_update.disponible.big
            )
            db_postre.disponible = disponible_tuple
        
        db.commit()
        db.refresh(db_postre)
        return db_postre
    
    @staticmethod
    def delete(db: Session, postre_id: int) -> bool:
        db_postre = PostreRepository.get_by_id(db, postre_id)
        if not db_postre:
            return False
        
        db.delete(db_postre)
        db.commit()
        return True
