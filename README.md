# DeepSeek QQBot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

DeepSeek QQBot 是一个基于 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 和 [DeepSeek API](https://platform.deepseek.com/) 的智能 QQ 机器人，提供强大的聊天、问答等功能，专为群聊对话场景设计。

---

## 前置条件

在使用本项目之前，请确保满足以下条件：
1. 已安装 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 或兼容协议的软件，并设置上报地址为 `http://0.0.0.0:8080`。
2. 在 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册账号并申请一个 API Key。

---

## 特点

- **强大 AI 加持**：基于 DeepSeek 的先进语言模型，提供高质量的对话体验。
- **上下文记忆**：支持保存和追踪对话上下文，提升交互连贯性。
- **深度思考**：能够处理复杂问题，提供更深入的回答。
- **内置小工具**：集成了多种实用功能，满足多样化需求。
- **群聊优化**：针对群聊场景专门优化，确保流畅体验。

---

## 安装步骤

### 1. 克隆仓库
首先，将本项目克隆到本地：
```bash
git clone https://github.com/CikeSeven/deepseek-qqbot.git
cd deepseek-qqbot
```

### 2. 创建虚拟环境
建议使用虚拟环境以隔离依赖：
```bash
python -m venv .env
# 激活虚拟环境
source .env/bin/activate  # Linux/MacOS
.env\Scripts\activate      # Windows
```

### 3. 安装依赖
安装项目所需的 Python 包：
```bash
pip install -r requirements.txt
```

### 4. 启动机器人
运行以下命令启动机器人：
```bash
python app/bot.py
```

### 5.按照提示输入API Key和管理员账号
![image](https://github.com/user-attachments/assets/d1c021a9-67f2-47d2-a425-9b6440460664)

在终端中输入API Key和管理员账号，然后按回车键。


成功启动后，机器人会开始监听消息并响应指令。

---

## 使用方法

### 1. 开启机器人
在需要使用的群聊中发送以下指令：
```
/open
```
机器人会在群聊中开启服务，并向管理员发送私信确认。

### 2. 关闭机器人
在群聊中发送以下指令关闭机器人：
```
/close
```
机器人会停止当前群聊的服务，并向管理员发送私信确认。


## 指令文档

以下是机器人支持的所有指令及其功能说明：

| 指令        | 功能描述                                   | 备注      |
|-------------|------------------------------------------|---------------|
|             | 群组管理员指令       
| `/open`     | 开启当前群聊机器人服务，启用对话功能。          |      |
| `/close`    | 关闭当前群聊机器人服务，暂停对话功能。          |      |
| `/clear`    | 清空上下文记录，重置机器人状态。            |      |
| `/model v3` | 切换当前群组模型为V3                      | 也可用简写`/m v3`|
| `/model r1`  | 切换当前群组模型为V3                     | 也可用简写` /m r1` |
| `/model default`  | 切换当前群组模型为默认（跟随全局）    | 也可用简写` /md` |
| `/think open`  | 展示当前群组R1模型的思考过程              | 也可用简写`/to`       |
| `/think close`  | 关闭当前群组R1模型的思考过程              | 也可用简写`/tc`       |
|            | 非群组管理员指令
| `/balance`  | 查询 DeepSeek API 账户余额。             |     |
| `/admin add [qq]`  | 添加群管理员             |    后可跟多个QQ号，需用`空格`隔开|
| `/admin rm [qq]`  | 移除群管理员             |    后可跟多个QQ号，需用`空格`隔开|
| `/global model v3` | 切换全局模型为V3                      | 也可用简写`/gm v3`|
| `/global model r1`  | 切换全局模型为V3                     | 也可用简写` /gm r1` |
| `/global think open`  | 开启全局R1模型的思考过程              | 也可用简写`/gto`       |
| `/global think close`  | 关闭全局R1模型的思考过程              | 也可用简写`/gtc`       |

---

有问题请提issue或加入反馈群516723952

## 效果预览

以下是机器人运行时的效果截图：

![效果预览](https://github.com/user-attachments/assets/f6839acf-f99e-4308-900f-635c6cd27082)

