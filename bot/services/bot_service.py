import logging
import os
import aiohttp
import json
import requests

from config import BOT_CONFIG

class BotService:
    def __init__(self):
        self.base_url = BOT_CONFIG['api_base_url']

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
                    logging.info(f"\n=== 发送私聊消息响应 ===\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n")
                    return response.status == 200
        except Exception as e:
            logging.warning(f"\n=== 发送私聊消息失败 ===\n{str(e)}\n")
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
            
            message_data.append({
                "type": "text",
                "data": {
                    "text": f"\n{message}"
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
                    logging.info(f"\n=== 发送群消息响应 ===\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n")
                    return response.status == 200
        except Exception as e:
            logging.warning(f"\n=== 发送群消息失败 ===\n{str(e)}\n")
            return False
    async def send_reply_message(self, group_id, message: str, message_id: int):
        """发送回复消息"""
        url = f"{self.base_url}/send_group_msg"
        message_data = []
            # 添加艾特信息
        message_data.append({
            "type": "reply",
            "data": {
                "id": str(message_id)
            }
        })
        
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
                    logging.info(f"\n=== 发送群消息响应 ===\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n")
                    return response.status == 200
        except Exception as e:
            logging.warning(f"\n=== 发送群消息失败 ===\n{str(e)}\n")
            return False
    async def send_video(self, group_id, video_path: str) -> bool:
        url = f"{self.base_url}/send_group_msg"
        formatted_path = os.path.abspath(video_path)
        message_data = []
        message_data.append({
            "type": "video",
            "data": {
                "file": f"file://{formatted_path}"  # 本地视频路径
            }
        })
        data = {
            "group_id": group_id,
            "message": message_data,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    response_data = await response.json()
                    logging.info(f"\n=== 发送群消息响应 ===\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n")
                    return response.status == 200
        except Exception as e:
            logging.info(f"\n=== 发送群消息失败 ===\n{str(e)}\n")
            return False
    
    async def get_user_balance(self) -> str:
        url = "https://api.deepseek.com/user/balance"

        payload={}
        headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '+ BOT_CONFIG['key']
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code is not 200:
            logging.info(response.text)
            return "请求错误: " + response.status_code
        data = response.text
        data = json.loads(data)
        balance_infos = data['balance_infos']
        is_available = data['is_available']
        for info in balance_infos:
            currency = info['currency']
            total_balance = info['total_balance']
            granted_balance = info['granted_balance']
            topped_up_balance = info['topped_up_balance']
        message = f"可用: {is_available}\n货币: {currency}\n总余额: {total_balance}\n充值余额: {topped_up_balance}\n赠送余额: {granted_balance}"
        
        return message