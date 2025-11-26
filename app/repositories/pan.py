"""
Repository para Pan (hereda de Producto)
CRUD para la tabla pan respetando la herencia
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models import Pan
from app.schemas.pan import PanCreate, PanUpdate


class PanRepository:
    """Repository para operaciones CRUD en Pan"""
    
    @staticmethod
    def create(db: Session, pan: PanCreate) -> Pan:
        """
        Crear un nuevo pan.
        La inserción en la tabla hija automáticamente crea el registro en producto (herencia).
        """
        # Convertir precio schema a tupla para PostgreSQL
        precio_tuple = None
        if pan.precio:
            precio_tuple = (
                pan.precio.retail_sale,
                pan.precio.wholesale
            )
        
        # Crear el objeto directamente desde los atributos del schema
        db_pan = Pan(
            nombre=pan.nombre,
            descripcion=pan.descripcion,
            imagen_url=pan.imagen_url,
            tipo_pan=pan.tipo_pan.value if pan.tipo_pan else None,
            precio=precio_tuple,
            disponible=True,  # Disponible por defecto
            ingredientes=pan.ingredientes
        )
        
        db.add(db_pan)
        db.commit()
        db.refresh(db_pan)
        return db_pan
    
    @staticmethod
    def get_by_id(db: Session, pan_id: int) -> Optional[Pan]:
        """Obtener pan por ID"""
        stmt = select(Pan).where(Pan.id == pan_id)
        return db.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Pan]:
        """Obtener todos los panes con paginación"""
        stmt = select(Pan).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_tipo(db: Session, tipo_pan: str) -> List[Pan]:
        """Obtener panes por tipo (Dulce/Salado)"""
        stmt = select(Pan).where(Pan.tipo_pan == tipo_pan)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def update(db: Session, pan_id: int, pan_update: PanUpdate) -> Optional[Pan]:
        """Actualizar un pan existente"""
        db_pan = PanRepository.get_by_id(db, pan_id)
        if not db_pan:
            return None
        
        # Actualizar campos uno por uno para tener control sobre los enums
        if pan_update.nombre is not None:
            db_pan.nombre = pan_update.nombre
        if pan_update.descripcion is not None:
            db_pan.descripcion = pan_update.descripcion
        if pan_update.imagen_url is not None:
            db_pan.imagen_url = pan_update.imagen_url
        if pan_update.tipo_pan is not None:
            db_pan.tipo_pan = pan_update.tipo_pan.value
        if pan_update.ingredientes is not None:
            db_pan.ingredientes = pan_update.ingredientes
        
        # Manejar precio especialmente
        if pan_update.precio is not None:
            precio_tuple = (
                pan_update.precio.retail_sale,
                pan_update.precio.wholesale
            )
            db_pan.precio = precio_tuple
        
        # Manejar disponible
        if pan_update.disponible is not None:
            db_pan.disponible = pan_update.disponible
        
        db.commit()
        db.refresh(db_pan)
        return db_pan
    
    @staticmethod
    def delete(db: Session, pan_id: int) -> bool:
        """Eliminar un pan"""
        db_pan = PanRepository.get_by_id(db, pan_id)
        if not db_pan:
            return False
        
        db.delete(db_pan)
        db.commit()
        return True
