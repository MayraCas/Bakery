"""
Service para Bebida
Lógica de negocio para operaciones con bebidas
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.bebida import BebidaRepository
from app.schemas.bebida import BebidaCreate, BebidaUpdate, BebidaOut


class BebidaService:
    """Service con lógica de negocio para Bebida"""
    
    @staticmethod
    def create_bebida(db: Session, bebida: BebidaCreate) -> BebidaOut:
        """Crear una nueva bebida con validaciones"""
        # Validar que el nombre no esté vacío
        if not bebida.nombre or bebida.nombre.strip() == "":
            raise ValueError("El nombre de la bebida no puede estar vacío")
        
        # Validar ingredientes
        if not bebida.ingredientes or len(bebida.ingredientes) == 0:
            raise ValueError("La bebida debe tener al menos un ingrediente")
        
        # Validar coherencia de precios
        if bebida.precio.small > bebida.precio.medium:
            raise ValueError("El precio pequeño no puede ser mayor al mediano")
        if bebida.precio.medium > bebida.precio.big:
            raise ValueError("El precio mediano no puede ser mayor al grande")
        
        db_bebida = BebidaRepository.create(db, bebida)
        return BebidaOut.model_validate(db_bebida)
    
    @staticmethod
    def get_bebida(db: Session, bebida_id: int) -> Optional[BebidaOut]:
        """Obtener bebida por ID"""
        db_bebida = BebidaRepository.get_by_id(db, bebida_id)
        if not db_bebida:
            return None
        return BebidaOut.model_validate(db_bebida)
    
    @staticmethod
    def get_all_bebidas(db: Session, skip: int = 0, limit: int = 100) -> List[BebidaOut]:
        """Obtener todas las bebidas"""
        bebidas = BebidaRepository.get_all(db, skip, limit)
        return [BebidaOut.model_validate(b) for b in bebidas]
    
    @staticmethod
    def get_bebidas_by_tipo(db: Session, tipo_bebida: str) -> List[BebidaOut]:
        """Obtener bebidas por tipo"""
        bebidas = BebidaRepository.get_by_tipo(db, tipo_bebida)
        return [BebidaOut.model_validate(b) for b in bebidas]
    
    @staticmethod
    def get_bebidas_frias(db: Session) -> List[BebidaOut]:
        """Obtener solo bebidas frías"""
        bebidas = BebidaRepository.get_by_temperatura(db, es_fria=True)
        return [BebidaOut.model_validate(b) for b in bebidas]
    
    @staticmethod
    def get_bebidas_calientes(db: Session) -> List[BebidaOut]:
        """Obtener solo bebidas calientes"""
        bebidas = BebidaRepository.get_by_temperatura(db, es_fria=False)
        return [BebidaOut.model_validate(b) for b in bebidas]
    
    @staticmethod
    def update_bebida(db: Session, bebida_id: int, bebida_update: BebidaUpdate) -> Optional[BebidaOut]:
        """Actualizar bebida con validaciones"""
        # Validar coherencia de precios si se actualiza
        if bebida_update.precio:
            if bebida_update.precio.small > bebida_update.precio.medium:
                raise ValueError("El precio pequeño no puede ser mayor al mediano")
            if bebida_update.precio.medium > bebida_update.precio.big:
                raise ValueError("El precio mediano no puede ser mayor al grande")
        
        db_bebida = BebidaRepository.update(db, bebida_id, bebida_update)
        if not db_bebida:
            return None
        return BebidaOut.model_validate(db_bebida)
    
    @staticmethod
    def delete_bebida(db: Session, bebida_id: int) -> bool:
        """Eliminar bebida"""
        return BebidaRepository.delete(db, bebida_id)
