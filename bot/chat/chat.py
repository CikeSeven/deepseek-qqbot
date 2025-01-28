import json
from pathlib import Path
import re
from openai import OpenAI
from bot.config.config import ConfigManager
from services.bot_service import BotService
from utils.group_manager import GroupManager

class Chat:
    def __init__(self):
        self.config = ConfigManager().config
        self.bot_service = BotService()
        self.group_manager = GroupManager()
    
    async def get(self, event, raw_message):
        user_id = event.user_id
        sender = event.sender
        card = sender.card or sender.nickname
        group_id = event.group_id
        self_id = event.self_id

        if "CQ:image" in raw_message:
            pattern = re.compile(r'\[CQ:image[^\]]*\]')
            raw_message = pattern.sub('[图片]', raw_message)
        
            
        # 正则表达式模式
        pattern = re.compile(rf'\[CQ:at,qq={str(self_id)},name=[^\]]+\]')
        
        # 查找是否存在匹配项
        match = pattern.search(raw_message)
        
        if match is None:
            messages = self.get_or_init_chat(event.group_id)
            # 判断是否为首次对话，并添加系统消息
            is_first_message = len(messages) == 0
            if is_first_message:
                system_message = {"role": "system", "content": self.bot_config['set']}
                messages.append(system_message)

            # 添加用户消息到列表
            user_message = {"role": "user", "content": f"{card}({user_id}) 在群聊发了一条消息: {raw_message}"}
            messages.append(user_message)

            self.update_chat(event.group_id, messages)  # 保存所有消息

            return
        
        cleaned_message = pattern.sub('', raw_message).strip()
        
        await self.handle_chat(group_id, card, user_id, cleaned_message)

    async def send(self, card, user_id, content, group_id):

        #messages_path = self.group_manager.get_group_messages_path(group_id)
        
        client = OpenAI(api_key=self.config.bot_config.key, base_url="https://api.deepseek.com")
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self.config.bot_config.set},
                    {"role": "user", "content": f"{card}({user_id}): {content}"},
                ],
                stream=False
            )
            print(response)
            message = response.choices[0].message.content.strip()
            
            await self.bot_service.send_group_message(group_id, message, at_user=False)

        except Exception as e:
            print(f"An error occurred while sending message: {e}")
    
    async def handle_chat(self, group_id, card, user_id, content):
        client = OpenAI(api_key=self.config.bot_config.key, base_url="https://api.deepseek.com")

        messages = self.get_or_init_chat(group_id)

        # 判断是否为首次对话，并添加系统消息
        is_first_message = len(messages) == 0
        if is_first_message:
            system_message = {"role": "system", "content": self.config.bot_config.set}
            messages.append(system_message)

        # 添加用户消息到列表
        user_message = {"role": "user", "content": f"{card}({user_id}) 对你说: {content}"}
        messages.append(user_message)
        
        # 调用 API 获取回复
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        
        ai_message = response.choices[0].message
        
        # 将 AI 回复添加到列表，并保存更新后的消息列表
        assistant_message = {"role": "assistant", "content": ai_message.content.strip()}
        messages.append(assistant_message)
        self.update_chat(group_id, messages)  # 保存所有消息
        
        #print(f"Messages for Group {group_id}: {messages}")

        # 发送 AI 回复给群聊
        message_content = response.choices[0].message.content.strip()
        await self.bot_service.send_group_message(group_id, message_content, at_user=False)
        

    # 保存特定群聊的消息记录
    def save_messages(self, group_id, messages):
        messages_file = self.group_manager.get_group_messages_path(group_id)
        messages_file_path = Path(messages_file)

        with open(messages_file_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)

     # 加载特定群聊的消息记录
    def load_messages(self, group_id):
        messages_file = Path(self.group_manager.get_group_messages_path(group_id))
        if messages_file.exists():
            with open(messages_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []

    # 获取或初始化特定群聊的消息列表
    def get_or_init_chat(self, group_id):
        messages = self.load_messages(group_id)
        if not messages:
            self.save_messages(group_id, [])  # 如果是新群组，保存空列表
        return messages

    # 更新并保存特定群聊的消息列表
    def update_chat(self, group_id, messages):
        self.save_messages(group_id, messages)
