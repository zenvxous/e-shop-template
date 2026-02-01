#!/bin/sh
set -e

echo "🪣 Initializing MinIO buckets..."

# 1. Настраиваем алиас для MinIO
mc alias set myminio http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

# 2. Ждём готовности MinIO
echo -n "   ├─ Waiting for MinIO to be ready"
retries=30

while ! mc ready myminio >/dev/null 2>&1; do
  retries=$((retries - 1))
  if [ "$retries" -le 0 ]; then
    echo ""
    echo "❌ ERROR: MinIO is not ready after multiple attempts"
    exit 1
  fi
  printf "."
  sleep 2
done
echo " ✓"

# 3. Создаём buckets (идемпотентно)
echo "   ├─ Creating buckets (if missing)..."

mc mb --ignore-existing myminio/product-images
mc mb --ignore-existing myminio/user-avatars
mc mb --ignore-existing myminio/order-invoices

echo "   │   • product-images"
echo "   │   • user-avatars"
echo "   │   • order-invoices"

# 4. Настраиваем права (dev-режим: изображения публичные)
echo "   ├─ Setting access policies..."

# Публичное чтение только для product-images (картинки каталога)
mc anonymous set download myminio/product-images >/dev/null 2>&1 || true

# Остальные buckets приватные по умолчанию (ничего делать не нужно)

echo "   └─ MinIO buckets initialized successfully ✅"
