


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

class MiniProgramData(BaseModel):
    ver: str
    prompt: str
    config: MiniProgramConfig
    needShareCallBack: bool
    app: str
    view: str
    meta: Dict[str, Any]

class TextData(BaseModel):
    text: Optional[str] = None
    mini_program: Optional[MiniProgramData] = None

class AtData(BaseModel):
    qq: Optional[str] = None
    name: Optional[str] = None

class ImageData(BaseModel):
    file: str
    subType: int
    url: str
    file_size: str

class VideoData(BaseModel):
    file: str
    url: str
    path: str
    file_size: str

class ReplyData(BaseModel):
    id: str

#语音
class RecordData(BaseModel):
    file: str
    url: str
    path: str
    file_size: str

#表情
class FaceData(BaseModel):
    id: str

class MessageSegment(BaseModel):
    type: str
    data: Union[TextData, MiniProgramData, AtData, ImageData, VideoData, RecordData, FaceData, ReplyData]

class Sender(BaseModel):
    user_id: int
    nickname: str
    card: Optional[str] = None
    role:Optional[str] = None
    title: Optional[str] = None

class EventMessage(BaseModel):
    self_id: int
    user_id: int
    time: int
    message_id: int
    message_seq: int
    message_type: str
    sender: Sender
    raw_message: str
    message: List[MessageSegment]
    message_format: str
    post_type: str
    group_id: Optional[int] = None
    text: Optional[str] = None