package routes

import (
	"payment/internal/handlers"

	"github.com/gofiber/fiber/v3"
)

func SetupRoutes(app *fiber.App, h *handlers.Handlers) {
	api := app.Group("")

	api.Get("/health", h.Health)

	pay := api.Group("/payments")
	sessions := pay.Group("/sessions")

	sessions.Post("/", h.CreateSession)
	sessions.Get("/:id", h.GetSession)
	sessions.Post("/:id/confirm", h.ConfirmSession)
}
