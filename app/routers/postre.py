"""
Router para Postre
Endpoints CRUD para postres
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.postre_service import PostreService
from app.schemas.postre import PostreCreate, PostreUpdate, PostreOut


router = APIRouter(
    prefix="/postres",
    tags=["postres"]
)


@router.post("/", response_model=PostreOut, status_code=status.HTTP_201_CREATED)
def create_postre(
    postre: PostreCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo postre"""
    try:
        return PostreService.create_postre(db, postre)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{postre_id}", response_model=PostreOut)
def get_postre(
    postre_id: int,
    db: Session = Depends(get_db)
):
    """Obtener postre por ID"""
    postre = PostreService.get_postre(db, postre_id)
    if not postre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Postre con ID {postre_id} no encontrado"
        )
    return postre


@router.get("/", response_model=List[PostreOut])
def get_all_postres(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de postre"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los postres con paginación y filtro opcional por tipo"""
    if tipo:
        return PostreService.get_postres_by_tipo(db, tipo)
    return PostreService.get_all_postres(db, skip, limit)


@router.put("/{postre_id}", response_model=PostreOut)
def update_postre(
    postre_id: int,
    postre_update: PostreUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un postre"""
    try:
        postre = PostreService.update_postre(db, postre_id, postre_update)
        if not postre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Postre con ID {postre_id} no encontrado"
            )
        return postre
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{postre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_postre(
    postre_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un postre"""
    if not PostreService.delete_postre(db, postre_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Postre con ID {postre_id} no encontrado"
        )
