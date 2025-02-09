

import os


def is_admin(user_id):
    """判断是否为管理员"""
    import config
    return user_id in config.get_config()['chat']['admins']

def is_group_admin(group_id, user_id):
    """判断用户是否为群组管理员"""
    from utils.group_manager import GroupManager
    group_manager = GroupManager()
    group_config = group_manager.get_config(group_id)
    if group_config is None:
        return False
    return user_id in group_config['admins']
    