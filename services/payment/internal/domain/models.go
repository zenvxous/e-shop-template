package domain

import (
	"time"

	"github.com/google/uuid"
	"github.com/shopspring/decimal"
	"gorm.io/datatypes"
)

type PaymentStatus string

type EventType string

const (
	PaymentStatusPending   PaymentStatus = "pending"
	PaymentStatusSucceeded PaymentStatus = "succeeded"
	PaymentStatusFailed    PaymentStatus = "failed"

	EventTypeCreated   EventType = "created"
	EventTypeConfirmed EventType = "confirmed"
	EventTypeFailed    EventType = "failed"
)

type PaymentSession struct {
	ID        uuid.UUID     `gorm:"type:uuid;default:gen_random_uuid();primaryKey" json:"id"`
	OrderID   uuid.UUID     `gorm:"type:uuid;not null;index" json:"order_id"`
	Amount    decimal.Decimal `gorm:"type:numeric(10,2);not null" json:"amount"`
	Currency  string        `gorm:"type:text;not null" json:"currency"`
	Status    PaymentStatus `gorm:"type:text;not null" json:"status"`
	Provider  string        `gorm:"type:text;not null" json:"provider"`
	CreatedAt time.Time     `gorm:"type:timestamptz;not null;default:now()" json:"created_at"`
	UpdatedAt time.Time     `gorm:"type:timestamptz;not null;default:now()" json:"updated_at"`
}

type PaymentEvent struct {
	ID        uuid.UUID      `gorm:"type:uuid;default:gen_random_uuid();primaryKey" json:"id"`
	SessionID uuid.UUID      `gorm:"type:uuid;not null;index" json:"session_id"`
	EventType EventType      `gorm:"type:text;not null" json:"event_type"`
	Payload   datatypes.JSON `gorm:"type:jsonb;not null" json:"payload"`
	CreatedAt time.Time      `gorm:"type:timestamptz;not null;default:now()" json:"created_at"`
}
