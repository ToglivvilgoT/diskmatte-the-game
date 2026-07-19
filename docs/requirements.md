# Requirements for Diskmatte

## Product summary

Diskmatte is a gamified math learning app for students in a university mathematics course. Users can create accounts, solve tasks from courses and chapters, and track progress through stats and leaderboards.

## MVP goals

- User registration and login
- Course and chapter browsing
- Task solving flow
- Progress tracking for solved tasks
- Basic statistics and leaderboard

## Core user stories

1. As a student, I want to create an account so I can save my progress.
2. As a student, I want to open a course and chapter so I can find relevant tasks.
3. As a student, I want to solve tasks and receive feedback so I can learn.
4. As a student, I want to see my progress and score so I can track improvement.
5. As a student, I want to compare my results with others so I stay motivated.

## Functional requirements

- Authentication for signup, login, and logout
- Course catalog with chapters
- Task content with answer handling
- Tracking of correct/incorrect attempts
- User score and solved-task count
- Leaderboard ranked by completed tasks or score

## Non-functional requirements

- Clear and simple UI
- Responsive layout for desktop and mobile
- Reliable data persistence with Django models
- Test coverage for core workflows

## Out of scope for the first version

- Advanced adaptive learning
- Real-time multiplayer features
- Complex analytics dashboards
- Social features beyond leaderboard basics
