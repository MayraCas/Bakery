"""
Service para Pan
Lógica de negocio para operaciones con pan
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.pan import PanRepository
from app.schemas.pan import PanCreate, PanUpdate, PanOut


class PanService:
    """Service con lógica de negocio para Pan"""
    
    @staticmethod
    def create_pan(db: Session, pan: PanCreate) -> PanOut:
        """Crear un nuevo pan con validaciones"""
        # Validar que el nombre no esté vacío
        if not pan.nombre or pan.nombre.strip() == "":
            raise ValueError("El nombre del pan no puede estar vacío")
        
        # Validar ingredientes
        if not pan.ingredientes or len(pan.ingredientes) == 0:
            raise ValueError("El pan debe tener al menos un ingrediente")
        
        # Validar coherencia de precios (wholesale debe ser <= retail_sale)
        if pan.precio.wholesale > pan.precio.retail_sale:
            raise ValueError("El precio al por mayor no puede ser mayor al precio al por menor")
        
        db_pan = PanRepository.create(db, pan)
        return PanOut.model_validate(db_pan)
    
    @staticmethod
    def get_pan(db: Session, pan_id: int) -> Optional[PanOut]:
        """Obtener pan por ID"""
        db_pan = PanRepository.get_by_id(db, pan_id)
        if not db_pan:
            return None
        return PanOut.model_validate(db_pan)
    
    @staticmethod
    def get_all_panes(db: Session, skip: int = 0, limit: int = 100) -> List[PanOut]:
        """Obtener todos los panes"""
        panes = PanRepository.get_all(db, skip, limit)
        return [PanOut.model_validate(p) for p in panes]
    
    @staticmethod
    def get_panes_by_tipo(db: Session, tipo_pan: str) -> List[PanOut]:
        """Obtener panes por tipo (Dulce/Salado)"""
        panes = PanRepository.get_by_tipo(db, tipo_pan)
        return [PanOut.model_validate(p) for p in panes]
    
    @staticmethod
    def update_pan(db: Session, pan_id: int, pan_update: PanUpdate) -> Optional[PanOut]:
        """Actualizar pan con validaciones"""
        # Validar coherencia de precios si se actualiza
        if pan_update.precio:
            if pan_update.precio.wholesale > pan_update.precio.retail_sale:
                raise ValueError("El precio al por mayor no puede ser mayor al precio al por menor")
        
        db_pan = PanRepository.update(db, pan_id, pan_update)
        if not db_pan:
            return None
        return PanOut.model_validate(db_pan)
    
    @staticmethod
    def delete_pan(db: Session, pan_id: int) -> bool:
        """Eliminar pan"""
        return PanRepository.delete(db, pan_id)
