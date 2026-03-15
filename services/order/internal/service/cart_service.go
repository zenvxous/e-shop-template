package service

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"github.com/shopspring/decimal"

	"order/internal/domain"
	"order/internal/repository"
)

type CartService struct {
	repo *repository.CartRepository
}

func NewCartService(repo *repository.CartRepository) *CartService {
	return &CartService{repo: repo}
}

func (s *CartService) CreateCart(ctx context.Context, userID uuid.UUID) (domain.Cart, error) {
	cart := domain.Cart{UserID: userID}
	if err := s.repo.Create(ctx, &cart); err != nil {
		return domain.Cart{}, err
	}
	cart.Items = []domain.CartItem{}
	return cart, nil
}

func (s *CartService) AddItem(ctx context.Context, cartID uuid.UUID, productID uuid.UUID, quantity int, price decimal.Decimal) (domain.Cart, error) {
	if quantity <= 0 {
		return domain.Cart{}, errors.New("quantity must be > 0")
	}
	item := domain.CartItem{
		CartID:    cartID,
		ProductID: productID,
		Quantity:  quantity,
		Price:     price,
	}
	if err := s.repo.AddItem(ctx, &item); err != nil {
		return domain.Cart{}, err
	}
	return s.repo.GetByID(ctx, cartID)
}

func (s *CartService) UpdateItemQuantity(ctx context.Context, cartID, itemID uuid.UUID, quantity int) (domain.Cart, error) {
	if quantity <= 0 {
		return domain.Cart{}, errors.New("quantity must be > 0")
	}
	if _, err := s.repo.UpdateItemQuantity(ctx, cartID, itemID, quantity); err != nil {
		return domain.Cart{}, err
	}
	return s.repo.GetByID(ctx, cartID)
}

func (s *CartService) DeleteItem(ctx context.Context, cartID, itemID uuid.UUID) error {
	return s.repo.DeleteItem(ctx, cartID, itemID)
}

func (s *CartService) GetCart(ctx context.Context, cartID uuid.UUID) (domain.Cart, error) {
	return s.repo.GetByID(ctx, cartID)
}
