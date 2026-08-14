# Tasks app plan

## Purpose

The tasks app is responsible for math problems and the task-solving experience.

## Responsibilities

- define tasks and their content
- organize tasks under a learning set and topic
- manage answer submission and validation
- record attempts and outcomes
- expose task pages for users

## Main models

- Task
- TaskOption
- TaskAttempt

## Main views / features

- task detail page
- answer submission flow
- feedback after solving
- task navigation from topic pages

## Answer formats

For the current MVP, `Task` remains the single parent model for all task content.

- `checkbox`: a simple completion checkbox for tasks that are manually marked done
- `input_field`: a single free-form input used for numbers, booleans, or short text answers
- `multiple_choice`: a list of related `TaskOption` rows where the learner selects one option

Only multiple-choice tasks need extra relational data. Those options belong in `TaskOption` rather than separate task subtype tables, which keeps the task model simple while still allowing arbitrary numbers of choices.

## Boundaries

The tasks app should not handle:

- user authentication logic
- general leaderboard display
- long-term progress summaries unless they are directly tied to the attempt result

## Dependencies

- depends on the courses app for learning set, topic, and course context
- may update progress information for the user after a completed attempt

## MVP note

For the first release, tasks will be simple course-book tasks. The Task model should remain flexible enough to support richer content later, such as hints, images, external references, or solutions, without introducing multiple task-table models too early.

This means answer-type specialization should stay lightweight: common task fields live on `Task`, and only multiple-choice-specific option rows live in a separate model.
