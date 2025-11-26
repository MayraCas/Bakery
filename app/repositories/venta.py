"""
Repository para Venta y VentaDetalle
CRUD para ventas y sus detalles
"""
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from typing import List, Optional
from datetime import date
from app.models import Venta, VentaDetalle
from app.schemas.venta import VentaCreate, VentaUpdate, VentaDetalleCreate, VentaDetalleUpdate
import json


class VentaRepository:
    """Repository para operaciones CRUD en Venta"""
    
    @staticmethod
    def create(db: Session, venta: VentaCreate) -> Venta:
        """
        Crear una nueva venta con sus detalles.
        
        IMPORTANTE: Los triggers de PostgreSQL se encargan de:
        - Validar existencia de productos (trg_verificar_producto_fk)
        - Actualizar stock (trg_gestion_stock)
        - Calcular precio_total (trg_calcular_total_venta)
        """
        # Crear venta (cabecera) con precio_total = 0 (se calcula por trigger)
        db_venta = Venta(
            detalles=venta.detalles,
            fecha=venta.fecha or date.today(),
            precio_total=0
        )
        db.add(db_venta)
        db.flush()  # Obtener el ID sin hacer commit
        
        # Crear detalles
        for detalle in venta.detalles_venta:
            db_detalle = VentaDetalle(
                id_venta=db_venta.id,
                id_producto=detalle.id_producto,
                cantidad=detalle.cantidad,
                precio=detalle.precio
            )
            db.add(db_detalle)
        
        db.commit()
        db.refresh(db_venta)
        return db_venta
    
    @staticmethod
    def get_by_id(db: Session, venta_id: int) -> Optional[Venta]:
        """Obtener venta por ID con sus detalles"""
        stmt = select(Venta).where(Venta.id == venta_id)
        return db.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Venta]:
        """Obtener todas las ventas con paginación"""
        stmt = select(Venta).offset(skip).limit(limit).order_by(Venta.fecha.desc())
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_fecha(db: Session, fecha: date) -> List[Venta]:
        """Obtener ventas por fecha"""
        stmt = select(Venta).where(Venta.fecha == fecha)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def update(db: Session, venta_id: int, venta_update: VentaUpdate) -> Optional[Venta]:
        """
        Actualizar una venta.
        
        NOTA: Solo actualiza detalles y fecha.
        precio_total NO se debe modificar manualmente (lo calcula el trigger).
        """
        db_venta = VentaRepository.get_by_id(db, venta_id)
        if not db_venta:
            return None
        
        update_data = venta_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_venta, field, value)
        
        db.commit()
        db.refresh(db_venta)
        return db_venta
    
    @staticmethod
    def delete(db: Session, venta_id: int) -> bool:
        """
        Eliminar una venta.
        
        IMPORTANTE: Los detalles se eliminan en cascada (ON DELETE CASCADE).
        Los triggers devuelven el stock automáticamente.
        """
        db_venta = VentaRepository.get_by_id(db, venta_id)
        if not db_venta:
            return False
        
        db.delete(db_venta)
        db.commit()
        return True
    
    @staticmethod
    def insertar_venta_sql(
        db: Session, 
        detalles: str, 
        venta_detalle: List[dict],
        fecha: Optional[date] = None
    ) -> int:
        """
        Llama a la función SQL insertar_venta() de PostgreSQL.
        
        Esta función SQL maneja toda la lógica de:
        - Crear venta
        - Insertar detalles
        - Triggers automáticos
        
        Returns:
            ID de la venta creada
        """
        # Convertir venta_detalle a JSON
        venta_detalle_json = json.dumps(venta_detalle)
        
        # Preparar fecha
        fecha_str = fecha.isoformat() if fecha else None
        
        # Ejecutar función SQL
        if fecha_str:
            query = text(
                "SELECT insertar_venta(:detalles, :venta_detalle::jsonb, :fecha::date)"
            )
            result = db.execute(
                query,
                {
                    "detalles": detalles,
                    "venta_detalle": venta_detalle_json,
                    "fecha": fecha_str
                }
            )
        else:
            query = text(
                "SELECT insertar_venta(:detalles, :venta_detalle::jsonb)"
            )
            result = db.execute(
                query,
                {
                    "detalles": detalles,
                    "venta_detalle": venta_detalle_json
                }
            )
        
        venta_id = result.scalar()
        db.commit()
        return venta_id


class VentaDetalleRepository:
    """Repository para operaciones CRUD en VentaDetalle"""
    
    @staticmethod
    def create(db: Session, detalle: VentaDetalleCreate, venta_id: int) -> VentaDetalle:
        """
        Crear un detalle de venta.
        
        IMPORTANTE: Los triggers actualizan stock y recalculan total automáticamente.
        """
        db_detalle = VentaDetalle(
            id_venta=venta_id,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            precio=detalle.precio
        )
        db.add(db_detalle)
        db.commit()
        db.refresh(db_detalle)
        return db_detalle
    
    @staticmethod
    def get_by_id(db: Session, detalle_id: int) -> Optional[VentaDetalle]:
        """Obtener detalle por ID"""
        stmt = select(VentaDetalle).where(VentaDetalle.id == detalle_id)
        return db.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_by_venta(db: Session, venta_id: int) -> List[VentaDetalle]:
        """Obtener todos los detalles de una venta"""
        stmt = select(VentaDetalle).where(VentaDetalle.id_venta == venta_id)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def update(db: Session, detalle_id: int, detalle_update: VentaDetalleUpdate) -> Optional[VentaDetalle]:
        """
        Actualizar un detalle de venta.
        
        IMPORTANTE: Los triggers ajustan stock y recalculan total automáticamente.
        """
        db_detalle = VentaDetalleRepository.get_by_id(db, detalle_id)
        if not db_detalle:
            return None
        
        update_data = detalle_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_detalle, field, value)
        
        db.commit()
        db.refresh(db_detalle)
        return db_detalle
    
    @staticmethod
    def delete(db: Session, detalle_id: int) -> bool:
        """
        Eliminar un detalle de venta.
        
        IMPORTANTE: Los triggers devuelven stock y recalculan total automáticamente.
        """
        db_detalle = VentaDetalleRepository.get_by_id(db, detalle_id)
        if not db_detalle:
            return False
        
        db.delete(db_detalle)
        db.commit()
        return True
