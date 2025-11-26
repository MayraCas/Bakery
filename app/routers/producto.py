
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.producto_service import ProductoService
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoOut


router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)


@router.post("/", response_model=ProductoOut, status_code=status.HTTP_201_CREATED)
def create_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo producto"""
    try:
        return ProductoService.create_producto(db, producto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{producto_id}", response_model=ProductoOut)
def get_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """Obtener producto por ID"""
    producto = ProductoService.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return producto


@router.get("/", response_model=List[ProductoOut])
def get_all_productos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los productos con paginación"""
    return ProductoService.get_all_productos(db, skip, limit)


@router.put("/{producto_id}", response_model=ProductoOut)
def update_producto(
    producto_id: int,
    producto_update: ProductoUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un producto"""
    try:
        producto = ProductoService.update_producto(db, producto_id, producto_update)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
        return producto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un producto"""
    if not ProductoService.delete_producto(db, producto_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
