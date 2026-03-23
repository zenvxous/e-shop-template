package repository

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"

	"order/internal/domain"
)

type CartRepository struct {
	db *gorm.DB
}

func NewCartRepository(db *gorm.DB) *CartRepository {
	return &CartRepository{db: db}
}

func (r *CartRepository) Create(ctx context.Context, cart *domain.Cart) error {
	return r.db.WithContext(ctx).Create(cart).Error
}

func (r *CartRepository) GetByID(ctx context.Context, cartID uuid.UUID) (domain.Cart, error) {
	var cart domain.Cart
	err := r.db.WithContext(ctx).
		Preload("Items").
		First(&cart, "id = ?", cartID).Error
	return cart, err
}

func (r *CartRepository) AddItem(ctx context.Context, item *domain.CartItem) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *CartRepository) UpdateItemQuantity(ctx context.Context, cartID uuid.UUID, itemID uuid.UUID, quantity int) (domain.CartItem, error) {
	var item domain.CartItem
	db := r.db.WithContext(ctx)
	if err := db.First(&item, "id = ? AND cart_id = ?", itemID, cartID).Error; err != nil {
		return domain.CartItem{}, err
	}
	item.Quantity = quantity
	if err := db.Save(&item).Error; err != nil {
		return domain.CartItem{}, err
	}
	return item, nil
}

func (r *CartRepository) DeleteItem(ctx context.Context, cartID uuid.UUID, itemID uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&domain.CartItem{}, "id = ? AND cart_id = ?", itemID, cartID).Error
}
