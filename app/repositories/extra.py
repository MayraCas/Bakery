
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models import Extra
from app.schemas.extra import ExtraCreate, ExtraUpdate


class ExtraRepository:

    @staticmethod
    def create(db: Session, extra: ExtraCreate) -> Extra:
        # Convertir precio schema a tupla para PostgreSQL
        precio_tuple = None
        if extra.precio:
            precio_tuple = (
                extra.precio.retail_sale,
                extra.precio.wholesale
            )
        
        db_extra = Extra(
            nombre=extra.nombre,
            descripcion=extra.descripcion,
            imagen_url=extra.imagen_url,
            tipo_extra=extra.tipo_extra.value if extra.tipo_extra else None,
            precio=precio_tuple,
            disponible=True  
        )
        
        db.add(db_extra)
        db.commit()
        db.refresh(db_extra)
        return db_extra
    
    @staticmethod
    def get_by_id(db: Session, extra_id: int) -> Optional[Extra]:
        stmt = select(Extra).where(Extra.id == extra_id)
        return db.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Extra]:
        stmt = select(Extra).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_tipo(db: Session, tipo_extra: str) -> List[Extra]:
        stmt = select(Extra).where(Extra.tipo_extra == tipo_extra)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def update(db: Session, extra_id: int, extra_update: ExtraUpdate) -> Optional[Extra]:
        db_extra = ExtraRepository.get_by_id(db, extra_id)
        if not db_extra:
            return None
        
        # Actualizar campos uno por uno
        if extra_update.nombre is not None:
            db_extra.nombre = extra_update.nombre
        if extra_update.descripcion is not None:
            db_extra.descripcion = extra_update.descripcion
        if extra_update.imagen_url is not None:
            db_extra.imagen_url = extra_update.imagen_url
        if extra_update.tipo_extra is not None:
            db_extra.tipo_extra = extra_update.tipo_extra.value
        
        # Manejar precio especialmente
        if extra_update.precio is not None:
            precio_tuple = (
                extra_update.precio.retail_sale,
                extra_update.precio.wholesale
            )
            db_extra.precio = precio_tuple
        
        # Manejar disponible
        if extra_update.disponible is not None:
            db_extra.disponible = extra_update.disponible
        
        db.commit()
        db.refresh(db_extra)
        return db_extra
    
    @staticmethod
    def delete(db: Session, extra_id: int) -> bool:
        db_extra = ExtraRepository.get_by_id(db, extra_id)
        if not db_extra:
            return False
        
        db.delete(db_extra)
        db.commit()
        return True
