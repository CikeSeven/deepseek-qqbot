import json
import logging
import uvicorn
from fastapi import FastAPI, Request
import os
import sys

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)


from handlers.message_handler import MessageHandler
from models.message import EventMessage

app = FastAPI()
message_handler = MessageHandler()

@app.post("/")
async def handle_message(request: Request):
    data = await request.json()

    # 检查是否为消息类型
    if data.get('post_type') == 'message':
        # 过滤掉不包含文本的消息
        if 'message' in data:
            data['message'] = [msg for msg in data['message'] if msg.get('type') == 'text' and 'text' in msg.get('data', {})]

        event = EventMessage(**data)
        
        if event.post_type == "message":
            if event.message_type == "group":
                await message_handler.handle_group_message(event)
    else:
        logging.info("Ignoring non-message event")
    
    return {"status": "ok"}

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8080) 