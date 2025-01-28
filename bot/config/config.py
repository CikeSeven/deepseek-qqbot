import json
import logging
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,  # 设置最低日志级别为 INFO
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # 输出到控制台
    ]
)


@dataclass
class BotConfig:
    key: str
    set: str

@dataclass
class AppConfig:
    admins: List[int]
    bot_config: BotConfig

class ConfigManager:
    def __init__(self, config_file='config.json'):
        # 获取配置文件的完整路径
        self.config_file = os.path.join('config', config_file)
        self.config = self.load_config()

    def load_config(self) -> AppConfig:
        """加载配置文件，并转换为数据类"""
        # 如果 config 目录不存在，则创建
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

        if not os.path.exists(self.config_file):
            # 初始化默认配置
            default_config = AppConfig(
                admins=[],
                bot_config=BotConfig(key="", set="你是一个群聊机器人，直接回复消息内容即可。")
            )
            self.save_config(default_config)
            return default_config

        with open(self.config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 检查关键配置项
        required_keys = ["admins", "bot_config.key", "bot_config.set"]
        missing_keys = [key for key in required_keys if not self._check_key_exists(data, key)]
        if missing_keys:
            raise KeyError(f"配置文件缺失关键配置项: {', '.join(missing_keys)}")

        logging.info(f"配置文件信息: {data}")

        # 将字典转换为数据类
        return AppConfig(
            admins=data["admins"],
            bot_config=BotConfig(
                key=data["bot_config"]["key"],
                set=data["bot_config"]["set"]
            )
        )

    def save_config(self, config: AppConfig):
        """保存配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(config), f, indent=4, ensure_ascii=False)

    def _check_key_exists(self, data: dict, key: str) -> bool:
        """检查嵌套字典中是否存在某个键"""
        keys = key.split('.')
        value = data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return False
        return Trueimport os
from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class BotConfig:
    key: str
    set: str

@dataclass
class AppConfig:
    admins: List[int]
    bot_config: BotConfig

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> AppConfig:
        """加载配置文件，并转换为数据类"""
        if not os.path.exists(self.config_file):
            # 初始化默认配置
            default_config = AppConfig(
                admins=[],
                bot_config=BotConfig(key="", set="你是一个群聊机器人，直接回复消息内容即可。")
            )
            self.save_config(default_config)
            return default_config

        with open(self.config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 检查关键配置项
        required_keys = ["admins", "bot_config.key", "bot_config.set"]
        missing_keys = [key for key in required_keys if not self._check_key_exists(data, key)]
        if missing_keys:
            raise KeyError(f"配置文件缺失关键配置项: {', '.join(missing_keys)}")

        # 将字典转换为数据类
        return AppConfig(
            admins=data["admins"],
            bot_config=BotConfig(
                key=data["bot_config"]["key"],
                set=data["bot_config"]["set"]
            )
        )

    def save_config(self, config: AppConfig):
        """保存配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(config), f, indent=4, ensure_ascii=False)

    def _check_key_exists(self, data: dict, key: str) -> bool:
        """检查嵌套字典中是否存在某个键"""
        keys = key.split('.')
        value = data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return False
        return True

