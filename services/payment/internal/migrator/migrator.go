package migrator

import (
	"database/sql"

	"github.com/rubenv/sql-migrate"
)

type Migrator struct {
	db   *sql.DB
	path string
}

func New(migrationsPath string, db *sql.DB) *Migrator {
	return &Migrator{db: db, path: migrationsPath}
}

func (mg *Migrator) Up() error {
	if mg == nil || mg.db == nil {
		return nil
	}
	_, err := migrate.Exec(mg.db, "postgres", migrate.FileMigrationSource{Dir: mg.path}, migrate.Up)
	return err
}

func (mg *Migrator) Close() error {
	return nil
}
