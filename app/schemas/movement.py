from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MovementCreate(BaseModel):
    product_id: int
    type: str           # "IN" o "OUT"
    quantity: int
    reason: Optional[str] = None

class MovementResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    type: str
    quantity: int
    reason: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True