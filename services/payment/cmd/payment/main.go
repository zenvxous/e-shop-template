package main

import (
	"payment/internal/app"
	"payment/pkg/logger"
)

func main() {
	logger.New()
	app.App()
}
