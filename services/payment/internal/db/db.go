package db

import (
	"context"
	"database/sql"
	"time"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

type DB struct {
	Gorm *gorm.DB
	SQL  *sql.DB
}

func Connect(dsn string, debug bool) (DB, error) {
	cfg := &gorm.Config{}
	if debug {
		cfg.Logger = logger.Default.LogMode(logger.Info)
	}

	gdb, err := gorm.Open(postgres.Open(dsn), cfg)
	if err != nil {
		return DB{}, err
	}

	sqlDB, err := gdb.DB()
	if err != nil {
		return DB{}, err
	}

	sqlDB.SetMaxOpenConns(20)
	sqlDB.SetMaxIdleConns(10)
	sqlDB.SetConnMaxLifetime(30 * time.Minute)

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := sqlDB.PingContext(ctx); err != nil {
		return DB{}, err
	}

	return DB{Gorm: gdb, SQL: sqlDB}, nil
}
