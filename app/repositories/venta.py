from sqlalchemy.orm import Session
from sqlalchemy import select, text, String
from typing import List, Optional
from datetime import date
from app.models import Venta, VentaDetalle
from app.schemas.venta import VentaCreate, VentaUpdate, VentaDetalleCreate, VentaDetalleUpdate
import json


class VentaRepository:    
    @staticmethod
    def create(db: Session, venta: VentaCreate) -> Venta:
        db_venta = Venta(
            detalles=venta.detalles,
            fecha=venta.fecha or date.today(),
            precio_total=0
        )
        db.add(db_venta)
        db.flush() 
        
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
        stmt = select(Venta).where(Venta.id == venta_id)
        return db.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Venta]:
        stmt = select(Venta).offset(skip).limit(limit).order_by(Venta.fecha.desc())
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_fecha(db: Session, fecha: date) -> List[Venta]:
        stmt = select(Venta).where(Venta.fecha == fecha)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def update(db: Session, venta_id: int, venta_update: VentaUpdate) -> Optional[Venta]:
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

        venta_detalle_json = json.dumps(venta_detalle)
        
        detalles_escaped = detalles.replace("'", "''")
        venta_detalle_escaped = venta_detalle_json.replace("'", "''")
        
        if fecha:
            fecha_str = fecha.isoformat() if isinstance(fecha, date) else fecha
            sql = f"SELECT insertar_venta('{detalles_escaped}', '{venta_detalle_escaped}'::jsonb, '{fecha_str}'::date)"
        else:
            sql = f"SELECT insertar_venta('{detalles_escaped}', '{venta_detalle_escaped}'::jsonb)"
        
        result = db.execute(text(sql))
        venta_id = result.scalar()
        db.commit()
        return venta_id
    
    @staticmethod
    def obtener_ventas_detalles(db: Session) -> List[dict]:
        """
        Obtiene el historial completo de ventas usando la función SQL obtener_ventas_detalles().
        Retorna una lista de diccionarios con id_venta, fecha, productos (JSON) y total.
        """
        sql = "SELECT * FROM obtener_ventas_detalles()"
        result = db.execute(text(sql))
        
        ventas = []
        for row in result:
            ventas.append({
                "id_venta": row[0],
                "fecha": row[1].isoformat() if row[1] else None,
                "productos": row[2],
                "total": float(row[3]) if row[3] else 0.0
            })
        
        return ventas


class VentaDetalleRepository:

    @staticmethod
    def create(db: Session, detalle: VentaDetalleCreate, venta_id: int) -> VentaDetalle:

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
        stmt = select(VentaDetalle).where(VentaDetalle.id == detalle_id)
        return db.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_by_venta(db: Session, venta_id: int) -> List[VentaDetalle]:
        stmt = select(VentaDetalle).where(VentaDetalle.id_venta == venta_id)
        return list(db.execute(stmt).scalars().all())
    
    @staticmethod
    def update(db: Session, detalle_id: int, detalle_update: VentaDetalleUpdate) -> Optional[VentaDetalle]:
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
        db_detalle = VentaDetalleRepository.get_by_id(db, detalle_id)
        if not db_detalle:
            return False
        
        db.delete(db_detalle)
        db.commit()
        return True
