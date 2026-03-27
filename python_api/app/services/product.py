from typing import Optional, Tuple, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.product import Product
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: AsyncSession):
        self.repo = ProductRepository(db)

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        return await self.repo.create(product)

    async def get_or_404(self, product_id: int) -> Product:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Product not found")
        return product

    async def search(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Product], int]:
        skip = (page - 1) * page_size
        return await self.repo.search(
            query=query,
            category=category,
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=page_size,
        )

    async def update(self, product_id: int, data: ProductUpdate) -> Product:
        product = await self.get_or_404(product_id)
        return await self.repo.update(product, data.model_dump(exclude_none=True))

    async def delete(self, product_id: int) -> None:
        product = await self.get_or_404(product_id)
        await self.repo.delete(product)
