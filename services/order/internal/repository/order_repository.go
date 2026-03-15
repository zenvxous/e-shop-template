package repository

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"

	"order/internal/domain"
)

type OrderRepository struct {
	db *gorm.DB
}

func NewOrderRepository(db *gorm.DB) *OrderRepository {
	return &OrderRepository{db: db}
}

func (r *OrderRepository) Create(ctx context.Context, order *domain.Order) error {
	return r.db.WithContext(ctx).Create(order).Error
}

func (r *OrderRepository) GetByID(ctx context.Context, orderID uuid.UUID) (domain.Order, error) {
	var order domain.Order
	err := r.db.WithContext(ctx).
		Preload("Items").
		First(&order, "id = ?", orderID).Error
	return order, err
}

func (r *OrderRepository) UpdateStatus(ctx context.Context, orderID uuid.UUID, status domain.OrderStatus) (domain.Order, error) {
	db := r.db.WithContext(ctx)
	if err := db.Model(&domain.Order{}).
		Where("id = ?", orderID).
		Updates(map[string]any{"status": status, "updated_at": gorm.Expr("now()")}).Error; err != nil {
		return domain.Order{}, err
	}
	return r.GetByID(ctx, orderID)
}

func (r *OrderRepository) WithTx(tx *gorm.DB) *OrderRepository {
	return &OrderRepository{db: tx}
}
