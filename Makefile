MAKEFLAGS += -j4

.PHONY: frontend-install frontend-build frontend-dev django-dev django-install install i dev

# runs django and frontend dev servers parallelly
dev: vite-dev django-dev

i: install
install: django-install frontend-install

### cleans up the build artifacts and virtual environment
.PHONY: clean clean-venv clean-frontend-build clean-frontend-node-modules
clean: clean-frontend-build clean-venv clean-frontend-node-modules

clean-venv:
	rm -r .venv

clean-frontend-build:
	cd frontend && rm -r ./dist

clean-frontend-node-modules:
	cd frontend && rm -r node_modules

### installs the virtual environment and dependencies
django-install:
	uv sync --locked

django-dev:
	uv run granian --reload --interface asginl --workers 1 --runtime-threads 2 config.asgi:application

frontend-install:
	cd frontend && bun --bun install

vite-build:
	cd frontend && bun --bun run build

vite-dev:
	cd frontend && bun --bun run dev


makemigrations make migrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --no-input --clear

prod-start:
	env ENVIRONMENT=production uv run granian \
		--interface asginl \
 		--workers 3 \
 		--runtime-mode mt \
 		--host 0.0.0.0 \
 		--port 8000 \
 		config.asgi:application
