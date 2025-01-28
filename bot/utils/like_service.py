import aiohttp
import json

class LikeService:
    def __init__(self):
        self.base_url = "http://127.0.0.1:3000"

    async def send_like(self, user_id: int, times: int = 10) -> tuple[bool, str]:
        """给用户点赞"""
        url = f"{self.base_url}/send_like"
        data = {
            "user_id": user_id,
            "times": times
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    response_data = await response.json()
                    print(f"\n=== 点赞响应 ===\n{json.dumps(response_data, ensure_ascii=False, indent=2)}\n")
                    
                    # 检查是否已达到点赞上限
                    if response_data.get("message") == "Error: 今日同一好友点赞数已达上限":
                        return False, "今天已经赞过了哦~"
                    
                    return response.status == 200, "已给您点赞~"
        except Exception as e:
            print(f"\n=== 点赞失败 ===\n{str(e)}\n")
            return False, "点赞失败，请稍后再试" 