from html import unescape
import json
import re
from urllib.parse import unquote

from pydantic import ValidationError
from services.bot_service import BotService
from utils.group_manager import GroupManager
from models.message import EventMessage, MiniProgramData
from utils.mini_program_utils import MiniProgramUtils
from utils.admin_check import is_admin
from config import BOT_CONFIG

class MessageHandler:

    def __init__(self):
        from chat.chat import Chat
        self.chat = Chat()
        self.group_manager = GroupManager()
        self.bot_service = BotService()   
        self.handle = MiniProgramUtils() 

    async def parse_mini_program(self, raw_data: str):  # 添加这个方法
        try:
            # 处理HTML转义和URL解码
            cleaned = unescape(unquote(raw_data))
            # 处理反斜杠转义
            cleaned = cleaned.replace('\\/', '/')
            data = json.loads(cleaned)
            mini_program = MiniProgramData(**data)
            #await self.handle.handle_program(mini_program)
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"小程序解析失败: {str(e)}")
            return None
        return mini_program
    async def handle_group_message(self, event: EventMessage):
        text = event.raw_message.strip()
        #处理管理员指令
        if is_admin(event.user_id):
            if(text == '/open'):
                seccess = self.group_manager.open_group(event.group_id)
                if seccess:
                    await self.bot_service.send_private_message(event.user_id, f"群{event.group_id}开启成功")
            if(text == '/close'):
                success = self.group_manager.close_group(event.group_id)
                if success:
                    await self.bot_service.send_private_message(event.user_id, f"群{event.group_id}关闭成功")
            if(text == '/clear'):
                success = self.group_manager.clear(event.group_id)
                if success:
                    await self.bot_service.send_group_message(event.group_id, "已清空对话记录", at_user=False)
                return
            if event.raw_message.strip() == '/balance':
                data = await self.bot_service.get_user_balance()
                await self.bot_service.send_group_message(event.group_id, data, at_user=False)
                return

        # 检查群是否开启
        config_path = self.group_manager.get_group_config_path(event.group_id)
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if not config.get('open', False):
                    return  # 群未开启，不处理消息
        except:
            return  # 配置文件不存在或出错，不处理消息
        
        if event.raw_message[4:8] == 'json':
            await self.handle.handle_program(event)
            return
        if event.post_type != 'message':
            return
        if 'b23.tv' in text and BOT_CONFIG['bili_video_prase']:
            url = re.findall(r'https?://[^\s,。！？]*b23\.tv/[^\s,。！？]+', text)
            await self.handle.bili_video(url[0], event)
            return

        #处理分享消息
        message = event.raw_message
        await self.chat.get(event, message)


    