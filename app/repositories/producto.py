
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate


class ProductoRepository:

    @staticmethod
    def create(db: Session, producto: ProductoCreate) -> Producto:
        db_producto = Producto(**producto.model_dump())
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto
    
    @staticmethod
    def get_by_id(db: Session, producto_id: int) -> Optional[Producto]:
        stmt = select(Producto).where(Producto.id == producto_id)
        return db.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Producto]:
        stmt = select(Producto).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def update(db: Session, producto_id: int, producto_update: ProductoUpdate) -> Optional[Producto]:
        db_producto = ProductoRepository.get_by_id(db, producto_id)
        if not db_producto:
            return None
        
        update_data = producto_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_producto, field, value)
        
        db.commit()
        db.refresh(db_producto)
        return db_producto
    
    @staticmethod
    def delete(db: Session, producto_id: int) -> bool:
        db_producto = ProductoRepository.get_by_id(db, producto_id)
        if not db_producto:
            return False
        
        db.delete(db_producto)
        db.commit()
        return True
