
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.pan import PanRepository
from app.schemas.pan import PanCreate, PanUpdate, PanOut


class PanService:
    
    @staticmethod
    def create_pan(db: Session, pan: PanCreate) -> PanOut:

        if not pan.nombre or pan.nombre.strip() == "":
            raise ValueError("El nombre del pan no puede estar vacío")
        if not pan.ingredientes or len(pan.ingredientes) == 0:
            raise ValueError("El pan debe tener al menos un ingrediente")
        if pan.precio.wholesale > pan.precio.retail_sale:
            raise ValueError("El precio al por mayor no puede ser mayor al precio al por menor")
        
        db_pan = PanRepository.create(db, pan)
        return PanOut.model_validate(db_pan)
    
    @staticmethod
    def get_pan(db: Session, pan_id: int) -> Optional[PanOut]:

        db_pan = PanRepository.get_by_id(db, pan_id)
        if not db_pan:
            return None
        return PanOut.model_validate(db_pan)
    
    @staticmethod
    def get_all_panes(db: Session, skip: int = 0, limit: int = 100) -> List[PanOut]:
        panes = PanRepository.get_all(db, skip, limit)
        return [PanOut.model_validate(p) for p in panes]
    
    @staticmethod
    def get_panes_by_tipo(db: Session, tipo_pan: str) -> List[PanOut]:
        panes = PanRepository.get_by_tipo(db, tipo_pan)
        return [PanOut.model_validate(p) for p in panes]
    
    @staticmethod
    def update_pan(db: Session, pan_id: int, pan_update: PanUpdate) -> Optional[PanOut]:
        if pan_update.precio:
            if pan_update.precio.wholesale > pan_update.precio.retail_sale:
                raise ValueError("El precio al por mayor no puede ser mayor al precio al por menor")
        
        db_pan = PanRepository.update(db, pan_id, pan_update)
        if not db_pan:
            return None
        return PanOut.model_validate(db_pan)
    
    @staticmethod
    def delete_pan(db: Session, pan_id: int) -> bool:
        return PanRepository.delete(db, pan_id)
