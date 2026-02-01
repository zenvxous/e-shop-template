#!/bin/bash

set -e

check_required_var() {
	local var_name="$1"
	local var_value="${!var_name}"
	if [ -z "$var_value" ]; then
		echo "ERROR: Required variable $var_name is not set"
		exit 1
	fi
}

check_required_var "POSTGRES_USER"
check_required_var "KC_DB_PASS"

echo "🔧 Starting databases initialization..."

echo -n "Checking PostgreSQL connection... "
if ! psql -U "$POSTGRES_USER" -c 'SELECT 1' >/dev/null 2>&1; then
	echo "❌ FAILED"
	echo "ERROR: Cannot connect to PostgreSQL"
	exit 1
fi
echo "✓"

echo ""

DATABASES=(
	"users_db:user_svc:${USER_DB_PASS:-user_pass}"
	"catalog_db:catalog_svc:${CATALOG_DB_PASS:-catalog_pass}"
	"orders_db:order_svc:${ORDER_DB_PASS:-order_pass}"
	"payments_db:payment_svc:${PAYMENT_DB_PASS:-payment_pass}"
	"keycloak_db:keycloak_svc:${KC_DB_PASS}"
)

for entry in "${DATABASES[@]}"; do

	IFS=':' read -r db user pass <<< "$entry"

	echo "📦 Processing: $db"
	echo "   └─ User: $user"

	echo -n "   ├─ Creating database... "
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" >/dev/null 2>&1 <<-EOSQL
		SELECT 'CREATE DATABASE $db'
		WHERE NOT EXISTS (
			SELECT FROM pg_database WHERE datname = '$db'
		);
		\gexec
EOSQL
	echo "✓"

	echo -n "   ├─ Creating user... "	
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" >/dev/null 2>&1 <<-EOSQL
		DO \$\$
		BEGIN
			IF NOT EXISTS (
				SELECT FROM pg_catalog.pg_roles
				WHERE rolname = '$user'
			) THEN
				CREATE USER $user WITH PASSWORD '$pass';
				RAISE NOTICE 'User $user created';
			ELSE
				RAISE NOTICE 'User $user already exists';
			END IF;
		END
		\$\$;

		GRANT ALL PRIVILEGES ON DATABASE $db TO $user;
EOSQL
	echo "✓"

	echo -n "   └─ Granting privileges... "
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$db" >/dev/null 2>&1 <<-EOSQL
		GRANT ALL ON SCHEMA public TO $user;
		GRANT ALL ON ALL TABLES IN SCHEMA public TO $user;
		GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO $user;

		ALTER DEFAULT PRIVILEGES IN SCHEMA public 
			GRANT ALL ON TABLES TO $user;

		ALTER DEFAULT PRIVILEGES IN SCHEMA public
			GRANT ALL ON SEQUENCES TO $user;

		ALTER DATABASE $db OWNER TO postgres;
EOSQL
	echo "✓"
	echo ""
done

echo ""
echo "✅ All databases initialized successfully!"
