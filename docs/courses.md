# Courses app plan

## Purpose

The courses app is responsible for the curriculum structure of the math app.

## Responsibilities

- represent courses
- represent learning sets within a course, such as course book, daily task, or exam questions
- represent chapters within a learning set
- expose course, learning set, and chapter browsing pages
- provide the structure needed for task organization

## Main models

- Course
- LearningSet
- Chapter

## Main views / features

- course listing page
- course detail page
- learning set overview page
- chapter listing page
- chapter detail page

## Boundaries

The courses app should not handle:

- authentication
- task solving logic
- user scoring or leaderboard ranking

## Dependencies

- may be referenced by the tasks app for course, learning set, and chapter context
- may be used by the progress app for context on completed content

## MVP note

For the first release, the app will support one course and one active learning set: the course book. Other learning-set types can be added later without changing the overall app structure.
