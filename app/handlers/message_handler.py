from html import unescape
import json
import logging
from urllib.parse import unquote

from pydantic import ValidationError
from services.bot_service import BotService
from utils.group_manager import GroupManager
from utils.bot_manager import BotManager
from config import get_config
from models.message import MiniProgramData, EventMessage
from utils.admin_check import is_admin, is_group_admin


class MessageHandler:

    def __init__(self):
        self.config = get_config()
        self.group_manager = GroupManager()
        self.bot_service = BotService()
        self.bot_manager = BotManager()

    async def handle_group_message(self, event: EventMessage):
        self.bot_manager.update_config()
        logging.info(f"Group Event: {event}")
        text = event.text.strip()
        if is_admin(event.user_id) or is_group_admin(event.group_id, event.user_id):
            if text.lower() == '/open':
                success = self.group_manager.open_group(event.group_id)
                if success:
                    logging.info(f"管理员 {event.user_id} 开启群组 {event.group_id}")
                    await self.bot_service.send_private_message(event.user_id, f"群 {event.group_id} 已开启")
                return
            """已下命令需要群聊开启"""
            if not self.group_manager.group_is_open(event.group_id):
                return
            match text.lower():
                case '/close':
                    success = self.group_manager.close_group(event.group_id)
                    if success:
                        logging.info(f"管理员 {event.user_id} 关闭群组 {event.group_id}")
                        await self.bot_service.send_private_message(event.user_id, f"群 {event.group_id} 已关闭")
                    return
                case '/clear':
                    success = self.group_manager.clear(event.group_id)
                    if success:
                        logging.info(f"管理员 {event.user_id} 清空群组 {event.group_id} 的对话记录")
                        await self.bot_service.send_group_message(event.group_id, "已清空对话记录")
                    return
                case '/model v3' | '/m v3':
                    success, _ = self.bot_manager.set_model_to_v3(event.group_id, event.user_id)
                    if success:
                        logging.info(f"管理员 {event.user_id} 将群 {event.group_id} 模型切换为 V3")
                        await self.bot_service.send_group_message(event.group_id, "已切换为V3模型")
                    return
                case '/model r1' | '/m r1':
                    success, _ = self.bot_manager.set_model_to_r1(event.group_id, event.user_id)
                    if success:
                        logging.info(f"管理员 {event.user_id} 将群 {event.group_id} 模型切换为 R1")
                        await self.bot_service.send_group_message(event.group_id, "已切换R1模型")
                    return
                case '/think close' | '/tc':
                    success, _ = self.bot_manager.close_think_content(event.group_id, event.user_id)
                    if success:
                        logging.info(f"管理员 {event.user_id} 关闭群聊 {event.group_id} 思考过程")
                        await self.bot_service.send_group_message(event.group_id, "已关闭显示思考过程")
                    return
                case '/think open' | '/to':
                    success, _ = self.bot_manager.open_think_content(event.group_id, event.user_id)
                    if success:
                        logging.info(f"管理员 {event.user_id} 开启群聊 {event.group_id} 思考过程")
                        await self.bot_service.send_group_message(event.group_id, "已开启显示思考过程")
                    return
                case '/model default' | '/md':
                    success, _ = self.bot_manager.set_model_to_default(event.group_id, event.user_id)
                    if success:
                        logging.info(f"管理员 {event.user_id} 将群 {event.group_id} 模型切换为 default")
                        await self.bot_service.send_group_message(event.group_id, "已切换模型为默认")
                    return
                case '/think default' | 'td':
                    success, _ = self.bot_manager.default_think_content(event.group_id, event.user_id)
                    if success:
                        logging.info(f"管理员 {event.user_id} 将群 {event.group_id} 思考过程显示方式切换为 default")
                        await self.bot_service.send_group_message(event.group_id, "已切换思考过程显示方式为默认")
                    return
            if is_admin(event.user_id):
                if '/admin add' in text.lower():
                    parts = [part for part in text.split(' ')]
                    if len(parts) < 3:
                        await self.bot_service.send_group_message(event.group_id, "指令错误")
                        return
                    admins = [int(part) for part in parts[2:] if part.isdigit()]
                    success = self.group_manager.add_admins(event.group_id, admins)
                    if success:
                        logging.info(f"管理员 {event.user_id} 为群 {event.group_id} 添加管理员 {admins}")
                        await self.bot_service.send_group_message(event.group_id, "已添加管理员")
                    return
                
                if '/admin rm' in text.lower():
                    parts = [part for part in text.split(' ')]
                    if len(parts) < 3:
                        await self.bot_service.send_group_message(event.group_id, "指令错误")
                        return
                    admins = [int(part) for part in parts[2:] if part.isdigit()]
                    success = self.group_manager.remove_admins(event.group_id, admins)
                    if success:
                        logging.info(f"管理员 {event.user_id} 为群 {event.group_id} 移除管理员 {admins}")
                        await self.bot_service.send_group_message(event.group_id, "已移除管理员")
                    return
                
                if '/set api' in text.lower():
                    parts = [part for part in text.split(' ')]
                    if len(parts) < 3:
                        await self.bot_service.send_group_message(event.group_id, "指令错误")
                        return
                    api_id = int(parts[2])
                    success, msg = self.bot_manager.set_api(event.user_id, api_id)
                    if success:
                       logging.info(f"管理员 {event.user_id} 将群 {event.group_id} 设置为 API {api_id}")
                    await self.bot_service.send_group_message(event.group_id, msg)
                match text.lower():
                    case '/balance':
                        data = await self.bot_service.get_user_balance(event.user_id)
                        await self.bot_service.send_group_message(event.group_id, data)
                        return
                    case '/global model v3' | '/gm v3': 
                        success, _ = self.bot_manager.set_global_model_to_v3(event.user_id)
                        if success:
                            logging.info(f"管理员 {event.user_id} 将全局模型切换为 V3")
                            await self.bot_service.send_group_message(event.group_id, "已切换全局模型为V3")
                        return
                    case '/global model r1' | '/gm r1':
                        success, _ = self.bot_manager.set_global_model_to_r1(event.user_id)
                        if success:
                            logging.info(f"管理员 {event.user_id} 将全局模型切换为 R1")
                            await self.bot_service.send_group_message(event.group_id, "已切换全局模型为R1")
                        return
                    case '/global think open' | '/gto':
                        success, _ = self.bot_manager.open_global_think_content(event.user_id)
                        if success:
                            logging.info(f"管理员 {event.user_id} 开启全局显示思考过程")
                            await self.bot_service.send_group_message(event.group_id, "已开启全局显示思考过程")
                        return
                    case '/global think close' | '/gtc':
                        success, _ = self.bot_manager.close_global_think_content(event.user_id)
                        if success:
                            logging.info(f"管理员 {event.user_id} 关闭全局显示思考过程")
                            await self.bot_service.send_group_message(event.group_id, "已关闭全局显示思考过程")
                        return
                    case '/stream open' | '/so':
                        success, _ = self.bot_manager.open_stream(event.user_id)
                        if success:
                            logging.info(f"管理员 {event.user_id} 开启全局流式输出")
                            await self.bot_service.send_group_message(event.group_id, "已开启流式输出")
                        return
                    case '/stream close' | '/sc':
                        success, _ = self.bot_manager.close_stream(event.group_id, event.user_id)
                        if success:
                            logging.info(f"管理员 {event.user_id} 关闭全局流式输出")
                            await self.bot_service.send_group_message(event.group_id, "已关闭流式输出")
                        return

        if(self.group_manager.group_is_open(event.group_id)):
            from services.chat_service import ChatService
            chat_service = ChatService()
            await chat_service.get(event, text)
            

    async def handle_private_message(self, event: EventMessage):
        logging.info(f"Private Event: {event}")
        if is_admin(event.user_id):
            text = event.text.strip().lower()
            if '/open' in text:
                try:
                    parts = [part for part in text.split(' ')]
                    if len(parts) < 2:
                        await self.bot_service.send_private_message(event.user_id, "指令错误")
                        return
                    groups = [int(group) for group in parts[1:] if group.isdigit()]
                    logging.info(f"管理员{event.user_id}开启群组{groups}")
                    success, fail = self.group_manager.open_groups(groups)
                    await self.bot_service.send_private_message(event.user_id, f"成功开启{success}个，失败{fail}个")
                    return
                except Exception as e:
                    logging.warning(e)
                    return
            if '/close' in text:
                try:
                    parts = [part for part in text.split(' ')]
                    if len(parts) < 2:
                        await self.bot_service.send_private_message(event.user_id, "指令错误")
                        return
                    groups = [int(group) for group in parts[1:] if group.isdigit()]
                    logging.info(f"管理员{event.user_id}关闭群组{groups}")
                    success, fail = self.group_manager.close_groups(groups)
                    await self.bot_service.send_private_message(event.user_id, f"成功关闭{success}个，失败{fail}个")
                    return
                except Exception as e:
                    logging.warning(e)

    async def preprocess_message(self, data):
        import config
        bot_info = await self.bot_service.get_bot_info()
        bot_id = bot_info['user_id']
        config.set_bot_id(bot_id)

        processed_segments = []
        fromatted_message = []
        for seg in data.get('message', []):
            processed_segments.append(await self. parse_message(seg))
            fromatted_message.append(await self.fromat_message(seg, data['self_id']))
        text = ''.join(str(i) for i in fromatted_message)
        data['message'] = processed_segments
        data['text'] = text
        event = EventMessage(**data)
        if event.message_type == 'private':
            await self.handle_private_message(event)
            return
        if event.message_type == 'group':
            await self.handle_group_message(event)
            return

        
    async def fromat_message(self, seg, self_id):
        match seg['type']:
            case 'text':
                return seg['data']['text']
            case 'at':
                if seg['data']['qq'] == str(self_id):
                    return '[艾特你]'
                return f"[艾特 {seg['data']['name']}({seg['data']['qq']})]"
            case 'image':
                return '[图片]'
            case 'video':
                return '[视频]'
            case 'json':
                return '[卡片分享]'
            case 'face':
                return '[表情]'
            case _:
                return seg

    async def parse_message(self,seg):
        if seg['type'] == 'json':
            # 提取并解析小程序数据
            raw_json = seg['data']['data']
            parser = MessageHandler()
            mini_program = await parser.parse_mini_program(raw_json)
            return{
                'type': 'json',
                'data': {'mini_program': mini_program.model_dump()}
            }
        else:
            return seg



    async def parse_mini_program(self, raw_data: str):  # 添加这个方法
        try:
            # 处理HTML转义和URL解码
            cleaned = unescape(unquote(raw_data))
            # 处理反斜杠转义
            cleaned = cleaned.replace('\\/', '/')
            data = json.loads(cleaned)
            mini_program = MiniProgramData(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"小程序解析失败: {str(e)}")
            return None
        return mini_program
    
    async def handle(self, data):
        await self.preprocess_message(data)