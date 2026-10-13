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
    - pnpm vite

tasks-dev:
    - just dj run_huey

mail-dev:
    - mailpit

############
# COMMANDS #
############

# setup the environment for development
setup:
    - uv run scripts/setup.py

test *ARGS:
    - uv run pytest {{ ARGS }}

format:
    - uvx ruff check --fix
    - uvx ruff format
    - pnpx prettier --write .

# start the dev environment
[parallel]
dev: django-dev vite-dev tasks-dev mail-dev

# build assets for production
build:
    - uv sync
    - pnpm i
    - pnpm vite build
    - just dj collectstatic --noinput

# start the production server
prod $DEBUG="false" PORT="8000":
    - uv run waitress-serve --port={{ PORT }} config.wsgi:application

# run the task worker process
tasks *ARGS:
    - just dj run_huey {{ ARGS }}
