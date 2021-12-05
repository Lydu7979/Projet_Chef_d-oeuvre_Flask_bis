from flask_login import UserMixin
import datetime
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

ACCESS = {'user': 0,'admin': 1}

class User(UserMixin):
    def __init__(self, id_, name, password, email, access=ACCESS['user'] ):
        self.id = id_
        self.name = name
        self.password = generate_password_hash(password)
        self.email = email
        self.registered_on = datetime.now()
        self.access = access

    def is_admin(self):
        return self.access == ACCESS['admin']
    
    def allowed(self, access_level):
        return self.access >= access_level

    def check_password(self, password:str):
        return check_password_hash(self.password, password)

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user
