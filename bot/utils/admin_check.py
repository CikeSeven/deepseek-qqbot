
def is_admin(user_id: int, config) -> bool:
    return user_id in config.admins