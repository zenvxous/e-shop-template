package app

import (
	"context"
	"fmt"
	"log/slog"
	"strings"
	"time"

	"order/internal/config"
	"order/internal/db"
	"order/internal/handlers"
	"order/internal/migrator"
	"order/internal/repository"
	"order/internal/routes"
	"order/internal/service"

	"github.com/gofiber/fiber/v3"
)

type App struct {
	cfg config.Config
	app *fiber.App
	db  db.DB
	mg  *migrator.Migrator
}

func New(cfg config.Config) (*App, error) {
	debug := strings.EqualFold(cfg.LogLevel, "debug")

	gdb, err := db.Connect(cfg.DatabaseURL, debug)
	if err != nil {
		return nil, err
	}

	mg := migrator.New(cfg.MigrationsPath, gdb.SQL)
	if err := mg.Up(); err != nil {
		_ = gdb.SQL.Close()
		return nil, err
	}

	cartRepo := repository.NewCartRepository(gdb.Gorm)
	orderRepo := repository.NewOrderRepository(gdb.Gorm)

	cartSvc := service.NewCartService(cartRepo)
	orderSvc := service.NewOrderService(gdb.Gorm, cartRepo, orderRepo)

	h := handlers.New(cartSvc, orderSvc, cfg.ServiceName)

	fiberApp := fiber.New(fiber.Config{
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	})

	routes.SetupRoutes(fiberApp, h)

	return &App{cfg: cfg, app: fiberApp, db: gdb, mg: mg}, nil
}

func (a *App) Start() error {
	addr := fmt.Sprintf(":%d", a.cfg.Port)
	slog.Info("starting server", slog.String("addr", addr))
	return a.app.Listen(addr)
}

func (a *App) Shutdown(ctx context.Context) error {
	if a == nil {
		return nil
	}

	errCh := make(chan error, 1)
	go func() {
		errCh <- a.app.Shutdown()
	}()

	select {
	case <-ctx.Done():
		return ctx.Err()
	case err := <-errCh:
		if err != nil {
			return err
		}
	}

	if a.db.SQL != nil {
		_ = a.db.SQL.Close()
	}
	if a.mg != nil {
		_ = a.mg.Close()
	}

	return nil
}
