#!/usr/bin/env python
# coding: utf-8
import os
import time
import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

# -------------------------- 初始化通义千问VL客户端 --------------------------
# 加载密钥
load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise Exception("请在.env文件配置DASHSCOPE_API_KEY阿里云密钥")

# 兼容OpenAI接口
client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
MODEL_NAME = "qwen3-vl-plus"


# -------------------------- 工具函数：图片转base64 --------------------------
def image_to_base64(img_path: str) -> str:
    path = Path(img_path)
    suffix = path.suffix.lower()
    mime_type = "image/jpeg"
    if suffix == ".png":
        mime_type = "image/png"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{data}"


# -------------------------- 工具函数：本地视频转base64（通义千问支持短视频） --------------------------
def video_to_base64(video_path: str) -> str:
    path = Path(video_path)
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:video/mp4;base64,{data}"


# ==================== 1. 纯文字问答（对应原Gemini文本输出） ====================
print("===== 文本问答测试 =====")
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": "用中文解释AI大模型是如何工作的"
        }
    ],
    temperature=0.1
)
print(response.choices[0].message.content)
print("\n" + "-"*60 + "\n")


# ==================== 2. 图片理解（对应原dog_and_girl.jpeg图像解析） ====================
print("===== 图片理解测试 =====")
img_base64 = image_to_base64("dog_and_girl.jpeg")
content_list = [
    {"type": "text", "text": "帮我解释下这张照片"},
    {"type": "image_url", "image_url": {"url": img_base64}}
]

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[{"role": "user", "content": content_list}],
    temperature=0.1
)
print(response.choices[0].message.content)
print("\n" + "-"*60 + "\n")


# ==================== 3. 短视频理解（对应原car.mp4视频解析） ====================
# 注意限制：通义千问VL本地视频base64仅支持短时长MP4（≤1分钟，≤20MB）
print("===== 视频理解测试 =====")
print("读取本地视频文件...")
video_base64 = video_to_base64("car.mp4")

content_list = [
    {"type": "text", "text": "详细描述视频里发生了什么？如果有对话，请把关键对话提取出来。"},
    {"type": "video_url", "video_url": {"url": video_base64}}
]

print("开始推理视频内容...")
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[{"role": "user", "content": content_list}],
    temperature=0.1
)
print(response.choices[0].message.content)