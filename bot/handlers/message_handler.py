import json
import logging
import aiohttp
from utils.admin_check import is_admin
from utils.group_manager import GroupManager
from services.bot_service import BotService
from models.message import EventMessage
from utils.like_service import LikeService
from chat.chat import Chat

class MessageHandler:
    def __init__(self):
        self.chat = Chat()
        self.group_manager = GroupManager()
        self.bot_service = BotService()
        self.like_service = LikeService()

    async def handle_group_message(self, event: EventMessage):
        # 确保事件类型为消息
        if event.post_type != "message":
            return

        # 检查是否是管理员命令
        if is_admin(event.user_id):
            if event.raw_message.strip() == '/open':
                success = self.group_manager.open_group(event.group_id)
                if success:
                    await self.bot_service.send_private_message(event.user_id, "succeed")
                    logging.info(f"群聊已开启：{event.group_id}")
                return
            elif event.raw_message.strip() == '/close':
                success = self.group_manager.close_group(event.group_id)
                if success:
                    await self.bot_service.send_private_message(event.user_id, "succeed")
                    logging.info(f"群聊已关闭：{event.group_id}")
                return
            elif event.raw_message.strip() == '/status':
                # 发送POST请求到指定URL
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.post("http://localhost:3000/get_status") as response:
                            if response.status == 200:
                                status_info = await response.json()
                                readable_status = self.parse_status_info(status_info)
                                await self.bot_service.send_group_message(event.group_id, readable_status, at_user=False)
                            else:
                                await self.bot_service.send_group_message(event.group_id, f"请求失败，状态码: {response.status}", at_user=False)
                                logging.error(f"请求出错: {str(e)}")
                    except Exception as e:
                        await self.bot_service.send_group_message(event.group_id, f"请求出错: {str(e)}", at_user=False)
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
        message = event.raw_message
        
        await self.chat.get(event, message)

    def parse_status_info(self, status_info: dict) -> str:
        """解析状态信息为可读格式"""
        if not status_info or 'data' not in status_info:
            return "无法获取状态信息"

        data = status_info['data']
        online_status = "在线" if data.get('online', False) else "离线"
        good_status = "良好" if data.get('good', False) else "异常"

        # 仅当状态不为ok时返回详细信息
        if status_info.get('status') != 'ok':
            detailed_info = f"\n详细信息: {status_info.get('wording', '无')}"
        else:
            detailed_info = ""

        return (
            f"状态信息:\n"
            f"在线状态: {online_status}\n"
            f"系统状态: {good_status}"
            f"{detailed_info}"
        )