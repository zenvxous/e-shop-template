# Переменные
COMPOSE_FILE := ./infra/docker-compose.yml
PROJECT_NAME := e-shop-template
DOCKER_COMPOSE := docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME)

.PHONY: help
help: ## Показать помощь
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Собрать образы
	$(DOCKER_COMPOSE) build

.PHONY: up
up: ## Запустить все сервисы
	$(DOCKER_COMPOSE) up -d

.PHONY: down
down: ## Остановить все сервисы
	$(DOCKER_COMPOSE) down

.PHONY: restart
restart: down up ## Перезапустить всё

.PHONY: logs
logs: ## Показать логи всех сервисов
	$(DOCKER_COMPOSE) logs -f

.PHONY: ps
ps: ## Статус контейнеров
	$(DOCKER_COMPOSE) ps

.PHONY: clean
clean: ## Удалить контейнеры, сети, volumes
	$(DOCKER_COMPOSE) down -v --remove-orphans

.PHONY: rebuild
rebuild: clean build up ## Полная пересборка
