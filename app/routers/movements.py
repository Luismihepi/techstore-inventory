from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.movement import Movement
from app.models.user import User
from app.schemas.movement import MovementCreate, MovementResponse
from app.services.auth import get_current_user
from app.services.inventory import register_movement

router = APIRouter(
    prefix="/movements",
    tags=["Movements"]
)


# POST /movements — Registrar entrada o salida
@router.post("/", response_model=MovementResponse, status_code=201)
def create_movement(
    movement_data: MovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # employee y admin pueden registrar
):
    return register_movement(movement_data, db, current_user)


# GET /movements — Historial completo con filtros
@router.get("/", response_model=List[MovementResponse])
def get_movements(
    skip: int = Query(0),
    limit: int = Query(20),
    type: Optional[str] = Query(None, description="IN o OUT"),
    product_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Movement)

    if type:
        query = query.filter(Movement.type == type)
    if product_id:
        query = query.filter(Movement.product_id == product_id)

    return query.order_by(Movement.created_at.desc()).offset(skip).limit(limit).all()


# GET /movements/product/{id} — Historial de un producto específico
@router.get("/product/{product_id}", response_model=List[MovementResponse])
def get_product_movements(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Movement).filter(
        Movement.product_id == product_id
    ).order_by(Movement.created_at.desc()).all()