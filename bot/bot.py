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
    if data['post_type'] != 'message':
        print("Ignoring non-message event")
        print(data)
        return {"message": "ok"}
    if data['self_id'] not in BOT_CONFIG['bot_qq'] and BOT_CONFIG['bot_qq'] != []:
        #非机器人QQ接收的消息
        return {"status": "ok"}
    # 预处理消息段
    processed_segments = []
    for seg in data.get('message', []):
        if seg['type'] == 'json':
            try:
                # 提取并解析小程序数据
                raw_json = seg['data']['data']
                parser = MessageHandler()
                mini_program = await parser.parse_mini_program(raw_json)
                if mini_program:
                    processed_segments.append({
                        'type': 'json',
                        'data': {'mini_program': mini_program.model_dump()}
                    })
            except Exception as e:
                print(f"小程序解析异常: {str(e)}")
        elif seg['type'] == 'text':
            processed_segments.append(seg)
    data['message'] = processed_segments
    
    event = EventMessage(**data)
        
    if event.post_type == "message":
        if event.message_type == "group":
            await message_handler.handle_group_message(event)
    
    return {"status": "ok"}


if __name__ == '__main__':
    if BOT_CONFIG['key'] == "":
        raise ValueError("请先在config.py中设置key")
    if BOT_CONFIG['admins'] == []:
        raise ValueError("请先在config.py中设置管理员列表")
    if BOT_CONFIG['set'] == "":
        raise ValueError("请先在config.py中设置机器人设定")
    
    uvicorn.run(app, host='0.0.0.0', port=8080)