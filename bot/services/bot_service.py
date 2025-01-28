import aiohttp
import json
import requests


class BotService:
    def __init__(self):
        self.base_url = "http://127.0.0.1:3000"  # go-cqhttp的地址

    async def send_private_message(self, user_id: int, message: str) -> bool:
        """发送私聊消息"""
        url = f"{self.base_url}/send_private_msg"
        data = {
            "user_id": user_id,
            "message": message
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    response_data = await response.json()
                    print(f"\n=== 发送私聊消息响应 ===\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n")
                    return response.status == 200
        except Exception as e:
            print(f"\n=== 发送私聊消息失败 ===\n{str(e)}\n")
            return False


    async def send_group_message(self, group_id: int, message: str, user_id: int = None, at_user: bool = True) -> bool:
        """发送群消息，支持艾特用户"""
        url = f"{self.base_url}/send_group_msg"
        message_data = []

        if at_user and user_id:
            # 添加艾特信息
            message_data.append({
                "type": "at",
                "data": {
                    "qq": str(user_id)
                }
            })
            # 添加文本信息，确保在新的一行
            message_data.append({
                "type": "text",
                "data": {
                    "text": f"\n{message}"  # 在消息前添加换行符
                }
            })
        else:
            # 直接添加文本信息
            message_data.append({
                "type": "text",
                "data": {
                    "text": message
                }
            })

        data = {
            "group_id": group_id,
            "message": message_data
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    response_data = await response.json()
                    print(f"\n=== 发送群消息响应 ===\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n")
                    return response.status == 200
        except Exception as e:
            print(f"\n=== 发送群消息失败 ===\n{str(e)}\n")
            return False

