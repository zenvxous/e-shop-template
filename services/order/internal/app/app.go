package app

import (
	"log/slog"
	"order/internal/routes"

	"github.com/gofiber/fiber/v3"
)

func App() {
	app := fiber.New()

	routes.SetupRoutes(app)

	slog.Error("Server stopped w an error", slog.Any("error", app.Listen(":8003")))
}
