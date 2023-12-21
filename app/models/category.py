from ..database.db import get_db
class Category():
    pass

    def get_all():
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute('SELECT id, name FROM categories')
                categories = curs.fetchall()

        return categories
