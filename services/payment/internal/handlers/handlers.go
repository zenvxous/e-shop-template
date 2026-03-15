package handlers

import (
	"payment/internal/service"

	"github.com/gofiber/fiber/v3"
)

type Handlers struct {
	Payment *service.PaymentService

	ServiceName string
}

func New(payment *service.PaymentService, serviceName string) *Handlers {
	return &Handlers{Payment: payment, ServiceName: serviceName}
}

func jsonError(c fiber.Ctx, status int, msg string) error {
	return c.Status(status).JSON(fiber.Map{"error": msg})
}
