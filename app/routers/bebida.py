
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.bebida_service import BebidaService
from app.schemas.bebida import BebidaCreate, BebidaUpdate, BebidaOut


router = APIRouter(
    prefix="/bebidas",
    tags=["bebidas"]
)


@router.post("/", response_model=BebidaOut, status_code=status.HTTP_201_CREATED)
def create_bebida(
    bebida: BebidaCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva bebida"""
    try:
        return BebidaService.create_bebida(db, bebida)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{bebida_id}", response_model=BebidaOut)
def get_bebida(
    bebida_id: int,
    db: Session = Depends(get_db)
):
    """Obtener bebida por ID"""
    bebida = BebidaService.get_bebida(db, bebida_id)
    if not bebida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bebida con ID {bebida_id} no encontrado"
        )
    return bebida


@router.get("/", response_model=List[BebidaOut])
def get_all_bebidas(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de bebida"),
    fria: Optional[bool] = Query(None, description="Filtrar por temperatura (true=fría, false=caliente)"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todas las bebidas con paginación y filtros opcionales"""
    if tipo:
        return BebidaService.get_bebidas_by_tipo(db, tipo)
    if fria is not None:
        if fria:
            return BebidaService.get_bebidas_frias(db)
        else:
            return BebidaService.get_bebidas_calientes(db)
    return BebidaService.get_all_bebidas(db, skip, limit)


@router.put("/{bebida_id}", response_model=BebidaOut)
def update_bebida(
    bebida_id: int,
    bebida_update: BebidaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una bebida"""
    try:
        bebida = BebidaService.update_bebida(db, bebida_id, bebida_update)
        if not bebida:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bebida con ID {bebida_id} no encontrado"
            )
        return bebida
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{bebida_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bebida(
    bebida_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar una bebida"""
    if not BebidaService.delete_bebida(db, bebida_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bebida con ID {bebida_id} no encontrado"
        )
