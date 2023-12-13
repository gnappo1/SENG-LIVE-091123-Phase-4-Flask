# Implementing Authentication and Authorization in a FS Flask-React application

## Why do we have to remember the user who attempted to login/signup?
  - UX, we do not want them to re-login every time
  - Statelessness of the HTTP protocol


## How can we implement the logic? What are the options our there?
    - session-based auth (sent back and forth with requests)
    - token-based authentication (sent back and forth with requests)

- What are the steps involved in planning for such a big feature?

## BACKEND Notes:
  - New Routes (/register, /login, /logout, /me)
  - New Model: User (username/email, password -> password protection with bcrypt and hybrid property)
  - New Schema: UserSchema


## FRONTEND Notes:
  - New Route(s): (/register)
  - New Component(s): (Authentication)
  - New useEffect at the highest level to keep the user logged in (localStorage or backend communication)
