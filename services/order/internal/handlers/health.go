package handlers

import (
	"log/slog"
	"net/http"

	"github.com/gofiber/fiber/v3"
)

func Health(c fiber.Ctx) error {
	slog.Info(
		"Health check called",
		slog.String("path", c.OriginalURL()),
		slog.String("method", c.Method()),
		slog.Int("status_code", fiber.StatusOK),
		slog.String("status_text", http.StatusText(fiber.StatusOK)),
		slog.String("response_message", "healthy"),
		slog.String("ip", c.IP()),
		slog.String("user_agent", c.Get("User-Agent")),
	)
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"status": "healthy",
	})
}
