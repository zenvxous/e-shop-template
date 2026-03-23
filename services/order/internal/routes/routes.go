package routes

import (
	"order/internal/handlers"

	"github.com/gofiber/fiber/v3"
)

func SetupRoutes(app *fiber.App, h *handlers.Handlers) {
	api := app.Group("")

	api.Get("/health", h.Health)

	api.Post("/carts", h.CreateCart)
	api.Post("/carts/:cart_id/items", h.AddCartItem)
	api.Patch("/carts/:cart_id/items/:item_id", h.UpdateCartItem)
	api.Delete("/carts/:cart_id/items/:item_id", h.DeleteCartItem)

	api.Post("/orders", h.CreateOrder)
	api.Get("/orders/:order_id", h.GetOrder)
	api.Patch("/orders/:order_id/status", h.UpdateOrderStatus)
}
