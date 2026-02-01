package app

import (
	"log"
	"order/internal/routes"

	"github.com/gofiber/fiber/v2"
)

func App() {
	app := fiber.New()

	routes.SetupRoutes(app)

	log.Fatal(app.Listen("0.0.0.0:8003"))
}
