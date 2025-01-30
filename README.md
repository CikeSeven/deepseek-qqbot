# DeepSeek QQBot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

DeepSeek QQBot 是一个基于 LLOneBot 和 DeepSeek API 的 QQ 机器人，提供智能聊天、问答等功能，仅支持群聊对话。

## 前置条件

在使用本项目之前，请确保你已经安装了 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 或者是相同协议的软件也行，详见[LLOneBot](https://github.com/LLOneBot/LLOneBot)。
并设置上报地址为`http://0.0.0.0:8080`

## 特点
- DeepSeek强大AI加持
- 支持保存上下文信息
- 支持深度思考
- 内置其他小工具
- 对群聊对话专门优化

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
在你要使用的群聊直接发送 `/open` 
成功后机器人会发送成功私信

#### AI聊天
需`艾特`机器人发送消息，进行AI对话

#### 关闭当前群聊
群聊中直接发送`/close`
成功后机器人会发送成功私信

#### 清空消息记录，使用后机器人将恢复出厂设置
群聊中直接发送`/clear`

#### 查询余额
群聊中直接发送 `/blance`

## 效果预览

![39db0d3cb04dd3f8e13017d32127c69d_720](https://github.com/user-attachments/assets/f6839acf-f99e-4308-900f-635c6cd27082)


