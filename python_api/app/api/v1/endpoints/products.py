from typing import Optional

from fastapi import APIRouter, Query

from app.core.dependencies import CurrentAdmin, CurrentUser, DBSession
from app.schemas.common import PaginatedResponse
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product import ProductService
import math

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    db: DBSession,
    q: Optional[str] = Query(None, description="Search by name or description"),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List and search products with pagination."""
    service = ProductService(db)
    items, total = await service.search(
        query=q,
        category=category,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size,
    )
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: DBSession):
    """Get product detail."""
    service = ProductService(db)
    return await service.get_or_404(product_id)


@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(data: ProductCreate, db: DBSession, _: CurrentAdmin):
    """Create a product (admin only)."""
    service = ProductService(db)
    return await service.create(data)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, data: ProductUpdate, db: DBSession, _: CurrentAdmin):
    """Update a product (admin only)."""
    service = ProductService(db)
    return await service.update(product_id, data)


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, db: DBSession, _: CurrentAdmin):
    """Delete a product (admin only)."""
    service = ProductService(db)
    await service.delete(product_id)
