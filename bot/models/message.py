from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel

# 程序配置模型
class MiniProgramConfig(BaseModel):
    type: str
    width: int
    height: int
    forward: int
    autoSize: int
    ctime: int
    token: str

# 程序元数据模型
class MiniProgramMeta(BaseModel):
    appid: str
    appType: int
    title: str
    desc: str
    icon: str
    preview: str
    url: str
    scene: int
    host: Dict[str, Any]
    shareTemplateId: str
    qqdocurl: str

# 程序数据模型
class MiniProgramData(BaseModel):
    ver: str
    prompt: str
    config: MiniProgramConfig
    needShareCallBack: bool
    app: str
    view: str
    meta: Dict[str, Any]  # 使用字典简化结构，可根据需要进一步细化

# 修改MessageData模型支持多种类型
class MessageData(BaseModel):
    text: Optional[str] = None
    mini_program: Optional[MiniProgramData] = None

class MessageSegment(BaseModel):
    type: str
    data: Union[MessageData, MiniProgramData]

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
            if segment.type == 'text' and segment.data.text:
                text_parts.append(segment.data.text)
            elif segment.type == 'json' and segment.data.mini_program:
                # 添加小程序提示信息
                text_parts.append(f"[小程序]{segment.data.mini_program.meta['detail_1']['title']}")
        return ''.join(text_parts)

    @property
    def mini_programs(self) -> List[MiniProgramData]:
        """获取消息中的小程序信息"""
        return [seg.data.mini_program for seg in self.message 
                if seg.type == 'json' and seg.data.mini_program]