package service

import (
	"context"
	"encoding/json"
	"math/rand"
	"time"

	"github.com/google/uuid"
	"github.com/shopspring/decimal"
	"gorm.io/gorm"
	"gorm.io/datatypes"

	"payment/internal/domain"
	"payment/internal/repository"
)

type PaymentService struct {
	db   *gorm.DB
	repo *repository.PaymentRepository
}

func NewPaymentService(db *gorm.DB, repo *repository.PaymentRepository) *PaymentService {
	return &PaymentService{db: db, repo: repo}
}

func (s *PaymentService) CreateSession(ctx context.Context, orderID uuid.UUID, amount decimal.Decimal, currency string) (domain.PaymentSession, error) {
	var created domain.PaymentSession

	err := s.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		session := domain.PaymentSession{
			OrderID:   orderID,
			Amount:    amount,
			Currency:  currency,
			Status:    domain.PaymentStatusPending,
			Provider:  "mock",
		}

		if err := repository.NewPaymentRepository(tx).CreateSession(ctx, &session); err != nil {
			return err
		}

		payloadBytes, _ := json.Marshal(map[string]any{
			"order_id":  orderID.String(),
			"amount":    amount.String(),
			"currency":  currency,
			"provider":  "mock",
			"status":    string(domain.PaymentStatusPending),
			"timestamp": time.Now().UTC().Format(time.RFC3339Nano),
		})

		event := domain.PaymentEvent{
			SessionID: session.ID,
			EventType: domain.EventTypeCreated,
			Payload:   datatypes.JSON(payloadBytes),
		}
		if err := repository.NewPaymentRepository(tx).CreateEvent(ctx, &event); err != nil {
			return err
		}

		created = session
		return nil
	})
	if err != nil {
		return domain.PaymentSession{}, err
	}

	return s.repo.GetSession(ctx, created.ID)
}

func (s *PaymentService) GetSession(ctx context.Context, id uuid.UUID) (domain.PaymentSession, error) {
	return s.repo.GetSession(ctx, id)
}

func (s *PaymentService) ConfirmSession(ctx context.Context, id uuid.UUID) (domain.PaymentSession, error) {
	// 80% success, 20% failure
	// Seed on first use
	rand.Seed(time.Now().UnixNano())

	status := domain.PaymentStatusSucceeded
	eventType := domain.EventTypeConfirmed
	if rand.Float64() >= 0.8 {
		status = domain.PaymentStatusFailed
		eventType = domain.EventTypeFailed
	}

	var updated domain.PaymentSession
	err := s.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		repo := repository.NewPaymentRepository(tx)
		session, err := repo.UpdateSessionStatus(ctx, id, status)
		if err != nil {
			return err
		}

		payloadBytes, _ := json.Marshal(map[string]any{
			"session_id": session.ID.String(),
			"status":     string(status),
			"timestamp":  time.Now().UTC().Format(time.RFC3339Nano),
		})

		event := domain.PaymentEvent{
			SessionID: session.ID,
			EventType: eventType,
			Payload:   datatypes.JSON(payloadBytes),
		}
		if err := repo.CreateEvent(ctx, &event); err != nil {
			return err
		}

		updated = session
		return nil
	})
	if err != nil {
		return domain.PaymentSession{}, err
	}

	return updated, nil
}
