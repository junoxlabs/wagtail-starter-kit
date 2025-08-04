MAKEFLAGS += -j4

.PHONY: frontend-install frontend-build frontend-dev django-dev django-install install dev

# runs django and frontend dev servers parallelly 
dev: django-dev frontend-dev

install: django-install frontend-install

django-install:
	uv sync --locked

django-dev:
	uv run python manage.py runserver

frontend-install:
	cd apps/frontend/static_src && bun --bun install

frontend-build: # uses node 22 (bun doesn't work with webpack yet)
	cd apps/frontend/static_src && rm -r ../build && bun run build 

frontend-dev:
	cd apps/frontend/static_src && rm -r ../build && bun run dev