# DeepSeek QQBot


DeepSeek QQBot 是一个基于 LLOneBot协议 和 DeepSeek API 的 QQ 机器人，提供智能聊天、问答等功能。
## 前置条件 / Prerequisites

在使用本项目之前，请确保你已经安装了 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 或相同协议的QQ消息监听软件，详见[LLOneBot](https://github.com/LLOneBot/LLOneBot)。

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
