"""
Aplicación FastAPI - Bakery System
Sistema de gestión de panadería con productos y ventas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    producto_router,
    postre_router,
    pan_router,
    bebida_router,
    extra_router,
    venta_router,
)


# Crear aplicación FastAPI
app = FastAPI(
    title="Bakery API",
    description="API para gestión de panadería con productos (postres, pan, bebidas, extras) y ventas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(producto_router)
app.include_router(postre_router)
app.include_router(pan_router)
app.include_router(bebida_router)
app.include_router(extra_router)
app.include_router(venta_router)


@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "message": "Bakery API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Endpoint de health check"""
    return {"status": "healthy"}
