# DeepSeek QQBot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

DeepSeek QQBot 是一个基于 LLOneBot 和 DeepSeek API 的 QQ 机器人，提供智能聊天、问答等功能。

支持深度思考。
## 前置条件 / Prerequisites

在使用本项目之前，请确保你已经安装了 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 或相同协议的QQ消息监听软件，详见[LLOneBot](https://github.com/LLOneBot/LLOneBot)。
设置上报地址为`http://0.0.0.0:8080`

## 安装步骤

#### 1.克隆仓库

首先，克隆仓库到本地：

```bash
git clone https://github.com/CikeSeven/deepseek-qqbot.git
cd deepseek-qqbot
```
#### 2.创建虚拟环境
```bash
python -m venv .env
#进入虚拟环境
source .env/bin/activate  # Linux/MacOS
.env\Scripts\activate  # Windows
```
#### 3.安装项目所需依赖
```bash
pip install -r requirements.txt
```
#### 4.修改配置文件
打开`config.py`文件，修改`key`和`admins`为你的信息
#### 5.启动机器人
```
python bot/bot.py
```

## 使用方法
成功启动后

![image](https://github.com/user-attachments/assets/33d1584c-e349-4fd5-9c6f-e90aed0de832)

#### 开启机器人
在你要使用的群聊发送 `/open` 
成功后机器人会发送成功私信

#### AI聊天
艾特机器人发送消息，即可进行AI对话

#### 关闭当前群聊
群聊中发送`/close`
成功后机器人会发送成功私信

#### 清空消息记录，使用后机器人恢复出厂设置
群聊中发送`/clear`

## 效果预览

![39db0d3cb04dd3f8e13017d32127c69d_720](https://github.com/user-attachments/assets/f6839acf-f99e-4308-900f-635c6cd27082)

