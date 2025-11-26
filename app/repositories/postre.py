"""
Repository para Postre (hereda de Producto)
CRUD para la tabla postre respetando la herencia
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models import Postre
from app.schemas.postre import PostreCreate, PostreUpdate


class PostreRepository:
    """Repository para operaciones CRUD en Postre"""
    
    @staticmethod
    def create(db: Session, postre: PostreCreate) -> Postre:
        """
        Crear un nuevo postre.
        La inserción en la tabla hija automáticamente crea el registro en producto (herencia).
        """
        # Convertir precio schema a tupla para PostgreSQL
        precio_tuple = None
        if postre.precio:
            precio_tuple = (
                postre.precio.small,
                postre.precio.medium,
                postre.precio.big
            )
        
        # Crear el objeto directamente desde los atributos del schema
        # Esto evita problemas con la serialización de enums
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
        """Obtener postre por ID"""
        stmt = select(Postre).where(Postre.id == postre_id)
        return db.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Postre]:
        """Obtener todos los postres con paginación"""
        stmt = select(Postre).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_tipo(db: Session, tipo_postre: str) -> List[Postre]:
        """Obtener postres por tipo"""
        stmt = select(Postre).where(Postre.tipo_postre == tipo_postre)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def update(db: Session, postre_id: int, postre_update: PostreUpdate) -> Optional[Postre]:
        """Actualizar un postre existente"""
        db_postre = PostreRepository.get_by_id(db, postre_id)
        if not db_postre:
            return None
        
        # Actualizar campos uno por uno para tener control sobre los enums
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
        
        # Manejar precio especialmente
        if postre_update.precio is not None:
            precio_tuple = (
                postre_update.precio.small,
                postre_update.precio.medium,
                postre_update.precio.big
            )
            db_postre.precio = precio_tuple
        
        # Manejar disponible especialmente
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
        """Eliminar un postre"""
        db_postre = PostreRepository.get_by_id(db, postre_id)
        if not db_postre:
            return False
        
        db.delete(db_postre)
        db.commit()
        return True
