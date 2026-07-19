# Accounts app plan

## Purpose

The accounts app is responsible for user identity and account-related experience in Diskmatte.

## Responsibilities

- user registration and login
- logout and session handling
- basic user profile information
- account settings that are specific to the user

## Main models

- UserProfile (optional, if extra profile fields are needed)

## Main views / features

- signup page
- login page
- logout flow
- profile page
- account settings page

## Boundaries

The accounts app should not handle:

- course content
- task creation or grading
- leaderboard ranking
- progress statistics beyond what is needed for the user's own profile

## Dependencies

- Django authentication system
- the user model from Django

## Notes for implementation

- Prefer the built-in Django auth system first.
- Add a profile model only if extra user data is needed later.
- Keep business logic in services or helper modules rather than putting everything in views.
