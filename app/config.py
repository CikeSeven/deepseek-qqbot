import getpass
import logging
import os
from enum import Enum
from pathlib import Path

from models.chat_models import ChatModels
import yaml


"""
这里的参数可以不做修改，首次启动项目可以在终端输入相关配置
模型等可以用指令修改，具体看文档
"""
config = {
    "chat": {
        "api_key": "",  # DeepSeek API key
        "admins": [],   # 管理员账号
        "api_base_url": "https://api.deepseek.com",
        "set": "1.你是一个群聊机器人，在群里和群友们聊天，接收到的消息前面会加上昵称和id，表示谁说的，你只需要回复他就行了，不需要加任何前缀。2.记住回复的时候不需要加昵称和id，如果要回复某个人，也尽量不要带上id，只需要说昵称就行了。3.只有和你说话的时候，你才需要发言，这是的消息是xxx对你说，而平时xxx发了一条信息，不需要你发言",
        "model": ChatModels.DEEPSEEK_CHAT.value,    # 默认使用V3模型
        "show_reasoning_content": False,     # 默认使用推理模型是否显示思考过程
    },
    "bot": {
        "base_url": "http://localhost:3000",
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8080
    }
}

def set_bot_id(bot_id):
    config = get_config()
    config['bot']['bot_id'] = bot_id
    set_config(config)

def get_bot_id():
    config = get_config()
    return config['bot']['bot_id']
def get_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(base_dir, 'app', 'config')
    config_path = os.path.join(config_dir, 'config.yml')
    if not os.path.exists(config_path):
        init()
    with open(config_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data

def set_config(config):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(base_dir, 'app', 'config')
    Path(config_dir).mkdir(parents=True, exist_ok=True)
    config_path = os.path.join(config_dir, 'config.yml')

    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys = False)

def init():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(base_dir, 'app', 'config')
    Path(config_dir).mkdir(parents=True, exist_ok=True)
    config_path = os.path.join(config_dir, 'config.yml')

    if not os.path.exists(config_path):
        logging.info("初始化配置文件")
        input_admins = input("请输入管理员QQ号(多个用英文逗号隔开):")
        parts = [admin.strip() for admin in input_admins.split(',')]

        admins= []
        for admin in parts:
            admins.append(int(admin))

        key = getpass.getpass("请输入DeepSeek API Key:")
        config['chat']['admins'] = admins
        config['chat']['api_key'] = key
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, sort_keys = False)
        print("已保存，修改请在config目录中config.yml文件进行")
    

    