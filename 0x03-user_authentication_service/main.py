#!/usr/bin/env python3

from app import app, AUTH

user = AUTH.register_user(
    'test@test.com',
    'test'
)

session_id = AUTH.create_session(
    'test@test.com'
)
print(user.session_id)

AUTH.destroy_session(user.id)
print(user.session_id)
print(user.email)

if user.session_id is not None:
    print("destroy is not suceesful.")
    exit(0)


print("OK", end='')
