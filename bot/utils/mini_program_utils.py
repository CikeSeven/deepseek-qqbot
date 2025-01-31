from datetime import datetime
import json
import os
from pathlib import Path
import re
import subprocess

import requests
from config import BOT_CONFIG
from services.bot_service import BotService


class MiniProgramUtils:

    def __init__(self):
        self.bot_service = BotService()
    async def handle_program(self, event):
        mini_program = event.message[0].data.mini_program
        meta = mini_program.meta
        if meta['detail_1']['title'] == '哔哩哔哩' and BOT_CONFIG['bili_video_prase']:
            await self.bili_video(meta['detail_1']['qqdocurl'], event)
            return
    
    
    async def bili_video(self, url, event):
        short_url = url.split('?')[0]
        response = requests.get(short_url, allow_redirects=True)
        final_url = response.url.split('?')[0]
        cookie = BOT_CONFIG['bili_cookie']
        headers = {
                "Referer": final_url,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
                "Cookie": cookie
        }
        # 发送请求
        response = requests.get(url=url, headers=headers)
        html = response.text
        
        # 解析数据: 提取视频标题
        title = re.findall('title="(.*?)"', html)[0]
        print(f"视频标题: {title}")

        #获取播放量
        views = re.findall('播放量 (\d+)', html)
        #获取弹幕数
        dm = re.findall('弹幕量 (\d+)', html)
        #获取发布时间
        pubdate = re.findall('<div class="pubdate-ip-text"[^>]*>(.*?)</div>', html)
        #获取点赞数
        likes = re.findall('点赞数 (\d+)', html)
        #获取投币
        coins = re.findall('投硬币枚数 (\d+)', html)
        #获取收藏
        favs = re.findall('收藏人数 (\d+)', html)
        shares = re.findall(r'转发人数 (\d+)', html)
        auther = re.findall(r'视频作者 ([^,]+)', html)
        #评论数
        comments = re.findall(r'"reply":(\d+)', html)
        #视频长度
        video_time = re.findall(r'"timelength":(\d+)', html)
        time_m = float(video_time[0]) / 1000 / 60 if video_time else 0
        if(time_m > BOT_CONFIG['limit_time']):
            print(f"视频长度超过限制，不进行下载 {time_m}")
            return
        # 确定保存路径
        current_dir = Path(__file__).resolve().parent
        parent_dir = current_dir.parent
        video_dir = parent_dir / 'video'
        
        # 如果目录不存在，则创建
        video_dir.mkdir(parents=True, exist_ok=True)
        output_file_path = video_dir / f'{title}.mp4'
        if os.path.exists(output_file_path):
            print(f"视频已存在，跳过下载: {title}.mp4")

        else:
            # 提取视频信息
            info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
            # info -> json字符串转成json字典
            json_data = json.loads(info)
            # 提取视频链接
            video_url = json_data['data']['dash']['video'][0]['baseUrl']
            # 提取音频链接
            audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
            print("开始下载视频")
            video_content = requests.get(url=video_url, headers=headers).content
            # 获取音频内容
            audio_content = requests.get(url=audio_url, headers=headers).content
            
            temp_video_path = video_dir / 'temp/temp.mp4'
            temp_audio_path = video_dir / 'temp/temp.mp3'
            # 保存视频文件
            with open(temp_video_path, mode='wb') as v:
                v.write(video_content)
                print(f"Video saved to {temp_video_path}")
            
            # 保存音频文件
            with open(temp_audio_path, mode='wb') as a:
                a.write(audio_content)
                print(f"Audio saved to {temp_audio_path}")
            # 合并音频和视频
            await self.merge_audio_video(temp_video_path, temp_audio_path, output_file_path)
        if BOT_CONFIG['bili_info']:
            reply_message = f"视频标题: {title}\n作者: {auther[0]}\n发布时间: {pubdate[0]}\n播放: {views[0]} | 点赞: {likes[0]}\n投币: {coins[0]} | 收藏: {favs[0]}\n转发: {shares[0]} | 评论: {comments[0]}\n投币: {coins[0]}"
            success = await self.bot_service.send_reply_message(group_id=event.group_id, message=reply_message, message_id=event.message_id)
            if success:
                print(f"已发送视频信息消息")
        success = await self.bot_service.send_video(group_id=event.group_id, video_path=output_file_path)
        if success:
            print(f"已发送视频")
         
        



    async def merge_audio_video(self, video_path, audio_path, output_path):
        try:
            # 确保路径为字符串
            video_path = str(video_path)
            audio_path = str(audio_path)
            output_path = str(output_path)
            
            # 构造 FFmpeg 命令
            ffmpeg_cmd = [
                'ffmpeg',
                '-y',                      # 覆盖输出文件
                '-i', video_path,          # 视频输入
                '-i', audio_path,          # 音频输入
                '-c:v', 'copy',            # 复制视频流
                '-c:a', 'aac',             # 重新编码音频
                '-strict', 'experimental', # 兼容性参数
                output_path
            ]

            # 执行命令
            subprocess.run(
                ffmpeg_cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"合并成功: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"合并失败: {e.stderr.decode()}")
        except Exception as e:
            print(f"发生错误: {str(e)}")