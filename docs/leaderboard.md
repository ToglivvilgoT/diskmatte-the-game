# Leaderboard app plan

## Purpose

The leaderboard app is responsible for presenting user ranking and gamification information.

## Responsibilities

- display ranking lists
- show top users based on solved tasks or score
- present leaderboard views for the web app

## Main models

- no core ownership of user progress data; it should consume existing progress data

## Main views / features

- leaderboard page
- top users overview
- personal ranking view

## Boundaries

The leaderboard app should not handle:

- task creation
- user authentication
- score calculation logic unless it is only a thin presentation layer

## Dependencies

- should rely on data from the progress app
- may also read user information from the accounts app
