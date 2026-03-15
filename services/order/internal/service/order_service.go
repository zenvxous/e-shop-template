package service

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"github.com/shopspring/decimal"
	"gorm.io/gorm"

	"order/internal/domain"
	"order/internal/repository"
)

type OrderService struct {
	db        *gorm.DB
	cartRepo  *repository.CartRepository
	orderRepo *repository.OrderRepository
}

func NewOrderService(db *gorm.DB, cartRepo *repository.CartRepository, orderRepo *repository.OrderRepository) *OrderService {
	return &OrderService{db: db, cartRepo: cartRepo, orderRepo: orderRepo}
}

func (s *OrderService) CreateFromCart(ctx context.Context, cartID uuid.UUID) (domain.Order, error) {
	cart, err := s.cartRepo.GetByID(ctx, cartID)
	if err != nil {
		return domain.Order{}, err
	}
	if len(cart.Items) == 0 {
		return domain.Order{}, errors.New("cart is empty")
	}

	var created domain.Order
	err = s.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		total := decimal.NewFromInt(0)
		items := make([]domain.OrderItem, 0, len(cart.Items))
		for _, it := range cart.Items {
			sub := it.Price.Mul(decimal.NewFromInt(int64(it.Quantity)))
			total = total.Add(sub)
			items = append(items, domain.OrderItem{
				ProductID: it.ProductID,
				Quantity:  it.Quantity,
				UnitPrice: it.Price,
				Subtotal:  sub,
			})
		}

		order := domain.Order{
			UserID:      cart.UserID,
			Status:      domain.OrderStatusPending,
			TotalAmount: total,
			Items:       items,
		}

		if err := repository.NewOrderRepository(tx).Create(ctx, &order); err != nil {
			return err
		}
		created = order
		return nil
	})
	if err != nil {
		return domain.Order{}, err
	}

	return s.orderRepo.GetByID(ctx, created.ID)
}

func (s *OrderService) Get(ctx context.Context, orderID uuid.UUID) (domain.Order, error) {
	return s.orderRepo.GetByID(ctx, orderID)
}

func (s *OrderService) UpdateStatus(ctx context.Context, orderID uuid.UUID, status domain.OrderStatus) (domain.Order, error) {
	if status != domain.OrderStatusPaid && status != domain.OrderStatusCancelled {
		return domain.Order{}, errors.New("status must be paid or cancelled")
	}
	return s.orderRepo.UpdateStatus(ctx, orderID, status)
}
