
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.pan_service import PanService
from app.schemas.pan import PanCreate, PanUpdate, PanOut


router = APIRouter(
    prefix="/pan",
    tags=["pan"]
)


@router.post("/", response_model=PanOut, status_code=status.HTTP_201_CREATED)
def create_pan(
    pan: PanCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo pan"""
    try:
        return PanService.create_pan(db, pan)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{pan_id}", response_model=PanOut)
def get_pan(
    pan_id: int,
    db: Session = Depends(get_db)
):
    """Obtener pan por ID"""
    pan = PanService.get_pan(db, pan_id)
    if not pan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pan con ID {pan_id} no encontrado"
        )
    return pan


@router.get("/", response_model=List[PanOut])
def get_all_panes(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de pan (Dulce/Salado)"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los panes con paginación y filtro opcional por tipo"""
    if tipo:
        return PanService.get_panes_by_tipo(db, tipo)
    return PanService.get_all_panes(db, skip, limit)


@router.put("/{pan_id}", response_model=PanOut)
def update_pan(
    pan_id: int,
    pan_update: PanUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un pan"""
    try:
        pan = PanService.update_pan(db, pan_id, pan_update)
        if not pan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pan con ID {pan_id} no encontrado"
            )
        return pan
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{pan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pan(
    pan_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un pan"""
    if not PanService.delete_pan(db, pan_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pan con ID {pan_id} no encontrado"
        )
