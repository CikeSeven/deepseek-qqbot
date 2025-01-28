from typing import List, Dict, Optional, Union, Any
from pydantic import BaseModel

class MessageData(BaseModel):
    text: str

class MessageSegment(BaseModel):
    type: str
    data: MessageData

class Sender(BaseModel):
    user_id: int
    nickname: str
    card: Optional[str] = ""
    role: Optional[str] = "member"
    title: Optional[str] = ""

class EventMessage(BaseModel):
    post_type: str
    message_type: str
    sub_type: str
    message_id: int
    user_id: int
    message: List[MessageSegment]  # 消息段列表
    raw_message: str
    font: int
    sender: Sender
    group_id: Optional[int] = None
    self_id: Optional[int] = None
    time: Optional[int] = None

    def get_message_text(self) -> str:
        """获取消息文本内容"""
        text_parts = []
        for segment in self.message:
            if segment.type == 'text':
                text_parts.append(segment.data.text)
        return ''.join(text_parts)