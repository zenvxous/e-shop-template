import uuid
from fastapi import HTTPException, status

from src.repo.category import CategoryRepository
from src.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate, CategoryTree


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def create(self, data: CategoryCreate) -> CategoryRead:
        existing = await self.repo.get_by_slug(data.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category with slug='{data.slug}' already exists",
            )
        category = await self.repo.create(data)
        return CategoryRead.model_validate(category)

    async def get(self, category_id: uuid.UUID) -> CategoryRead:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return CategoryRead.model_validate(category)

    async def get_tree(self) -> list[CategoryTree]:
        """Дерево: только корни, children подгружаются через relationship"""
        roots = await self.repo.get_roots()
        return [CategoryTree.model_validate(c) for c in roots]

    async def update(self, category_id: uuid.UUID, data: CategoryUpdate) -> CategoryRead:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        if data.slug:
            existing = await self.repo.get_by_slug(data.slug)
            if existing and existing.id != category_id:
                raise HTTPException(status_code=409, detail="Slug already taken")

        category = await self.repo.update(category, data)
        return CategoryRead.model_validate(category)

    async def delete(self, category_id: uuid.UUID) -> None:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await self.repo.delete(category)
