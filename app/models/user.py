from ..database.db import get_db
from werkzeug.security import generate_password_hash
from flask import (g, session)


class User():
    pass

    def login(email):
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    'SELECT * FROM users WHERE email = %s',
                    (email,)
                )
                user = curs.fetchone()

        return user

    def register(name, email, password):
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    '''INSERT INTO users (name, email, password)
                    VALUES (%s, %s, %s)''',
                    (name, email, generate_password_hash(password))
                )

    def logged_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            with get_db() as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        'SELECT * FROM users WHERE id = %s', (user_id,)
                    )
                    g.user = curs.fetchone()
