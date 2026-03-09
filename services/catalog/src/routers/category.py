import uuid
from fastapi import APIRouter, Depends, status

from src.dep import get_category_service
from src.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate, CategoryTree
from src.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/tree", response_model=list[CategoryTree])
async def get_tree(service: CategoryService = Depends(get_category_service)):
    return await service.get_tree()


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: uuid.UUID,
    service: CategoryService = Depends(get_category_service),
):
    return await service.get(category_id)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    return await service.create(data)


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: uuid.UUID,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    return await service.update(category_id, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: uuid.UUID,
    service: CategoryService = Depends(get_category_service),
):
    await service.delete(category_id)
