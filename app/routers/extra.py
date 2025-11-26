
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.extra_service import ExtraService
from app.schemas.extra import ExtraCreate, ExtraUpdate, ExtraOut


router = APIRouter(
    prefix="/extras",
    tags=["extras"]
)


@router.post("/", response_model=ExtraOut, status_code=status.HTTP_201_CREATED)
def create_extra(
    extra: ExtraCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo extra"""
    try:
        return ExtraService.create_extra(db, extra)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{extra_id}", response_model=ExtraOut)
def get_extra(
    extra_id: int,
    db: Session = Depends(get_db)
):
    """Obtener extra por ID"""
    extra = ExtraService.get_extra(db, extra_id)
    if not extra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Extra con ID {extra_id} no encontrado"
        )
    return extra


@router.get("/", response_model=List[ExtraOut])
def get_all_extras(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de extra"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los extras con paginación y filtro opcional por tipo"""
    if tipo:
        return ExtraService.get_extras_by_tipo(db, tipo)
    return ExtraService.get_all_extras(db, skip, limit)


@router.put("/{extra_id}", response_model=ExtraOut)
def update_extra(
    extra_id: int,
    extra_update: ExtraUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un extra"""
    try:
        extra = ExtraService.update_extra(db, extra_id, extra_update)
        if not extra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Extra con ID {extra_id} no encontrado"
            )
        return extra
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{extra_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_extra(
    extra_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un extra"""
    if not ExtraService.delete_extra(db, extra_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Extra con ID {extra_id} no encontrado"
        )
