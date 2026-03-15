package handlers

import "github.com/gofiber/fiber/v3"

func (h *Handlers) Health(c fiber.Ctx) error {
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"status":  "healthy",
		"service": h.ServiceName,
	})
}
