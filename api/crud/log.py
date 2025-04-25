from db import get_db
from models.log import UserLog


def get_user_log(user_id):
    db = next(get_db())
    return db.query(UserLog).filter(UserLog.user_id == user_id).first()
