
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from datetime import date
from app.repositories.venta import VentaRepository
from app.repositories.producto import ProductoRepository
from app.schemas.venta import VentaCreate, VentaUpdate, VentaOut, InsertarVentaRequest
from app.models import Producto


class VentaService:

    @staticmethod
    def create_venta(db: Session, venta: VentaCreate) -> VentaOut:

        if not venta.detalles_venta or len(venta.detalles_venta) == 0:
            raise ValueError("La venta debe tener al menos un producto")
        
        for detalle in venta.detalles_venta:
            producto = ProductoRepository.get_by_id(db, detalle.id_producto)
            if not producto:
                raise ValueError(f"El producto con ID {detalle.id_producto} no existe")
            
            if detalle.cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
            if detalle.precio <= 0:
                raise ValueError("El precio debe ser mayor a 0")
        
        db_venta = VentaRepository.create(db, venta)
        return VentaOut.model_validate(db_venta)
    
    @staticmethod
    def get_venta(db: Session, venta_id: int) -> Optional[VentaOut]:
        db_venta = VentaRepository.get_by_id(db, venta_id)
        if not db_venta:
            return None
        return VentaOut.model_validate(db_venta)
    
    @staticmethod
    def get_all_ventas(db: Session, skip: int = 0, limit: int = 100) -> List[VentaOut]:
        ventas = VentaRepository.get_all(db, skip, limit)
        return [VentaOut.model_validate(v) for v in ventas]
    
    @staticmethod
    def get_ventas_by_fecha(db: Session, fecha: date) -> List[VentaOut]:
        ventas = VentaRepository.get_by_fecha(db, fecha)
        return [VentaOut.model_validate(v) for v in ventas]
    
    @staticmethod
    def update_venta(db: Session, venta_id: int, venta_update: VentaUpdate) -> Optional[VentaOut]:
        db_venta = VentaRepository.update(db, venta_id, venta_update)
        if not db_venta:
            return None
        return VentaOut.model_validate(db_venta)
    
    @staticmethod
    def delete_venta(db: Session, venta_id: int) -> bool:

        return VentaRepository.delete(db, venta_id)
    
    @staticmethod
    def insertar_venta_sql(db: Session, request: InsertarVentaRequest) -> int:

        if not request.venta_detalle or len(request.venta_detalle) == 0:
            raise ValueError("La venta debe tener al menos un producto")
        
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
            raise ValueError(f"Error al crear venta: {str(e)}")
