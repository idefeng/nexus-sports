.PHONY: help install init dev backend frontend watcher backup test lint clean

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# ── Setup ────────────────────────────────────────────────────
install: ## Install all dependencies (Python + Node.js)
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	cd webapp && npm install

init: ## Initialize database
	. .venv/bin/activate && PYTHONPATH=. python backend/init_db.py

# ── Development ──────────────────────────────────────────────
dev: ## Start both backend + frontend (requires 2 terminals)
	@echo "Run in separate terminals:"
	@echo "  make backend"
	@echo "  make frontend"

backend: ## Start backend API server
	. .venv/bin/activate && uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir backend

frontend: ## Start React webapp dev server
	cd webapp && npm run dev

watcher: ## Start auto-import watcher (default: ./data/auto_import)
	. .venv/bin/activate && PYTHONPATH=. python backend/services/watcher.py --dir ./data/auto_import

# ── Operations ───────────────────────────────────────────────
backup: ## Create backup of database and archived files
	. .venv/bin/activate && PYTHONPATH=. python backend/services/backup.py

build: ## Build frontend for production
	cd webapp && npm run build

# ── Quality ──────────────────────────────────────────────────
test: ## Run backend tests
	. .venv/bin/activate && PYTHONPATH=. python -m pytest tests/ -v

lint: ## Lint frontend code
	cd webapp && npm run lint

# ── Cleanup ──────────────────────────────────────────────────
clean: ## Remove generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
