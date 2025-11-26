"""
Service para Producto
Lógica de negocio para operaciones con productos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.producto import ProductoRepository
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoOut
from app.models import Producto


class ProductoService:
    """Service con lógica de negocio para Producto"""
    
    @staticmethod
    def create_producto(db: Session, producto: ProductoCreate) -> ProductoOut:
        """Crear un nuevo producto con validaciones"""
        # Validar que el nombre no esté vacío
        if not producto.nombre or producto.nombre.strip() == "":
            raise ValueError("El nombre del producto no puede estar vacío")
        
        db_producto = ProductoRepository.create(db, producto)
        return ProductoOut.model_validate(db_producto)
    
    @staticmethod
    def get_producto(db: Session, producto_id: int) -> Optional[ProductoOut]:
        """Obtener producto por ID"""
        db_producto = ProductoRepository.get_by_id(db, producto_id)
        if not db_producto:
            return None
        return ProductoOut.model_validate(db_producto)
    
    @staticmethod
    def get_all_productos(db: Session, skip: int = 0, limit: int = 100) -> List[ProductoOut]:
        """Obtener todos los productos"""
        productos = ProductoRepository.get_all(db, skip, limit)
        return [ProductoOut.model_validate(p) for p in productos]
    
    @staticmethod
    def update_producto(db: Session, producto_id: int, producto_update: ProductoUpdate) -> Optional[ProductoOut]:
        """Actualizar producto con validaciones"""
        # Validar que al menos un campo se esté actualizando
        if not any(producto_update.model_dump(exclude_unset=True).values()):
            raise ValueError("Debe proporcionar al menos un campo para actualizar")
        
        db_producto = ProductoRepository.update(db, producto_id, producto_update)
        if not db_producto:
            return None
        return ProductoOut.model_validate(db_producto)
    
    @staticmethod
    def delete_producto(db: Session, producto_id: int) -> bool:
        """Eliminar producto"""
        return ProductoRepository.delete(db, producto_id)
