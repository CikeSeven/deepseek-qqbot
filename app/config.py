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

如果已经启动了bot，这里修改参数无效
需要在config/config.yml中修改
"""
config = {
    "chat": {
        "admins": [],   # 管理员账号
        "api": "deepseek",
        "set": "1.你是一个群聊机器人，在群里和群友们聊天，接收到的消息前面会加上昵称和id，表示谁说的，你只需要回复他就行了，不需要加任何前缀。2.记住回复的时候不需要加昵称和id，如果要回复某个人，也尽量不要带上id，只需要说昵称就行了。3.只有和你说话的时候，你才需要发言，这是的消息是xxx对你说，而平时xxx发了一条信息，不需要你发言",
        "model": ChatModels.DEEPSEEK_CHAT.value,    # 默认使用V3模型
        "stream": True,    # 是否流式输出，不影响QQ消息发送方式，只是影响接收回答的方式，可能有些小bug，出现问题在config.yml文件中关闭
        "max_tokens": 4,    #最大回答长度，默认4k，最大8k，这里的数字不可以超过8
        "show_reasoning_content": False,     # 默认使用推理模型是否显示思考过程
        "temperature": 1.3, #temperature，仅适用于V3模型，R1不接受此参数，  0.0适用于代码生成/数学解题、1.0适用于数据抽取/分析、1.3适用于通用对话与翻译，1.5适用于创意类写作/诗歌创作
    },
    "bot": {
        "base_url": "http://localhost:3000",
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8080
    },
    "api_list": {
        "deepseek": "https://api.deepseek.com",
        "tencent": "https://api.lkeap.cloud.tencent.com/v1"
    },
    "key_list": {   #别在这里修改，在config/config.yml中修改
        "deepseek": "",
        "tencent": ""
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
        
        print("选择api提供方，默认使用deepseek官方api，如果要更换请输入数字：")
        print("1.更换为腾讯api")
        api = input("请输入数字（如果不更换，直接回车）：")

        input_admins = input("请输入管理员QQ号(多个用英文逗号隔开):")
        parts = [admin.strip() for admin in input_admins.split(',')]

        admins= []
        for admin in parts:
            admins.append(int(admin))
            
        config['chat']['admins'] = admins

        key = getpass.getpass("请输入DeepSeek API Key（输入时不可见）:")
        if api == '1':
            config['chat']['api'] = "tencent"
            config['key_list']['tencent'] = key
        else:
            config['key_list']['deepseek'] = key
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, sort_keys = False)
        print("已保存，修改请在config目录中config.yml文件进行")
    

    