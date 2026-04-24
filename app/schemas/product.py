from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    price: float
    stock: int = 0
    stock_min: int = 5
    serial_required: bool = False
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_min: Optional[int] = None
    serial_required: Optional[bool] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    is_active: Optional[bool] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    sku: str
    price: float
    stock: int
    stock_min: int
    serial_required: bool
    is_active: bool
    category_id: Optional[int]
    supplier_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True