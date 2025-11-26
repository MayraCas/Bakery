"""
Service para Extra
Lógica de negocio para operaciones con extras
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.extra import ExtraRepository
from app.schemas.extra import ExtraCreate, ExtraUpdate, ExtraOut


class ExtraService:
    """Service con lógica de negocio para Extra"""
    
    @staticmethod
    def create_extra(db: Session, extra: ExtraCreate) -> ExtraOut:
        """Crear un nuevo extra con validaciones"""
        # Validar que el nombre no esté vacío
        if not extra.nombre or extra.nombre.strip() == "":
            raise ValueError("El nombre del extra no puede estar vacío")
        
        # Validar coherencia de precios (wholesale debe ser <= retail_sale)
        if extra.precio.wholesale > extra.precio.retail_sale:
            raise ValueError("El precio al por mayor no puede ser mayor al precio al por menor")
        
        db_extra = ExtraRepository.create(db, extra)
        return ExtraOut.model_validate(db_extra)
    
    @staticmethod
    def get_extra(db: Session, extra_id: int) -> Optional[ExtraOut]:
        """Obtener extra por ID"""
        db_extra = ExtraRepository.get_by_id(db, extra_id)
        if not db_extra:
            return None
        return ExtraOut.model_validate(db_extra)
    
    @staticmethod
    def get_all_extras(db: Session, skip: int = 0, limit: int = 100) -> List[ExtraOut]:
        """Obtener todos los extras"""
        extras = ExtraRepository.get_all(db, skip, limit)
        return [ExtraOut.model_validate(e) for e in extras]
    
    @staticmethod
    def get_extras_by_tipo(db: Session, tipo_extra: str) -> List[ExtraOut]:
        """Obtener extras por tipo"""
        extras = ExtraRepository.get_by_tipo(db, tipo_extra)
        return [ExtraOut.model_validate(e) for e in extras]
    
    @staticmethod
    def update_extra(db: Session, extra_id: int, extra_update: ExtraUpdate) -> Optional[ExtraOut]:
        """Actualizar extra con validaciones"""
        # Validar coherencia de precios si se actualiza
        if extra_update.precio:
            if extra_update.precio.wholesale > extra_update.precio.retail_sale:
                raise ValueError("El precio al por mayor no puede ser mayor al precio al por menor")
        
        db_extra = ExtraRepository.update(db, extra_id, extra_update)
        if not db_extra:
            return None
        return ExtraOut.model_validate(db_extra)
    
    @staticmethod
    def delete_extra(db: Session, extra_id: int) -> bool:
        """Eliminar extra"""
        return ExtraRepository.delete(db, extra_id)
