import sys
import uvicorn
from fastapi import FastAPI, Request

from handlers.message_handler import MessageHandler
from models.message import EventMessage
from config import BOT_CONFIG



app = FastAPI()
message_handler = MessageHandler()

@app.post("/")
async def handle_message(request: Request):
    data = await request.json()
    if data.get('post_type') == 'message':
        # 过滤掉不包含文本的消息
        if 'message' in data:
            data['message'] = [msg for msg in data['message'] if msg.get('type') == 'text' and 'text' in msg.get('data', {})]

        event = EventMessage(**data)
        
        if event.post_type == "message":
            if event.message_type == "group":
                await message_handler.handle_group_message(event)
    else:
        print("Ignoring non-message event")
    
    return {"status": "ok"}


if __name__ == '__main__':
    if BOT_CONFIG['key'] == "":
        raise ValueError("请先在config.py中设置key")
    if BOT_CONFIG['admins'] == []:
        raise ValueError("请先在config.py中设置管理员列表")
    if BOT_CONFIG['set'] == "":
        raise ValueError("请先在config.py中设置机器人设定")
    
    uvicorn.run(app, host='0.0.0.0', port=8080)