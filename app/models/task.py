from flask import session
from ..database.db import get_db


class Task():
    pass

    def get_all(search):
        user_id = session.get('user_id')
        query = '''SELECT tasks.*, categories.name AS category_name FROM tasks
                LEFT JOIN categories ON tasks.category_id = categories.id
                WHERE user_id = %s'''

        parameters = (user_id,)

        if search:
            query += ' and description ilike %s'
            parameters += ('%' + (search if search else '') + '%',)

        query += ' ORDER BY conclusion_date DESC, id'

        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    query,
                    parameters
                )
                tasks = curs.fetchall()
        
        return tasks
    
    def insert(user_id, description, category_id):
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    '''INSERT INTO tasks (user_id, description,
                    category_id) VALUES(%s, %s, %s)''',
                    (user_id, description, category_id))
                
    def update(description, category_id, id):
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    '''UPDATE tasks SET description = %s,
                    category_id = %s WHERE id = %s ''',
                    (description, category_id, id))
                
    def get_from_id(id):
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    'SELECT * FROM tasks WHERE id = %s',
                    (id,)
                )
                task = curs.fetchone()
        return task
    
    def check(id):
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    '''UPDATE tasks SET conclusion_date = CURRENT_TIMESTAMP
                    WHERE id = %s''',
                    (id,))
                
    def uncheck(id):
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    '''UPDATE tasks SET conclusion_date = NULL
                    WHERE id = %s''',
                    (id,))

    def delete(id):
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    'DELETE FROM tasks WHERE id = %s',
                    (id,))

