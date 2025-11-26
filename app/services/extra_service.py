
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.extra import ExtraRepository
from app.schemas.extra import ExtraCreate, ExtraUpdate, ExtraOut


class ExtraService:    
    @staticmethod
    def create_extra(db: Session, extra: ExtraCreate) -> ExtraOut:
        if not extra.nombre or extra.nombre.strip() == "":
            raise ValueError("El nombre del extra no puede estar vacío")
        
        if extra.precio.wholesale > extra.precio.retail_sale:
            raise ValueError("El precio al por mayor no puede ser mayor al precio al por menor")
        
        db_extra = ExtraRepository.create(db, extra)
        return ExtraOut.model_validate(db_extra)
    
    @staticmethod
    def get_extra(db: Session, extra_id: int) -> Optional[ExtraOut]:
        db_extra = ExtraRepository.get_by_id(db, extra_id)
        if not db_extra:
            return None
        return ExtraOut.model_validate(db_extra)
    
    @staticmethod
    def get_all_extras(db: Session, skip: int = 0, limit: int = 100) -> List[ExtraOut]:
        extras = ExtraRepository.get_all(db, skip, limit)
        return [ExtraOut.model_validate(e) for e in extras]
    
    @staticmethod
    def get_extras_by_tipo(db: Session, tipo_extra: str) -> List[ExtraOut]:
        extras = ExtraRepository.get_by_tipo(db, tipo_extra)
        return [ExtraOut.model_validate(e) for e in extras]
    
    @staticmethod
    def update_extra(db: Session, extra_id: int, extra_update: ExtraUpdate) -> Optional[ExtraOut]:

        if extra_update.precio:
            if extra_update.precio.wholesale > extra_update.precio.retail_sale:
                raise ValueError("El precio al por mayor no puede ser mayor al precio al por menor")
        
        db_extra = ExtraRepository.update(db, extra_id, extra_update)
        if not db_extra:
            return None
        return ExtraOut.model_validate(db_extra)
    
    @staticmethod
    def delete_extra(db: Session, extra_id: int) -> bool:
        return ExtraRepository.delete(db, extra_id)
