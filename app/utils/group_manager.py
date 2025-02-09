import asyncio
import json
import logging
import os
from pathlib import Path

import yaml
from models.chat_models import ChatModels
import config

class GroupManager:
    from services.bot_service import BotService

    bot_service = BotService()
    config.set_bot_id(asyncio.run(bot_service.get_bot_info())['user_id'])

    config = {
        'open': True,
        'admins': [],   #群组的管理员
        'model': ChatModels.DEFAULT.value,    #默认使用全局配置
        "show_reasoning_content": 'default'
    }


    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.groups_dir = os.path.join(self.base_dir, 'config', str(config.get_bot_id()), 'groups')
        # 确保groups目录存在
        Path(self.groups_dir).mkdir(parents=True, exist_ok=True)
    
    def get_groups(self):
        """获取群组列表"""
        if not os.path.exists(self.groups_dir):
            return []
        groups = []
        for file in os.listdir(self.groups_dir):
            group_id = int(file.split('.')[0])
            groups.append(group_id)
        return groups
    
    def get_group_config_path(self, group_id: int) -> str:
        """获取群配置文件路径"""
        group_dir = os.path.join(self.groups_dir, str(group_id))
        Path(group_dir).mkdir(exist_ok=True)
        return os.path.join(group_dir, 'config.yml')

    def get_group_messages_path(self, group_id: int) -> str:
        """获取群聊天记录文件路径"""
        group_dir = os.path.join(self.groups_dir, str(group_id))
        Path(group_dir).mkdir(exist_ok=True)
        return os.path.join(group_dir, 'message.json')
    
    def get_config(self, group_id: int):
        """获取群配置"""
        path = self.get_group_config_path(group_id)
        if os.path.exists(path):
            with open(path, 'r', encoding = 'utf-8') as f:
                config = yaml.safe_load(f)
            return config
        config = self.config
        config['open']=False
        self.set_config(config, group_id)
        self.close_group(group_id)
    
    def set_config(self, config, group_id):
        """设置群配置"""
        path = self.get_group_config_path(group_id)
        with open(path, 'w', encoding = 'utf-8') as f:
            yaml.dump(config, f, allow_unicode = True, sort_keys = False)
    
    def open_groups(self, groups):
        """开启多个群组"""
        success = fail = 0
        for group in groups:
            if self.open_group(group):
                success += 1
            else:
                fail += 1
        return success, fail

    def close_groups(self, groups):
        """关闭多个群组""" 
        success = fail = 0
        for group in groups:
            if self.close_group(group):
                success += 1
            else:
                fail += 1
        return success, fail
        

    def open_group(self, group_id: int) -> bool:
        """开启群组"""
        config_path = self.get_group_config_path(group_id)
        if not os.path.exists(config_path):
            self.set_config(self.config, group_id)
            return True
        config = self.get_config(group_id)
        if config['open']:
            return False
        config['open'] = True
        self.set_config(config, group_id)
        return True
    
    def close_group(self, group_id: int) -> bool:
        """关闭群组"""
        config_path = self.get_group_config_path(group_id)
        if not Path(config_path).exists():
            return False
        config = self.get_config(group_id)
        if not config['open']:
            return False
        config['open'] = False
        self.set_config(config, group_id)
        return True
    
    def clear(self, group_id: int) -> bool:
        """清除聊天记录"""
        messages_path = self.get_group_messages_path(group_id)
        if not Path(messages_path).exists():
            return False
        data = []
        with open(messages_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    
    def add_admins(self, group_id, admins):
        """添加群组管理员"""
        group_config = self.get_config(group_id)
        for admin in admins:
            if admin not in group_config['admins']:
                group_config['admins'].append(admin)
        self.set_config(group_config, group_id)
        return True
    
    def remove_admins(self, group_id, admins):
        """删除群组管理员"""
        group_config = self.get_config(group_id)
        group_config['admins'][:] = [x for x in group_config['admins'] if x not in admins]
        self.set_config(group_config, group_id)
        return True

    def group_is_open(self, group_id: int):
        """判断群是否开启"""
        config_path = self.get_group_config_path(group_id)
        if not Path(config_path).exists():
            return False
        config = self.get_config(group_id)
        return config['open']