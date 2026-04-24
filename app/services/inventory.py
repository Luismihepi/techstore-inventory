from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.product import Product
from app.models.movement import Movement
from app.models.user import User
from app.schemas.movement import MovementCreate

def register_movement(
    movement_data: MovementCreate,
    db: Session,
    current_user: User
) -> Movement:

    # 1. Verifica que el producto existe
    product = db.query(Product).filter(Product.id == movement_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {movement_data.product_id} no encontrado"
        )

    # 2. Verifica que el producto está activo
    if not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden registrar movimientos de un producto inactivo"
        )

    # 3. Valida el tipo de movimiento
    if movement_data.type not in ["IN", "OUT"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El tipo de movimiento debe ser 'IN' (entrada) o 'OUT' (salida)"
        )

    # 4. Si es salida, verifica que hay stock suficiente
    if movement_data.type == "OUT":
        if product.stock < movement_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente. Stock actual: {product.stock}, cantidad solicitada: {movement_data.quantity}"
            )

    # 5. Actualiza el stock según el tipo
    if movement_data.type == "IN":
        product.stock += movement_data.quantity
    else:
        product.stock -= movement_data.quantity

    # 6. Registra el movimiento con el usuario que lo hizo
    new_movement = Movement(
        product_id=movement_data.product_id,
        user_id=current_user.id,
        type=movement_data.type,
        quantity=movement_data.quantity,
        reason=movement_data.reason
    )

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)
    return new_movement