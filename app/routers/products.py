from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
 
from app.services.auth import get_current_user, get_admin_user
from app.models.user import User

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# GET /products — Listar con filtros y paginación
@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, description="Cuántos registros saltar"),
    limit: int = Query(10, description="Cuántos registros traer"),
    category_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    supplier_id: Optional[int] = Query(None, description="Filtrar por proveedor"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado"),
    search: Optional[str] = Query(None, description="Buscar por nombre o SKU"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Product)

    if category_id:
        query = query.filter(Product.category_id == category_id)
    if supplier_id:
        query = query.filter(Product.supplier_id == supplier_id)
    if is_active is not None:
        query = query.filter(Product.is_active == is_active)
    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%") | Product.sku.ilike(f"%{search}%")
        )

    return query.offset(skip).limit(limit).all()


# GET /products/low-stock ⭐ — Productos bajo stock mínimo
# OJO: este endpoint va ANTES de /{product_id} para que no haya conflicto
@router.get("/low-stock", response_model=List[ProductResponse])
def get_low_stock_products(db: Session = Depends(get_db)):
    return db.query(Product).filter(
        Product.stock <= Product.stock_min,
        Product.is_active == True
    ).all()


# GET /products/{id}
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {product_id} no encontrado"
        )
    return product


# POST /products
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, 
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_admin_user)
):

    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# PUT /products/{id}
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, 
                   product_data: ProductUpdate, 
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_admin_user)
):

    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


# DELETE /products/{id}
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_admin_user)
):
    
    db.delete(product)
    db.commit()