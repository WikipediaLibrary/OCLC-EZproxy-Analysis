from config import Config as config
from helpers import db_cursor


class TWLightUser:
    query_email = """
       SELECT auth_user.email as email FROM auth_user 
       INNER JOIN users_editor ON users_editor.user_id = auth_user.id
       WHERE users_editor.wp_username = '{}'
       """

    def __init__(self):
        self.db_cursor = db_cursor(config.twlight_db)

    def get_email(self, username):
        self.db_cursor.execute(self.query_email.format(username))
        result = self.db_cursor.fetchone()
        if result is not None:
            return result[0]
