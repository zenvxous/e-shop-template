package handlers

import (
	"order/internal/service"

	"github.com/gofiber/fiber/v3"
)

type Handlers struct {
	Cart  *service.CartService
	Order *service.OrderService

	ServiceName string
}

func New(cart *service.CartService, order *service.OrderService, serviceName string) *Handlers {
	return &Handlers{Cart: cart, Order: order, ServiceName: serviceName}
}

func jsonError(c fiber.Ctx, status int, msg string) error {
	return c.Status(status).JSON(fiber.Map{"error": msg})
}
