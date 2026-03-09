# Импортируем все модели, чтобы Alembic их видел
from src.models.category import Category
from src.models.product import Product, ProductImage

__all__ = ["Category", "Product", "ProductImage"]
