import json
from services.bot_service import BotService
from utils.group_manager import GroupManager
from models.message import EventMessage
from utils.admin_check import is_admin

class MessageHandler:

    def __init__(self):
        from chat.chat import Chat
        self.chat = Chat()
        self.group_manager = GroupManager()
        self.bot_service = BotService()
    async def handle_group_message(self, event: EventMessage):
        if event.post_type != 'message':
            return
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
        

        # 检查群是否开启
        config_path = self.group_manager.get_group_config_path(event.group_id)
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if not config.get('open', False):
                    return  # 群未开启，不处理消息
        except:
            return  # 配置文件不存在或出错，不处理消息
        message = event.raw_message
        await self.chat.get(event, message)


    