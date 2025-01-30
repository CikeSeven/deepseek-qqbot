BOT_CONFIG = {
    "admins": [],
    'bot_qq': [],   #机器人QQ，可不填
    "set" : "1.你是一个群聊机器人，在群里和群友们聊天，接收到的消息前面会加上昵称和id，表示谁说的，你只需要回复他就行了，不需要加任何前缀。2.记住回复的时候不需要加昵称和id，如果要回复某个人，也尽量不要带上id，只需要说昵称就行了。3.只有和你说话的时候，你才需要发言，这是的消息是xxx对你说，而平时xxx发了一条信息，不需要你发言",		#机器人设定
    "key" :"",
    "api_base_url": "http://localhost:3000",
    
    "bili_video_prase": True, #是否解析b站视频，需要安装ffmpeg，开启后请在下方填上你的b站cookie
    "bili_cookie": "",
    "bili_info": True,   #是否获取b站视频信息
    "limit_time": 4,    #下载视频最大时长， 单位分钟
}