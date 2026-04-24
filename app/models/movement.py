from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(10), nullable=False)       # "IN" entrada o "OUT" salida
    quantity = Column(Integer, nullable=False)
    reason = Column(Text, nullable=True)            # "Compra a proveedor", "Venta", etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Llaves foráneas
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relaciones
    product = relationship("Product", back_populates="movements")
    user = relationship("User", back_populates="movements")