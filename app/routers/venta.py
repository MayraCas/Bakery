
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.services.venta_service import VentaService
from app.schemas.venta import VentaCreate, VentaUpdate, VentaOut, InsertarVentaRequest


router = APIRouter(
    prefix="/ventas",
    tags=["ventas"]
)


@router.post("/", response_model=VentaOut, status_code=status.HTTP_201_CREATED)
def create_venta(
    venta: VentaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva venta con sus detalles.
    
    Los triggers de PostgreSQL se encargan automáticamente de:
    - Validar existencia de productos
    - Actualizar stock
    - Calcular precio_total
    """
    try:
        return VentaService.create_venta(db, venta)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/crear", status_code=status.HTTP_201_CREATED)
def insertar_venta_sql(
    request: InsertarVentaRequest,
    db: Session = Depends(get_db)
):
    """
    Crear venta usando la función SQL insertar_venta() de PostgreSQL.
    
    Esta función delega toda la lógica a la base de datos.
    Los triggers manejan automáticamente:
    - Validación de productos
    - Actualización de stock
    - Cálculo de total
    
    Returns:
        ID de la venta creada
    """
    try:
        venta_id = VentaService.insertar_venta_sql(db, request)
        return {"id": venta_id, "message": "Venta creada exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{venta_id}", response_model=VentaOut)
def get_venta(
    venta_id: int,
    db: Session = Depends(get_db)
):
    """Obtener venta por ID con sus detalles"""
    venta = VentaService.get_venta(db, venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta con ID {venta_id} no encontrada"
        )
    return venta


@router.get("/", response_model=List[VentaOut])
def get_all_ventas(
    fecha: Optional[date] = Query(None, description="Filtrar por fecha"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todas las ventas con paginación y filtro opcional por fecha"""
    if fecha:
        return VentaService.get_ventas_by_fecha(db, fecha)
    return VentaService.get_all_ventas(db, skip, limit)


@router.put("/{venta_id}", response_model=VentaOut)
def update_venta(
    venta_id: int,
    venta_update: VentaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una venta (solo detalles y fecha).
    
    NOTA: No se puede modificar precio_total directamente,
    se recalcula automáticamente por trigger.
    """
    try:
        venta = VentaService.update_venta(db, venta_id, venta_update)
        if not venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta con ID {venta_id} no encontrada"
            )
        return venta
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{venta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venta(
    venta_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una venta.
    
    IMPORTANTE: Los triggers devuelven el stock automáticamente.
    """
    if not VentaService.delete_venta(db, venta_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta con ID {venta_id} no encontrada"
        )
