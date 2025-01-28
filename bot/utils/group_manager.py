import json
import os
from pathlib import Path

class GroupManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.groups_dir = os.path.join(self.base_dir, 'config', 'groups')
        # 确保groups目录存在
        Path(self.groups_dir).mkdir(parents=True, exist_ok=True)
    
    def get_group_config_path(self, group_id: int) -> str:
        group_dir = os.path.join(self.groups_dir, str(group_id))
        Path(group_dir).mkdir(exist_ok=True)
        return os.path.join(group_dir, 'config.json')

    def get_group_messages_path(self, group_id: int) -> str:
        group_dir = os.path.join(self.groups_dir, str(group_id))
        Path(group_dir).mkdir(exist_ok=True)
        return os.path.join(group_dir, 'message.json')

    def get_messages(self, group_id) ->json:
        config_path = self.get_group_messages_path(group_id)


    
    def open_group(self, group_id: int) -> bool:
        config_path = self.get_group_config_path(group_id)
        config = {
            "group_id": group_id,
            "open": True,
            "created_at": str(Path(config_path).stat().st_ctime if Path(config_path).exists() else "")
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return True
    
    def close_group(self, group_id: int) -> bool:
        config_path = self.get_group_config_path(group_id)
        if not Path(config_path).exists():
            return False
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config['open'] = False
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return True
