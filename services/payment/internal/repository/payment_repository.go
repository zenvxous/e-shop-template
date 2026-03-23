package repository

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"

	"payment/internal/domain"
)

type PaymentRepository struct {
	db *gorm.DB
}

func NewPaymentRepository(db *gorm.DB) *PaymentRepository {
	return &PaymentRepository{db: db}
}

func (r *PaymentRepository) CreateSession(ctx context.Context, s *domain.PaymentSession) error {
	return r.db.WithContext(ctx).Create(s).Error
}

func (r *PaymentRepository) GetSession(ctx context.Context, id uuid.UUID) (domain.PaymentSession, error) {
	var s domain.PaymentSession
	err := r.db.WithContext(ctx).First(&s, "id = ?", id).Error
	return s, err
}

func (r *PaymentRepository) UpdateSessionStatus(ctx context.Context, id uuid.UUID, status domain.PaymentStatus) (domain.PaymentSession, error) {
	db := r.db.WithContext(ctx)
	if err := db.Model(&domain.PaymentSession{}).
		Where("id = ?", id).
		Updates(map[string]any{"status": status, "updated_at": gorm.Expr("now()")}).Error; err != nil {
		return domain.PaymentSession{}, err
	}
	return r.GetSession(ctx, id)
}

func (r *PaymentRepository) CreateEvent(ctx context.Context, e *domain.PaymentEvent) error {
	return r.db.WithContext(ctx).Create(e).Error
}

func (r *PaymentRepository) WithTx(tx *gorm.DB) *PaymentRepository {
	return &PaymentRepository{db: tx}
}
