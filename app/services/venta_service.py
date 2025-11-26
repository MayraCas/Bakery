"""
Service para Venta
Lógica de negocio para operaciones con ventas
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from datetime import date
from app.repositories.venta import VentaRepository
from app.repositories.producto import ProductoRepository
from app.schemas.venta import VentaCreate, VentaUpdate, VentaOut, InsertarVentaRequest
from app.models import Producto


class VentaService:
    """Service con lógica de negocio para Venta"""
    
    @staticmethod
    def create_venta(db: Session, venta: VentaCreate) -> VentaOut:
        """
        Crear una nueva venta con validaciones.
        
        Validaciones:
        - Todos los productos deben existir
        - Cantidades y precios deben ser positivos
        
        Los triggers de PostgreSQL se encargan de:
        - Verificar disponibilidad automáticamente
        - Calcular precio_total
        """
        # Validar que hay al menos un detalle
        if not venta.detalles_venta or len(venta.detalles_venta) == 0:
            raise ValueError("La venta debe tener al menos un producto")
        
        # Validar existencia de productos
        for detalle in venta.detalles_venta:
            # Verificar que el producto existe
            producto = ProductoRepository.get_by_id(db, detalle.id_producto)
            if not producto:
                raise ValueError(f"El producto con ID {detalle.id_producto} no existe")
            
            # Validar cantidad y precio positivos
            if detalle.cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
            if detalle.precio <= 0:
                raise ValueError("El precio debe ser mayor a 0")
        
        # Crear venta (los triggers manejan stock y total)
        db_venta = VentaRepository.create(db, venta)
        return VentaOut.model_validate(db_venta)
    
    @staticmethod
    def get_venta(db: Session, venta_id: int) -> Optional[VentaOut]:
        """Obtener venta por ID con sus detalles"""
        db_venta = VentaRepository.get_by_id(db, venta_id)
        if not db_venta:
            return None
        return VentaOut.model_validate(db_venta)
    
    @staticmethod
    def get_all_ventas(db: Session, skip: int = 0, limit: int = 100) -> List[VentaOut]:
        """Obtener todas las ventas ordenadas por fecha descendente"""
        ventas = VentaRepository.get_all(db, skip, limit)
        return [VentaOut.model_validate(v) for v in ventas]
    
    @staticmethod
    def get_ventas_by_fecha(db: Session, fecha: date) -> List[VentaOut]:
        """Obtener ventas de una fecha específica"""
        ventas = VentaRepository.get_by_fecha(db, fecha)
        return [VentaOut.model_validate(v) for v in ventas]
    
    @staticmethod
    def update_venta(db: Session, venta_id: int, venta_update: VentaUpdate) -> Optional[VentaOut]:
        """
        Actualizar venta (solo detalles y fecha).
        
        NOTA: No se puede modificar precio_total directamente,
        se calcula automáticamente por trigger.
        """
        db_venta = VentaRepository.update(db, venta_id, venta_update)
        if not db_venta:
            return None
        return VentaOut.model_validate(db_venta)
    
    @staticmethod
    def delete_venta(db: Session, venta_id: int) -> bool:
        """
        Eliminar venta.
        
        IMPORTANTE: Los triggers gestionan disponibilidad automáticamente.
        """
        return VentaRepository.delete(db, venta_id)
    
    @staticmethod
    def insertar_venta_sql(db: Session, request: InsertarVentaRequest) -> int:
        """
        Crear venta usando la función SQL insertar_venta().
        
        Esta función SQL maneja toda la lógica en PostgreSQL.
        Útil cuando se quiere delegar toda la lógica a la base de datos.
        
        Returns:
            ID de la venta creada
        """
        # Validar que hay al menos un detalle
        if not request.venta_detalle or len(request.venta_detalle) == 0:
            raise ValueError("La venta debe tener al menos un producto")
        
        # Convertir a formato dict para la función SQL
        venta_detalle_dicts = [
            {
                "id_producto": d.id_producto,
                "cantidad": d.cantidad,
                "precio": str(d.precio),
                "variante": d.variante
            }
            for d in request.venta_detalle
        ]
        
        try:
            venta_id = VentaRepository.insertar_venta_sql(
                db=db,
                detalles=request.detalles,
                venta_detalle=venta_detalle_dicts,
                fecha=request.fecha
            )
            return venta_id
        except Exception as e:
            # La función SQL puede lanzar excepciones (producto no existe, stock insuficiente, etc.)
            raise ValueError(f"Error al crear venta: {str(e)}")
