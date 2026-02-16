package main

import (
	"order/internal/app"
	"order/pkg/logger"
)

func main() {
	logger.New()
	app.App()
}
