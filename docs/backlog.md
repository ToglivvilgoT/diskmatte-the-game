# Backlog

## Planned

- Register page cooked
- Register user should sign them in

- Create course and chapter browsing pages
  - Define MVP screens: course selection, course overview, chapter list, chapter detail, and task detail
  - Define minimal models for a single-course MVP: Course, LearningSet, Chapter, and Task
  - Build course list and course detail views with URLs and templates
  - Build chapter list/detail views and navigation between chapters
  - Build a task detail view with answer submission support for course-book tasks
  - Add business logic for ordering, visibility, and simple progress-aware browsing
  - Keep task content flexible with a single Task model and optional fields or a lightweight JSON field for media/hints/solutions
  - Add tests for the browsing and task flow
- Add task pages with problem display and answer submission
- Track solved tasks and basic user progress statistics
- Implement a simple leaderboard based on solved tasks or score
- Add tests for authentication and core learning flow
- Plan how to uniformly style the entire app (what framework / raw css to use)

## In progress

## Done

- Create initial project planning documents
- Define MVP requirements and architecture direction
- Set up the Django project structure with separate apps for accounts, courses, tasks, progress, and leaderboard
- Add user registration and login flow using Django's built-in authentication


## Later / nice to have

- Add streaks, badges, and achievements
- Add difficulty levels and randomized tasks
- Add richer analytics and progress charts
- Add admin tools for managing courses and tasks
- Add a polished UI and responsive styling
