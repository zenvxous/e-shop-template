package handlers

import "github.com/gofiber/fiber/v3"

// Health is kept for backward compatibility with the initial project scaffold.
// New implementation is Handlers.Health which also returns the service name.
func Health(c fiber.Ctx) error {
	return c.Status(fiber.StatusOK).JSON(fiber.Map{"status": "healthy"})
}
