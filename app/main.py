from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Category, Supplier, Product, User, Movement
from app.routers import categories, suppliers, products, auth, movements
from app.config import settings

# Esto crea las tablas automáticamente al iniciar (por ahora)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TechStore Inventory API",
    description="Sistema de gestión de inventario para tienda de tecnología",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(suppliers.router)   
app.include_router(products.router)
app.include_router(movements.router) 

@app.get("/")
def root():
    return {
        "message": "TechStore Inventory API funcionando ✅",
        "docs": "/docs",
        "version": "1.0.0"
    }