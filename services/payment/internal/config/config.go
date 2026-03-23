package config

import (
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Config struct {
	ServiceName string
	Port        int
	LogLevel    string

	DatabaseURL string

	MigrationsPath string
}

func Load() (Config, error) {
	cfg := Config{
		ServiceName:    "payment-service",
		Port:           8004,
		LogLevel:       "info",
		MigrationsPath: "migrations",
	}

	if v := strings.TrimSpace(os.Getenv("PORT")); v != "" {
		p, err := strconv.Atoi(v)
		if err != nil {
			return Config{}, fmt.Errorf("invalid PORT: %w", err)
		}
		cfg.Port = p
	}

	if v := strings.TrimSpace(os.Getenv("LOG_LEVEL")); v != "" {
		cfg.LogLevel = v
	}

	cfg.DatabaseURL = strings.TrimSpace(os.Getenv("DATABASE_URL"))
	if cfg.DatabaseURL == "" {
		return Config{}, errors.New("DATABASE_URL is required")
	}
	if !strings.HasPrefix(cfg.DatabaseURL, "postgresql://") && !strings.HasPrefix(cfg.DatabaseURL, "postgres://") {
		return Config{}, errors.New("DATABASE_URL must start with postgresql:// or postgres://")
	}

	if v := strings.TrimSpace(os.Getenv("MIGRATIONS_PATH")); v != "" {
		cfg.MigrationsPath = v
	}

	return cfg, nil
}
