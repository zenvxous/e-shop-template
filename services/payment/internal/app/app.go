package app

import (
	"log"
	"payment/internal/handlers"

	"github.com/gofiber/fiber/v2"
)

func setupRoutes(app *fiber.App) {
	api := app.Group("/api")

	api.Get("/health", handlers.Health)
}

func App() {
	app := fiber.New()

	setupRoutes(app)

	log.Fatal(app.Listen(":8000"))
}
