package routes

import (
	"order/internal/handlers"

	"github.com/gofiber/fiber/v2"
)

func SetupRoutes(app *fiber.App) {
	api := app.Group("/order/api")

	api.Get("/health", handlers.Health)
}
