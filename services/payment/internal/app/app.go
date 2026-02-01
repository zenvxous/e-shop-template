package app

import (
	"log"
	"payment/internal/routes"

	"github.com/gofiber/fiber/v2"
)

func App() {
	app := fiber.New()

	routes.SetupRoutes(app)

	log.Fatal(app.Listen(":8004"))
}
