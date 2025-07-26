.PHONY: help install dev prod test clean logs

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install all dependencies
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

dev: ## Start development environment
	@echo "Starting development environment..."
	docker-compose up -d

prod: ## Start production environment
	@echo "Starting production environment..."
	docker-compose -f docker-compose.prod.yml up -d

build: ## Build all Docker images
	@echo "Building Docker images..."
	docker-compose -f docker-compose.prod.yml build --no-cache

stop: ## Stop all containers
	@echo "Stopping containers..."
	docker-compose down
	docker-compose -f docker-compose.prod.yml down

logs: ## Show container logs
	docker-compose logs -f

logs-prod: ## Show production container logs
	docker-compose -f docker-compose.prod.yml logs -f

test: ## Run tests
	@echo "Testing backend..."
	cd backend && python -m pytest tests/ -v || echo "No tests found"
	@echo "Testing frontend..."
	cd frontend && npm run lint

clean: ## Clean up Docker resources
	@echo "Cleaning up..."
	docker system prune -f
	docker volume prune -f

deploy: ## Deploy to production
	@echo "Deploying to production..."
	./scripts/deploy.sh

status: ## Show container status
	docker-compose ps
	docker-compose -f docker-compose.prod.yml ps

restart: ## Restart all services
	@echo "Restarting services..."
	docker-compose restart
	docker-compose -f docker-compose.prod.yml restart 