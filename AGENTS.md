# AGENTS.md

## Project context

This repository is a Django-based math learning app called Diskmatte. The initial goal is to support:

- user accounts and authentication
- chapters and math task from a university math course
- progress tracking and stats
- leaderboards and gamification

## Working rules for AI coding agents

- Keep changes small and focused.
- Prefer Django app separation by domain
- Keep business logic in services or helper modules rather than putting everything in views.
- Add tests for new features whenever possible.
- Update the planning documents in docs/ before implementing larger features.
- Preserve a clear separation between presentation, business logic, and data models.
- Do not commit secrets. Use environment variables for configuration.

## Recommended workflow

1. Read the requirements and plan docs before coding.
2. Implement one slice of functionality from docs/backlog.md at a time.
3. Verify with Django tests or manage.py checks.
4. Update docs if the scope changes or new tasks need to be added to docs/backlog.md
