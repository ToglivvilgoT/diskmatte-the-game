# AGENTS.md

## Project context

This repository is a Django-based math learning app called Diskmatte. The initial goal is to support:

- user accounts and authentication
- chapters and math task from a university math course
- progress tracking and stats
- leaderboards and gamification

## Working rules for AI coding agents

- Keep changes small and focused.
- The app's user-facing language is Swedish. All text visible to users, including UI labels, messages, help text, validation errors, and other rendered content, must be in Swedish. Keep code, code comments, developer-only documentation, and other content intended only for developers or exposed through tools such as the browser inspector in English.
- Prefer Django app separation by domain
- Keep business logic in services or helper modules rather than putting everything in views.
- Never hand-write Django migration files. Change models first, then generate migrations with `python manage.py makemigrations`.
- Treat `apps/*/migrations/*.py` as generated artifacts. Only edit an existing migration manually if the user explicitly asks for that and the reason is documented in the task.
- If Python code changes, run mypy for the affected scope before finishing. When in doubt, run `..\venv\Scripts\python.exe -m mypy .` from the Django project directory.
- Add tests for new features whenever possible.
- Update the planning documents in docs/ before implementing larger features.
- Preserve a clear separation between presentation, business logic, and data models.
- Do not commit secrets. Use environment variables for configuration.

## Repository layout and validation

- The workspace root contains the `venv` virtual environment. The Django project
    root is the nested `diskmatte-the-game/` directory containing `manage.py`.
- From the workspace root, run Django commands with
    `Push-Location diskmatte-the-game; ..\venv\Scripts\python.exe manage.py <command>; Pop-Location`.
- From the workspace root, run mypy with
    `Push-Location diskmatte-the-game; ..\venv\Scripts\python.exe -m mypy .; Pop-Location`.
- Skin metadata format and synchronization behavior are documented in
    `diskmatte-the-game/static/cosmetics/skins/metadata_template_docs.md`.
- Task metadata format and synchronization behavior are documented in
    `diskmatte-the-game/static/tasks/metadata_template_docs.md`.

## Recommended workflow

1. Read the requirements and plan docs before coding.
2. Implement one slice of functionality from docs/backlog.md at a time.
3. If models change, run `python manage.py makemigrations` and review the generated migration before continuing.
4. If Python code changes, run mypy before continuing.
5. Verify with Django tests or manage.py checks.
6. Update docs if the scope changes or new tasks need to be added to docs/backlog.md
