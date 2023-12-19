from flask import g
import psycopg
from psycopg.rows import dict_row


def get_db():
    db_params = {
        "host": "localhost",
        "dbname": "listup",
        "user": 'postgres',
        "password": 'postgres',
        "port": 5432
    }
    # if 'db' not in g:
    #     g.db = psycopg.connect(**db_params, row_factory=dict_row)

    return psycopg.connect(**db_params, row_factory=dict_row)


# def close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()


# def init_app(app):
#     app.teardown_appcontext(close_db)
