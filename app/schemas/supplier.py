from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class SupplierCreate(BaseModel):
    name: str
    contact: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class SupplierResponse(BaseModel):
    id: int
    name: str
    contact: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True