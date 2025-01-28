from config import BOT_CONFIG
def is_admin(user_id: int) -> bool:
    return user_id in BOT_CONFIG['admins']