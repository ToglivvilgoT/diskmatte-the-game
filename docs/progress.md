# Progress app plan

## Purpose

The progress app is responsible for tracking user advancement and gamified learning progress.

## Responsibilities

- track solved tasks and completion progress
- store user score and related stats
- support streaks, achievements, or badges later
- provide data for personal dashboards and leaderboards

## Main models

- UserProgress
- Achievement or Badge (later)

## Main views / features

- progress dashboard
- stats overview
- recent activity view

## Boundaries

The progress app should not handle:

- authentication
- course content creation
- task content definition

## Dependencies

- may read data from the tasks app
- may be used by the leaderboard app
