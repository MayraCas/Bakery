"""
Repository para Bebida (hereda de Producto)
CRUD para la tabla bebida respetando la herencia
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models import Bebida
from app.schemas.bebida import BebidaCreate, BebidaUpdate


class BebidaRepository:
    """Repository para operaciones CRUD en Bebida"""
    
    @staticmethod
    def create(db: Session, bebida: BebidaCreate) -> Bebida:
        """
        Crear una nueva bebida.
        La inserción en la tabla hija automáticamente crea el registro en producto (herencia).
        """
        # Convertir precio schema a tupla para PostgreSQL
        precio_tuple = None
        if bebida.precio:
            precio_tuple = (
                bebida.precio.small,
                bebida.precio.medium,
                bebida.precio.big
            )
        
        # Crear el objeto directamente desde los atributos del schema
        db_bebida = Bebida(
            nombre=bebida.nombre,
            descripcion=bebida.descripcion,
            imagen_url=bebida.imagen_url,
            tipo_bebida=bebida.tipo_bebida.value if bebida.tipo_bebida else None,
            precio=precio_tuple,
            disponible=(True, True, True),  # Todos los tamaños disponibles por defecto
            ingredientes=bebida.ingredientes,
            es_fria=bebida.es_fria
        )
        
        db.add(db_bebida)
        db.commit()
        db.refresh(db_bebida)
        return db_bebida
    
    @staticmethod
    def get_by_id(db: Session, bebida_id: int) -> Optional[Bebida]:
        """Obtener bebida por ID"""
        stmt = select(Bebida).where(Bebida.id == bebida_id)
        return db.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Bebida]:
        """Obtener todas las bebidas con paginación"""
        stmt = select(Bebida).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_tipo(db: Session, tipo_bebida: str) -> List[Bebida]:
        """Obtener bebidas por tipo"""
        stmt = select(Bebida).where(Bebida.tipo_bebida == tipo_bebida)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_temperatura(db: Session, es_fria: bool) -> List[Bebida]:
        """Obtener bebidas por temperatura (frías o calientes)"""
        stmt = select(Bebida).where(Bebida.es_fria == es_fria)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def update(db: Session, bebida_id: int, bebida_update: BebidaUpdate) -> Optional[Bebida]:
        """Actualizar una bebida existente"""
        db_bebida = BebidaRepository.get_by_id(db, bebida_id)
        if not db_bebida:
            return None
        
        # Actualizar campos uno por uno
        if bebida_update.nombre is not None:
            db_bebida.nombre = bebida_update.nombre
        if bebida_update.descripcion is not None:
            db_bebida.descripcion = bebida_update.descripcion
        if bebida_update.imagen_url is not None:
            db_bebida.imagen_url = bebida_update.imagen_url
        if bebida_update.tipo_bebida is not None:
            db_bebida.tipo_bebida = bebida_update.tipo_bebida.value
        if bebida_update.ingredientes is not None:
            db_bebida.ingredientes = bebida_update.ingredientes
        if bebida_update.es_fria is not None:
            db_bebida.es_fria = bebida_update.es_fria
        
        # Manejar precio especialmente
        if bebida_update.precio is not None:
            precio_tuple = (
                bebida_update.precio.small,
                bebida_update.precio.medium,
                bebida_update.precio.big
            )
            db_bebida.precio = precio_tuple
        
        # Manejar disponible especialmente
        if bebida_update.disponible is not None:
            disponible_tuple = (
                bebida_update.disponible.small,
                bebida_update.disponible.medium,
                bebida_update.disponible.big
            )
            db_bebida.disponible = disponible_tuple
        
        db.commit()
        db.refresh(db_bebida)
        return db_bebida
    
    @staticmethod
    def delete(db: Session, bebida_id: int) -> bool:
        """Eliminar una bebida"""
        db_bebida = BebidaRepository.get_by_id(db, bebida_id)
        if not db_bebida:
            return False
        
        db.delete(db_bebida)
        db.commit()
        return True
