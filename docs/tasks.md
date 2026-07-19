# Tasks app plan

## Purpose

The tasks app is responsible for math problems and the task-solving experience.

## Responsibilities

- define tasks and their content
- manage answer submission and validation
- record attempts and outcomes
- expose task pages for users

## Main models

- Task
- TaskAttempt

## Main views / features

- task detail page
- answer submission flow
- feedback after solving

## Boundaries

The tasks app should not handle:

- user authentication logic
- general leaderboard display
- long-term progress summaries unless they are directly tied to the attempt result

## Dependencies

- may depend on the courses app for chapter and course context
- may update progress information for the user after a completed attempt
