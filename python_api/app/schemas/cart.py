from typing import List

from pydantic import BaseModel, Field

from app.schemas.product import ProductResponse


class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductResponse
    subtotal: float

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_item(cls, item):
        return cls(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product=ProductResponse.model_validate(item.product),
            subtotal=item.quantity * item.product.price,
        )


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]
    subtotal: float

    model_config = {"from_attributes": True}
