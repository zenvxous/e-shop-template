package main

import (
	"context"
	"log/slog"
	"os"
	"os/signal"
	"syscall"
	"time"

	"order/internal/app"
	"order/internal/config"
	"order/pkg/logger"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		_, _ = os.Stderr.WriteString(err.Error() + "\n")
		os.Exit(1)
	}

	logger.New(cfg.LogLevel)

	application, err := app.New(cfg)
	if err != nil {
		slog.Error("failed to initialize app", slog.Any("error", err))
		os.Exit(1)
	}

	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	go func() {
		if err := application.Start(); err != nil {
			slog.Error("server stopped with error", slog.Any("error", err))
			stop()
		}
	}()

	<-ctx.Done()

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := application.Shutdown(shutdownCtx); err != nil {
		slog.Error("shutdown error", slog.Any("error", err))
	}
}
