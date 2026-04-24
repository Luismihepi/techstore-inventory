from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Lo que llega cuando CREAS una categoría
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Lo que llega cuando ACTUALIZAS (todo opcional)
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Lo que la API DEVUELVE al cliente
class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  # Permite convertir modelo SQLAlchemy a Pydantic