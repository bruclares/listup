from ..database.db import get_db
from werkzeug.security import generate_password_hash
from flask import (g, session)

# a model é a representação de uma entidade
# neste caso aqui a model está no formato classe
# a class user representa a tabela users


class User():
    pass

    def get_from_email(email):
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

    def validate_login(form_request):
        error_messages = {}

        email = form_request['email']
        password = form_request['password']

        if not email:
            error_messages['email'] = 'O e-mail é obrigatório.'

        if not password:
            error_messages['password'] = 'A senha é obrigatória.'

        return error_messages

    def validate_register(form_request):
        error_messages = {}

        name = form_request['name']
        email = form_request['email']
        password = form_request['password']

        if not name:
            error_messages['name'] = 'O nome é obrigatório.'

        if not email:
            error_messages['email'] = 'O e-mail é obrigatório.'

        if not password:
            error_messages['password'] = 'A senha é obrigatória.'

        return error_messages
