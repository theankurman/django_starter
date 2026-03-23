# AGENTS.md - Agentic Coding Guidelines

This document provides guidelines for AI agents working in this Django starter project.

## Project Overview

- **Framework**: Django 6.0
- **Python**: 3.14+
- **Frontend**: Vite + TailwindCSS + DaisyUI
- **Task Queue**: Huey
- **Testing**: pytest + pytest-django

## Build/Lint/Test Commands

### Setup environment

```bash
# installs dependencies, setups .env file, setups git pre-commit hooks, migrates database and generates assets
just setup
```

### Development Server

```bash
# Full dev environment (Django + Vite + Huey + Mailpit)
just dev
```

### Testing

```bash
# Run all tests
# Passes all arguments to pytest
just test

# Run a specific test
just test path/to/app -k "test_function_name"
```

### Linting & Formatting

```bash
# Format all files
just format
```

### Database

```bash
# Run migrations
just migrate

# Create a new migration
just dj makemigrations
```

### Build & Deploy

```bash
# Build assets for production
just build
```

## Code Style Guidelines

### Types

- Use type hints for all function signatures
- Prefer `python union` syntax for union types (Python 3.14+)

```python
# Good
def process_user(user_id: int) -> User | None:
    return User.objects.get_or_none(id=user_id)
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `UserProfile`)
- **Functions/variables**: `snake_case` (e.g., `get_user_profile`)
- **Constants**: `SCREAMING_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Django models**: Use singular names (e.g., `User`, not `Users`)
- **Database tables**: Explicitly set with `Meta.db_table`

### Django Patterns

- All urls defined in `config/urls.py`
- Urls should be namespaced like so `appname.namespace.viewname`
- Use class based views. Prefer generic views
- Use `related_name` on ForeignKey/ManyToMany relationships

```python
class User(AbstractUser):
    class Meta:
        db_table = "auth_user"
```

### Error Handling

- Use try/except sparingly, prefer Django's built-in error handling

### Templates

- Use Django templates
- Keep logic in views/forms, not templates
- All apps should have layout templates that extend the `core/layouts/base.html` template.
- All templates should extend a layout in their app.
- Prettier formats HTML/Jinja templates automatically

### JavaScript/TypeScript

- **Formatter**: Prettier with tab width 4
- Use vanilla typescript with Vite (no React/Vue)
- alpine-js may be used sparingly for frontend interactivity.

### CSS

- TailwindCSS v4 with DaisyUI
- Use utility classes in templates, prefer daisyui components over building custom components

### Background Tasks

- Use Huey task queue (`backgroundtasks/tasks.py`)
- Use the `@task()` or `@db_task()` decorator from `huey.contrib.djhuey` for async tasks
- Email is sent via background tasks

## Project Structure

```
django_starter/
├── config/           # Django project settings
├── core/             # Django app for shared logic between apps
    ├── resources/    # Frontend source files (js and css)
    ├── static/       # Custom static files (all apps have this folder)
    ├── templates/    # Django templates for this app (all apps have this folder)
├── users/            # Django app for users
├── backgroundtasks/  # Django app for background tasks
├── ...other django apps
```

## Common Tasks

### Run a python script / command

```bash
# prefix all python commands with uv run
uv run python ...
# run manage.py
just dj ...
```

### Create a new Django app

```bash
just dj startapp newapp
# Add to INSTALLED_APPS in config/settings.py
```

### Add a new model

1. Create model in `app/models.py`
2. Run `just dj makemigrations`
3. Run `just migrate`
4. Register in `app/admin.py`

Copy from `.env.example` and fill in values.

## Dependencies

- Add new python dependency: `uv add package_name`
- Add new js dependency: `bun add package_name`
