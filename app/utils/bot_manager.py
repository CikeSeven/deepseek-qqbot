
import json
import logging
import os
from pathlib import Path
import config
from utils.group_manager import GroupManager
from utils.admin_check import is_admin, is_group_admin
from models.chat_models import ChatModels

class BotManager:

    def __init__(self):
        self.config = config.get_config()
        self.group_manager = GroupManager()
    

    def set_chat_config(self,data):
        if data is None:
            return False
        print(config)
        if data.api_base_url is None or data.api_key is None or data.set is None or data.admins is None:
            return False
        self.config['chat']['api_key'] = data.api_key
        self.config['chat']['api_base_url'] = data.api_base_url
        self.config['chat']['model'] = data.model
        self.config['chat']['show_reasoning_content'] = data.show_reasoning_content
        self.config['chat']['set'] = data.set
        self.config['chat']['admins'] = data.admins
        config.set_config(self.config)
        return True
    
    def update_config(self):
        self.config = config.get_config()

    def set_model_to_v3(self, group_id, user_id):
        """设置当前群聊模型为V3"""
        if (not is_admin(user_id)) and (not is_group_admin(group_id, user_id)):
            logging.ingo(f"非管理员账号{user_id}尝试调用set_model_to_v3")
            return False, "修改失败，不是管理员"
        group_config = self.group_manager.get_config(group_id)
        print(group_config)
        if group_config['model'] == ChatModels.DEEPSEEK_CHAT.value:
            logging.info(f"管理员{user_id}尝试重复修改模型为V3")
            return False, "修改失败，当前模型已是V3"
        group_config['model'] = ChatModels.DEEPSEEK_CHAT.value
        self.group_manager.set_config(group_config, group_id)
        return True, "已修改当前群组模型为V3"
    
    def set_model_to_r1(self, group_id, user_id):
        """切换当前群聊模型为R1"""
        if (not is_admin(user_id)) and (not is_group_admin(group_id, user_id)):
            logging.ingo(f"非管理员账号{user_id}尝试调用set_model_to_r1")
            return False, "修改失败，不是管理员"
        group_config = self.group_manager.get_config(group_id)
        
        if group_config['model'] == ChatModels.DEEPSEEK_REASONER.value:
            logging.info(f"管理员{user_id}尝试重复修改模型为R1")
            return False, "修改失败，当前模型已是R1"
        group_config['model'] = ChatModels.DEEPSEEK_REASONER.value
        self.group_manager.set_config(group_config, group_id)
        return True, "已修改当前群组模型为R1"
    
    def set_model_to_default(self, group_id, user_id):
        """切换当前群聊模型为默认"""
        if (not is_admin(user_id)) and (not is_group_admin(group_id, user_id)):
            logging.ingo(f"非管理员账号{user_id}set_model_to_default")
            return False, "修改失败，不是管理员"
        group_config = self.group_manager.get_config(group_id)
        if group_config['model'] == ChatModels.DEFAULT.value:
            logging.info(f"管理员{user_id}尝试重复修改模型为默认")
            return False, "修改失败，当前模型已是默认"
        group_config['model'] = ChatModels.DEFAULT.value
        self.group_manager.set_config(group_config, group_id)
        return True, "已修改当前群组模型为默认"
    
    def set_global_model_to_v3(self, user_id):
        """切换默认模型为V3"""
        if not is_admin(user_id) :
            logging.ingo(f"非管理员账号{user_id}尝试调用set_global_model_to_v3")
            return False, "修改失败，不是管理员"
        if self.config['chat']['model'] == ChatModels.DEEPSEEK_CHAT.value:
            logging.info(f"管理员{user_id}尝试重复修改全局模型为V3")
            return False, "修改失败，当前模型已是V3"
        self.config['chat']['model'] = ChatModels.DEEPSEEK_CHAT.value
        config.set_config(self.config)
        return True, "全局配置模型已修改为V3"
    
    def set_global_model_to_r1(self, user_id):
        """切换默认模型为R1"""
        if not is_admin(user_id):
            logging.ingo(f"非管理员账号{user_id}尝试调用set_global_model_to_r1")
            return False, "修改失败，不是管理员"
        if self.config['chat']['model'] == ChatModels.DEEPSEEK_REASONER.value:
            logging.info(f"管理员{user_id}尝试重复修改全局模型为R1")
            return False, "修改失败，当前模型已是V3"
        self.config['chat']['model'] = ChatModels.DEEPSEEK_REASONER.value
        config.set_config(self.config)
        return True, "全局配置模型已修改为V3"
    
    def open_think_content(self, group_id, user_id):
        """打开当前群聊思考过程"""
        if (not is_admin(user_id)) and (not is_group_admin(user_id)):
            logging.ingo(f"非管理员账号{user_id}尝试调用open_think_content")
            return False, "开启失败，不是管理员"
        group_config = self.group_manager.get_config(group_id)
        if group_config['show_reasoning_content'] == True:
            logging.info(f"管理员{user_id}尝试重复开启思考过程")
            return False, "开启失败， 已是开启状态"
        group_config['show_reasoning_content'] = True
        self.group_manager.set_config(group_config, group_id)
        return True, "已开启显示思考过程"
    
    def open_global_think_content(self, user_id):
        """打开默认显示思考过程"""
        if not is_admin(user_id):
            logging.ingo(f"非管理员账号{user_id}尝试调用open_global_think_content")
            return False, "开启失败，不是管理员"
        if self.config['chat']['show_reasoning_content']:
            logging.info(f"管理员{user_id}尝试重复开启全局思考过程")
            return False, "开启失败，已是开启状态"
        self.config['chat']['show_reasoning_content'] = True
        config.set_config(self.config)
        return True, "已开启全局思考过程"
    
    def default_think_content(self, group_id, user_id):
        """设置当前群聊思考过程显示为默认"""
        if (not is_admin(user_id)) and (not is_group_admin(user_id)):
            logging.ingo(f"非管理员账号{user_id}default_think_content")
            return False, "设置失败，不是管理员"
        group_config = self.group_manager.get_config(group_id)
        if group_config['show_reasoning_content'] == 'default':
            logging.info(f"管理员{user_id}尝试重复设置思考过程为默认")
            return False, "设置失败， 已是默认状态"
        group_config['show_reasoning_content'] = 'default'
        self.group_manager.set_config(group_config, group_id)
        return True, "已设置显示思考过程为默认"
    
    def close_think_content(self, group_id, user_id):
        """关闭当前群聊思考过程"""
        if (not is_admin(user_id)) and (not is_group_admin(user_id)):
            logging.ingo(f"非管理员账号{user_id}尝试调用close_think_content")
            return False, "关闭失败，不是管理员"
        group_config = self.group_manager.get_config(group_id)
        if not group_config['show_reasoning_content']:
            logging.info(f"管理员{user_id}尝试重复关闭思考过程")
            return False, "关闭失败， 已是关闭状态"
        group_config['show_reasoning_content'] = False
        self.group_manager.set_config(group_config, group_id)
        return True, "已关闭显示思考过程"
    
    def close_global_think_content(self, user_id):
        """关闭全局思考过程"""
        if not is_admin(user_id):
            logging.ingo(f"非管理员账号{user_id}尝试调用close_global_think_content")
            return False, "关闭失败，不是管理员"
        if not self.config['chat']['show_reasoning_content']:
            logging.info(f"管理员{user_id}尝试重复关闭全局思考过程")
            return False, "关闭失败，已是关闭状态"
        self.config['chat']['show_reasoning_content'] = False
        config.set_config(self.config)
        return True, "已关闭全局思考过程"
    
    def open_stream(self, user_id):
        """开启流式输出"""
        if not is_admin(user_id):
            logging.ingo(f"非管理员账号{user_id}尝试调用open_stream")
            return False, "开启失败，不是管理员"
        if self.config['chat']['stream']:
            logging.info(f"管理员{user_id}尝试重复开启流式输出")
            return False, "开启失败， 已是开启状态"
        self.config['chat']['stream'] = True
        config.set_config(self.config)
        return True, "已开启流式输出"
    
    def close_stream(self, group_id, user_id):
        """关闭流式输出"""
        if (not is_admin(user_id)) and (not is_group_admin(user_id)):
            logging.ingo(f"非管理员账号{user_id}尝试调用close_stream")
            return False, "关闭失败，不是管理员"
        group_config = self.group_manager.get_config(group_id)
        if not group_config['stream']:
            logging.info(f"管理员{user_id}尝试重复关闭流式输出")
            return False, "关闭失败， 已是关闭状态"
        self.config['chat']['stream'] = False
        config.set_config(self.config)
        return True, "已关闭流式输出"
    
    def set_api(self, user_id, api_id):
        """
        设置api
        0：deepseek api
        1：腾讯api
        """
        if not is_admin(user_id):
            logging.ingo(f"非管理员账号{user_id}尝试调用set_api")
            return False, "设置失败，不是管理员"
        now_api = self.config['chat']['api']
        if now_api == 'deepseek' and api_id == 0:
            logging.info(f"管理员{user_id}尝试重复设置api为deepseek")
            return False, "设置失败， 已是deepseek api"
        if now_api == 'tencent' and api_id == 1:
            logging.info(f"管理员{user_id}尝试重复设置api为腾讯api")
            return False, "设置失败， 已是腾讯api"
        if api_id == 0 and self.config['key_list']['deepseek'] == '':
            logging.warning(f"管理员{user_id}尝试设置api为deepseek，但是未设置deepseek key")
            return False, "设置失败， 未设置deepseek key"
        if api_id == 1 and self.config['key_list']['tencent'] == '':
            logging.warning(f"管理员{user_id}尝试设置api为腾讯api，但是未设置腾讯api key")
            return False, "设置失败， 未设置腾讯api key"
        
        if api_id == 0:
            self.config['chat']['api'] = 'deepseek'
            config.set_config(self.config)
            return True, "已设置api为deepseek"
        if api_id == 1:
            self.config['chat']['api'] = 'tencent'
            config.set_config(self.config)
            return True, "已设置api为腾讯api"
        else:
            logging.warning(f"管理员{user_id}尝试设置api为{api_id}，但是api_id错误")
            return False, "设置失败， api_id错误"
        

    def trim_messages(self, group_id, user_id):
        """清理冗余信息"""
        if (not is_admin(user_id)) and (not is_group_admin(user_id)):
            logging.ingo(f"非管理员账号{user_id}尝试调用trim_messages")
            return False, "清理失败，不是管理员"
        messages_file = Path(self.group_manager.get_group_messages_path(group_id))
        if not messages_file.exists():
            logging.info(f"管理员{user_id}尝试清理不存在的群聊{group_id}的冗余信息")
            return False, "清理失败， 群聊不存在"
        
        with open(messages_file, 'r', encoding='utf-8') as f:
            messages = json.load(f)
        if len(messages) <= 3:
            logging.info(f"管理员{user_id}尝试清理群聊{group_id}的冗余信息，但是信息数量小于10")
            return False, "清理失败， 信息数量小于3"
        
        filtered_messages = []
        filtered_messages.append(messages[0])
        i = 1   #第一条为system消息
        while i < len(messages) - 1:
            if(
                messages[i]['role'] == 'user'
                and messages[i+1]['role'] == 'assistant'
                and messages[i+1]['content'] == '此消息与我不相关，不需要回复'
            ):
                i += 2
            else:
                filtered_messages.append(messages[i])
                i += 1

        with open(messages_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_messages, f, ensure_ascii=False, indent=4)

        return True, "已清理冗余信息"
