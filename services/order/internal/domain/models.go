package domain

import (
	"time"

	"github.com/google/uuid"
	"github.com/shopspring/decimal"
)

type Cart struct {
	ID        uuid.UUID  `gorm:"type:uuid;default:gen_random_uuid();primaryKey" json:"id"`
	UserID    uuid.UUID  `gorm:"type:uuid;not null;index" json:"user_id"`
	CreatedAt time.Time  `gorm:"type:timestamptz;not null;default:now()" json:"created_at"`
	Items     []CartItem `gorm:"foreignKey:CartID;constraint:OnDelete:CASCADE" json:"items"`
}

type CartItem struct {
	ID        uuid.UUID       `gorm:"type:uuid;default:gen_random_uuid();primaryKey" json:"id"`
	CartID    uuid.UUID       `gorm:"type:uuid;not null;index" json:"cart_id"`
	ProductID uuid.UUID       `gorm:"type:uuid;not null;index" json:"product_id"`
	Quantity  int             `gorm:"not null" json:"quantity"`
	Price     decimal.Decimal `gorm:"type:numeric(10,2);not null" json:"price"`
}

type OrderStatus string

const (
	OrderStatusPending         OrderStatus = "pending"
	OrderStatusAwaitingPayment OrderStatus = "awaiting_payment"
	OrderStatusPaid            OrderStatus = "paid"
	OrderStatusCancelled       OrderStatus = "cancelled"
)

type Order struct {
	ID          uuid.UUID       `gorm:"type:uuid;default:gen_random_uuid();primaryKey" json:"id"`
	UserID      uuid.UUID       `gorm:"type:uuid;not null;index" json:"user_id"`
	Status      OrderStatus     `gorm:"type:text;not null" json:"status"`
	TotalAmount decimal.Decimal `gorm:"type:numeric(10,2);not null" json:"total_amount"`
	CreatedAt   time.Time       `gorm:"type:timestamptz;not null;default:now()" json:"created_at"`
	UpdatedAt   time.Time       `gorm:"type:timestamptz;not null;default:now()" json:"updated_at"`
	Items       []OrderItem     `gorm:"foreignKey:OrderID;constraint:OnDelete:CASCADE" json:"items"`
}

type OrderItem struct {
	ID        uuid.UUID       `gorm:"type:uuid;default:gen_random_uuid();primaryKey" json:"id"`
	OrderID   uuid.UUID       `gorm:"type:uuid;not null;index" json:"order_id"`
	ProductID uuid.UUID       `gorm:"type:uuid;not null;index" json:"product_id"`
	Quantity  int             `gorm:"not null" json:"quantity"`
	UnitPrice decimal.Decimal `gorm:"type:numeric(10,2);not null" json:"unit_price"`
	Subtotal  decimal.Decimal `gorm:"type:numeric(10,2);not null" json:"subtotal"`
}
