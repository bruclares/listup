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
                
    