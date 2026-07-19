# Architecture overview

## Suggested project structure

```text
.diskmatte-the-game/
  AGENTS.md
  README.md
  manage.py
  docs/
    requirements.md
    architecture.md
    implementation-plan.md
    backlog.md
  diskmatte/
    settings.py
    urls.py
    wsgi.py
  apps/
    accounts/
    courses/
    tasks/
    progress/
    leaderboard/
  templates/
  static/
  tests/
```

## Suggested Django app responsibilities

- accounts: profile, user settings
- courses: course and chapter data
- tasks: problem definitions and answer validation
- progress: user attempts, solved tasks, streaks, stats
- leaderboard: ranking and gamification display

## Suggested models

- UserProfile or custom user model
- Course
- Chapter
- Task
- Attempt
- UserProgress
- Badge or reward (later)

## Development approach

- Use Django views for request handling.
- Keep logic in service functions or helper modules.
- Use templates for HTML rendering unless a frontend framework is introduced later.
- Use Django forms for task input and authentication.
