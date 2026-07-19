# Courses app plan

## Purpose

The courses app is responsible for the curriculum structure of the math app.

## Responsibilities

- represent courses
- represent chapters within courses
- expose course and chapter lists
- provide the structure needed for task organization

## Main models

- Course
- Chapter

## Main views / features

- course listing page
- chapter listing page
- course detail page

## Boundaries

The courses app should not handle:

- authentication
- task solving logic
- user scoring or leaderboard ranking

## Dependencies

- may be referenced by the tasks app
- may be used by the progress app for context on completed content
