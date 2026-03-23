###################
# HELPER COMMANDS #
###################

# run django manage.py commands
dj +ARGS:
    - uv run manage.py {{ ARGS }}

migrate:
    - just dj createcachetable
    - just dj migrate

# run the django dev server
django-dev $DEBUG="true":
    - just dj runserver

# run the vite asset server
vite-dev:
    - bun run vite

tasks-dev:
    - just dj run_huey

mail-dev:
    - mailpit

############
# COMMANDS #
############

# setup the environment for development
setup:
    - uv sync
    - bun i
    - cp --update=none .env.example .env
    - sed "s/SECRET_KEY=\"\"/SECRET_KEY=\"$(uv run python -c 'import secrets; print(secrets.token_urlsafe(32))')\"/g" --in-place .env
    - uvx prek install
    - just migrate
    - just build

# start the dev environment
[parallel]
dev: django-dev vite-dev tasks-dev mail-dev

# build assets for production
build:
    - bun run vite build
    - just dj collectstatic --noinput

# start the production server
serve $DEBUG="false" PORT="8000":
    - waitress-serve --port={{ PORT }} config.wsgi:application

# run the task worker process
tasks *ARGS:
    - just dj run_huey {{ ARGS }}
