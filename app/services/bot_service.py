import logging
import os
import aiohttp
import json
import requests
from utils.admin_check import is_admin
import config

class BotService:
    config = config.get_config()

    def __init__(self):
        self.base_url = self.config['bot']['base_url']

    async def send_private_message(self, user_id: int, message: str) -> bool:
        """发送私聊消息"""
        url = f"{self.base_url}/send_private_msg"
        data = {
            "user_id": user_id,
            "message": message
        }
        logging.info(f"准备发送私信消息: {data}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    response_data = await response.json()
                    logging.info(f"=== 发送私聊消息响应 ==={response_data}")
                    return response.status == 200
        except Exception as e:
            logging.warning(f"=== 发送私聊消息失败 ==={str(e)}")
            return False

    async def get_bot_info(self) ->json:
        """获取账号信息"""
        url = f"{self.base_url}/get_login_info"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response_data = await response.json()
                    logging.info(f"=== 获取机器人信息响应 === {response_data}")
                    return response_data['data']
        except Exception as e:
            logging.info(f"=== 获取机器人信息失败 === {str(e)}")
            return False


    async def send_group_message(self, group_id: int, message: str, user_id: list = None, at_user: bool = False) -> bool:
        """发送群聊消息"""
        url = f"{self.base_url}/send_group_msg"
        message_data = []
        if at_user:
            for id in user_id:
                message_data.append({
                    "type": "at",
                    "data": {
                        "qq": str(id)
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
        logging.info(f"准备发送群聊消息: {data}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    response_data = await response.json()
                    logging.info(f"=== 发送群消息响应 === {response_data}")
                    return response.status == 200
        except Exception as e:
            logging.warning(f"=== 发送群消息失败 === {str(e)}")
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
        logging.info(f"准备发送回复消息: {data}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    response_data = await response.json()
                    logging.info(f"=== 发送群消息响应 ==={json.dumps(response_data, ensure_ascii=False, indent=2)}")
                    return response.status == 200
        except Exception as e:
            logging.warning(f"=== 发送群消息失败 ==={str(e)}")
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
                    logging.info(f"=== 发送群消息响应 === {response_data}")
                    return response.status == 200
        except Exception as e:
            logging.info(f"=== 发送群消息失败 === {str(e)} ")
            return False
        

    async def send_like(self, user_id: int, times: int = 10):
        """给用户点赞"""
        url = f"{self.base_url}/send_like"
        data = {
            "user_id": user_id,
            "times": times
        }
        logging.info(f"准备给用户点赞: {data}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    response_data = await response.json()
                    logging.info(f"=== 点赞响应 === {response_data}")
                    
                    # 检查是否已达到点赞上限
                    if response_data.get("message") == "Error: 今日同一好友点赞数已达上限":
                        return "点赞失败 已经点赞过了"
                    
                    return "点赞成功"
        except Exception as e:
            logging.info(f"=== 点赞失败 ==={str(e)}")
            return f"点赞失败，{e}"
        
    
    async def get_user_balance(self, user_id: int):
        if not is_admin(user_id):
            return "不是管理员"
        url = "https://api.deepseek.com/user/balance"

        payload={}
        headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '+ self.config['chat']['api_key']
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
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