import json
import logging
from pathlib import Path

from openai import OpenAI
import openai
from models.message import EventMessage
from services.bot_service import BotService
from utils.group_manager import GroupManager
from models.chat_models import ChatModels
import config

class ChatService:
    def __init__(self):
        self.group_manager = GroupManager()
        self.bot_service = BotService()
        self.config = config.get_config()
        self.api = self.config['chat']['api']
        self.client = OpenAI(api_key = self.config['key_list'][self.api], base_url = self.config['api_list'][self.api])

    async def get(self, event: EventMessage, text: str):
        message = event.message
        at = False
        card = event.sender.card or event.sender.nickname

        for seg in message:
            if seg.type == 'at' and seg.data.qq == str(event.self_id):
                at = True
        
        if not at:
            messages = self.get_or_init_chat(event.group_id)
            # 判断是否为首次对话，并添加系统消息
            is_first_message = len(messages) == 0
            if is_first_message:
                system_message = {"role": "system", "content": self.config['chat']['set']}
                messages.append(system_message)
                
            # 添加用户消息到列表
            user_message = {"role": "user", "content": f"{card}({event.user_id}) 在群聊发了一条消息: {text}"}
            ai_message = {"role": "assistant", "content": "此消息与我不相关，不需要回复"}
            messages.append(user_message)
            messages.append(ai_message)
            self.save_messages(event.group_id, messages)  # 保存所有消息
            return
        
        self.config = config.get_config()
        self.api = self.config['chat']['api']
        self.client = OpenAI(api_key = self.config['key_list'][self.api], base_url = self.config['api_list'][self.api])

        await self.ai_chat(event.group_id, card, event.user_id, text)

    async def ai_chat(self, group_id, card, user_id, content):

        messages = self.get_or_init_chat(group_id)
        # 判断是否为首次对话，并添加系统消息
        is_first_message = len(messages) == 0
        if is_first_message:
            system_message = {"role": "system", "content": self.config['chat']['set']}
            messages.append(system_message)

        # 添加用户消息到列表
        user_message = {"role": "user", "content": f"{card}({user_id}) 对你说: {content}"}
        messages.append(user_message)
        
        group_config = self.group_manager.get_config(group_id)
        model = group_config['model']
        if model == ChatModels.DEFAULT.value:
            model = self.config['chat']['model']
        logging.info(f"群聊：{group_id} 用户： {user_id} 发送聊天请求，模型: {model}")
        if model == ChatModels.DEEPSEEK_REASONER.value:
            think, message = await self.send_by_reasoner_model(messages, group_id)
            assistant_message = {"role": "assistant", "content": message}
            ai_message = think + message
        else:
            ai_message = await self.send_by_chat_model(messages, group_id)
            assistant_message = {"role": "assistant", "content": ai_message}
        

        messages.append(assistant_message)
        self.save_messages(group_id, messages)  # 保存所有消息

        await self.bot_service.send_group_message(group_id, ai_message)
        
    async def send_by_chat_model(self, messages, group_id):
        #function calling暂不可用，等官方修复
        if self.api == 'tencent':
            model = "deepseek-v3"
        else:
            model = "deepseek-chat"
        try:
            response = self.client.chat.completions.create(
                model = model,
                messages = messages,
                stream=self.config['chat']['stream'],
                max_tokens=self.config['chat']['max_tokens'] * 1024,
                temperature=self.config['chat']['temperature'],
            )
            content = ""
            
            if self.config['chat']['stream']:
                for chunk in response:
                    content_chunk = chunk.choices[0].delta.content
                    if content_chunk == None:
                        continue
                    content += content_chunk
                    
                    if content_chunk:
                        print(content_chunk, end="", flush=True)
            else:
                content = response.choices[0].message.content
            
            logging.info(f"调用完毕: {content}")
            if content is None or content == "":
                return "服务器繁忙，请稍后再试。"
            return content.strip()
        except openai.APITimeoutError as e:
            logging.error(f"api timeout: {e}")
            return "api timeout"
        except openai.NotFoundError as e:
            logging.error(f"not found: {e}")
            return "Not Found"
        except openai.APIStatusError as e:
            logging.error(f"api status error: {e}")
            return "api status error"
        except openai.RateLimitError as e:
            logging.error(f"rate limit error: {e}")
            return "rate limit error"
        except openai.BadRequestError as e:
            logging.error(f"bad request error: {e}")
            return "bad requrst error"
        except openai.APIConnectionError as e:
            logging.error(f"connection error: {e}")
            return "connection error"
        except openai.AuthenticationError as e:
            logging.error(f"authentication error: {e}")
            return "authentication error"
        except openai.InternalServerError as e:
            logging.error(f"internal server error: {e}")
            return "internal server error"
        except openai.PermissionDeniedError as e:
            logging.error(f"permission denied error: {e}")
            return "permission denied error"
        except openai.LengthFinishReasonError as e:
            logging.error(f"length finish reason error: {e}")
            return "length finish reason error"
        except openai.UnprocessableEntityError as e:
            logging.error(f"unprocessable entity error: {e}")
            return "unprocessable entity error"
        except openai.APIResponseValidationError as e:
            logging.error(f"api response validation error: {e}")
            return "api response validation error"
        except openai.ContentFilterFinishReasonError as e:
            logging.error(f"content filter finish reason error: {e}")
            return "content filter finish reason error"
        except openai._AmbiguousModuleClientUsageError as e:
            logging.error(f"ambiguous Module client usage error: {e}")
            return "ambiguous Module client usage error"
        except Exception as e:
            print(f"错误：{e}")
            logging.warning(e)
            if str(e) == "Expecting value: line 1 column 1 (char 0)":
                return f"服务器繁忙，请稍后再试。"
            return f"出现未知错误：{e}"
    
    async def send_by_reasoner_model(self, messages, group_id):
        if self.api == 'tencent':
            model = "deepseek-r1"
        else:
            model = "deepseek-reasoner"
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=self.config['chat']['stream'],
                max_tokens=self.config['chat']['max_tokens'] * 1024,
            )

            reasoning_content = ""
            content = ""
            
            if self.config['chat']['stream']:
                for chunk in response:
                    if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content != None:
                        reasoning_content += chunk.choices[0].delta.reasoning_content
                        print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
                    if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content != None:
                        content += chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content, end="", flush=True)

                logging.info(f"调用完毕:<think> {reasoning_content.strip()} <think> ************************ {content}")
            else:
                logging.info(f"调用完毕: {response.choices[0].message}")
                reasoning_content = response.choices[0].message.reasoning_content
                content = response.choices[0].message.content
            
            if content is None or content == "":
                return "", "服务器繁忙，请稍后再试。"
            

            if self.group_manager.get_config(group_id)['show_reasoning_content'] == 'default':
                logging.info("群未配置是否显示思考过程，使用默认配置")
                show_reasoning_content = self.config['chat']['show_reasoning_content']
            else:
                show_reasoning_content = self.group_manager.get_config(group_id)['show_reasoning_content']
            if show_reasoning_content:
                return f"<think>\n{reasoning_content.strip()}\n<think>\n************************\n", content.strip()
            
            return "", content.strip()
            
        except openai.APITimeoutError as e:
            logging.error(f"api timeout: {e}")
            return "", "api timeout"
        except openai.NotFoundError as e:
            logging.error(f"not found: {e}")
            return "", "Not Found"
        except openai.APIStatusError as e:
            logging.error(f"api status error: {e}")
            return "", "api status error"
        except openai.RateLimitError as e:
            logging.error(f"rate limit error: {e}")
            return "", "rate limit error"
        except openai.BadRequestError as e:
            logging.error(f"bad request error: {e}")
            return "", "bad requrst error"
        except openai.APIConnectionError as e:
            logging.error(f"connection error: {e}")
            return "", "connection error"
        except openai.AuthenticationError as e:
            logging.error(f"authentication error: {e}")
            return "", "authentication error"
        except openai.InternalServerError as e:
            logging.error(f"internal server error: {e}")
            return "", "internal server error"
        except openai.PermissionDeniedError as e:
            logging.error(f"permission denied error: {e}")
            return "", "permission denied error"
        except openai.LengthFinishReasonError as e:
            logging.error(f"length finish reason error: {e}")
            return "", "length finish reason error"
        except openai.UnprocessableEntityError as e:
            logging.error(f"unprocessable entity error: {e}")
            return "", "unprocessable entity error"
        except openai.APIResponseValidationError as e:
            logging.error(f"api response validation error: {e}")
            return "", "api response validation error"
        except openai.ContentFilterFinishReasonError as e:
            logging.error(f"content filter finish reason error: {e}")
            return "", "content filter finish reason error"
        except openai._AmbiguousModuleClientUsageError as e:
            logging.error(f"ambiguous Module client usage error: {e}")
            return "", "ambiguous Module client usage error"
        except Exception as e:
            print(f"错误：{e}")
            logging.warning(e)
            if str(e) == "Expecting value: line 1 column 1 (char 0)":
                return "", f"服务器繁忙，请稍后再试。"
            return "", f"出现未知错误：{e}"

    # 保存特定群聊的消息记录
    def save_messages(self, group_id, messages):
        messages_file = self.group_manager.get_group_messages_path(group_id)
        messages_file_path = Path(messages_file)
        with open(messages_file_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)

     # 加载特定群聊的消息记录
    def load_messages(self, group_id):
        #bug高发地
        try:
            messages_file = Path(self.group_manager.get_group_messages_path(group_id))
            if messages_file.exists():
                with open(messages_file, 'r', encoding='utf-8') as f:
                    mes = f.read()
                    if mes == '' or mes == '[]':
                        return []
                    return json.loads(mes)
            else:
                return []
        except Exception as e:
            print(f"Error loading messages for group {group_id}: {e}")
            return []

    # 获取或初始化特定群聊的消息列表
    def get_or_init_chat(self, group_id):
        messages = self.load_messages(group_id)
        if not messages:
            self.save_messages(group_id, [])  # 如果是新群组，保存空列表
        return messages



tools = [
    {
        "type": "function",
        "function": {
            "name": "get_balance",
            "description": "获取当前账户api可调用次数的余额",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "int",
                        "description": "查询者的id，用于验证是否为管理员账号",
                    }
                },
                "required": ["id"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_like",
            "description": "给用户点赞",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "int",
                        "description": "对方的id, 用于给对方点赞",
                    },
                    "times": {
                        "type": "int",
                        "description": "点赞次数，最多十次，默认也是十次",
                    }
                }
            }
        }
    }
]
