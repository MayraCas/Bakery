
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.postre import PostreRepository
from app.schemas.postre import PostreCreate, PostreUpdate, PostreOut


class PostreService:
    
    @staticmethod
    def create_postre(db: Session, postre: PostreCreate) -> PostreOut:
        if not postre.nombre or postre.nombre.strip() == "":
            raise ValueError("El nombre del postre no puede estar vacío")
        
        if not postre.ingredientes or len(postre.ingredientes) == 0:
            raise ValueError("El postre debe tener al menos un ingrediente")
        
        if postre.precio.small > postre.precio.medium:
            raise ValueError("El precio pequeño no puede ser mayor al mediano")
        if postre.precio.medium > postre.precio.big:
            raise ValueError("El precio mediano no puede ser mayor al grande")
        
        db_postre = PostreRepository.create(db, postre)
        return PostreOut.model_validate(db_postre)
    
    @staticmethod
    def get_postre(db: Session, postre_id: int) -> Optional[PostreOut]:
        db_postre = PostreRepository.get_by_id(db, postre_id)
        if not db_postre:
            return None
        return PostreOut.model_validate(db_postre)
    
    @staticmethod
    def get_all_postres(db: Session, skip: int = 0, limit: int = 100) -> List[PostreOut]:
        postres = PostreRepository.get_all(db, skip, limit)
        return [PostreOut.model_validate(p) for p in postres]
    
    @staticmethod
    def get_postres_by_tipo(db: Session, tipo_postre: str) -> List[PostreOut]:
        postres = PostreRepository.get_by_tipo(db, tipo_postre)
        return [PostreOut.model_validate(p) for p in postres]
    
    @staticmethod
    def update_postre(db: Session, postre_id: int, postre_update: PostreUpdate) -> Optional[PostreOut]:
        if postre_update.precio:
            if postre_update.precio.small > postre_update.precio.medium:
                raise ValueError("El precio pequeño no puede ser mayor al mediano")
            if postre_update.precio.medium > postre_update.precio.big:
                raise ValueError("El precio mediano no puede ser mayor al grande")
        
        db_postre = PostreRepository.update(db, postre_id, postre_update)
        if not db_postre:
            return None
        return PostreOut.model_validate(db_postre)
    
    @staticmethod
    def delete_postre(db: Session, postre_id: int) -> bool:
        return PostreRepository.delete(db, postre_id)
