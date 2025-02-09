import asyncio
import os

import uvicorn

from fastapi import FastAPI, Request
from config import get_config
from handlers.message_handler import MessageHandler

import logging

# 配置日志
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename = 'app.log',
    filemode = 'a'
)

app = FastAPI()
config = get_config()
message_handler = MessageHandler()


# 获取当前脚本所在目录的上一级目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 构建 dist 文件夹的路径
DIST_PATH = os.path.join(BASE_DIR, "dist")

@app.post('/')
async def message_listener(request: Request):
    data = await request.json()
    logging.info(f"接收到消息   {data}")
    if data['post_type'] != 'message':
        print('not message')
        return {'status': 'ok'}
    
    await asyncio.create_task(message_handler.handle(data))
    
    return {'status': 'ok'}


if __name__ == '__main__':

    uvicorn.run(app, host = config['server']['host'], port = config['server']['port'])