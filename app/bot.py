import asyncio
import os

import uvicorn

from fastapi import FastAPI, Request
from config import get_config
from handlers.message_handler import MessageHandler

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


app = FastAPI()
config = get_config()
message_handler = MessageHandler()

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