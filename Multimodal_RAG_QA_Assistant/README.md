# 🎠 多模态RAG智能问答助手 | 企业级私有化知识库系统
✨ **Text-Image-Video 跨模态检索 RAG 项目**  
🔥 基于通义多模态向量模型 + Faiss 向量数据库 + Gradio 前端  
💡 支持全格式文档、图片、本地视频、网络视频多维知识库构建

<p align="center">
<img src="https://img.shields.io/badge/Python-3.11+-blue.svg"/>
<img src="https://img.shields.io/badge/Gradio-6.x-orange.svg"/>
<img src="https://img.shields.io/badge/RAG-多模态检索-green.svg"/>
<img src="https://img.shields.io/badge/LLM-通义千问-flat.svg"/>
</p>


## 📌 项目简介
本项目是一款**全功能多模态私有化 RAG 智能问答系统**，突破传统文本RAG限制，
支持 **文本、图片、视频** 三种模态数据混合知识库构建，
实现**跨模态语义检索 + 大模型问答**，可直接用于企业内部知识库、智能客服、资料问答场景。

项目完全本地化部署，**数据不上云、隐私安全**，刷新页面不丢失向量库。

## 🎯 项目亮点（简历重点）
✅ **多模态融合检索**：文本 + 图片 + 视频统一向量空间检索  
✅ **全格式文档解析**：支持 doc / docx / ppt / pptx / pdf / md / txt  
✅ **双模式视频导入**：本地视频上传 + 网络视频URL导入  
✅ **持久化向量数据库**：Faiss 本地存储，重启不丢失知识库  
✅ **私有化部署**：所有数据保存在本地，企业资料安全可控  
✅ **智能意图识别**：自动识别用户需要文本/图片/视频答案  
✅ **现代化 UI**：Gradio 6.x 全新界面，支持拖拽上传  

## 🛠️ 技术栈
- **后端框架**：Python
- **前端界面**：Gradio 6.x
- **大模型服务**：阿里通义千问 Flash
- **向量模型**：通义多模态向量模型 `tongyi-embedding-vision-plus`
- **向量数据库**：Faiss（高性能检索）
- **文档解析**：python-docx / python-pptx / PyPDF2 / markdown

## 📁 项目结构

├── disney_knowledge_base/   # 知识库素材存储目录

│   ├── images/              # 图片素材

│   └── videos/              # 视频素材

├── disney_index.faiss       # 向量索引文件（持久化）

├── disney_metadata.json     # 知识库元数据

├── gradio_app.py            # 项目主程序

└── README.md

## 🚀 快速启动
### 1. 安装依赖
```bash
pip install gradio faiss-cpu dashscope openai python-docx python-pptx markdown PyPDF2 numpy
```

### 2. 配置环境变量

```bash
# Windows
set DASHSCOPE_API_KEY=你的key

# Mac/Linux
export DASHSCOPE_API_KEY=你的key
```

### 3. 运行项目

```bash
python gradio_app.py
```

## 📎 使用流程

1. **上传素材**：支持文档、图片、本地视频、视频链接
2. **构建知识库**：一键生成多模态向量索引
3. **智能问答**：自动匹配文本、图片、视频素材回答问题
4. **持久化存储**：向量库永久保存，刷新 / 重启不丢失

## 💡 核心功能详解

### 1. 多格式文档解析

支持市面几乎所有主流文档：

`doc docx ppt pptx pdf md txt`

### 2. 双视频接入方案

- 本地视频上传：`mp4 mov avi mkv flv`
- 公网视频 URL 导入

### 3. 跨模态智能检索

- 用户提问自动判断需要 **文本答案 / 图片素材 / 视频素材**
- 多维度相似度匹配，精准返回对应知识库内容

### 4. 私有化安全架构

- 所有文件、向量库全部本地存储
- **无数据上传、无隐私泄露风险**
- 非常适合企业内部资料、培训资料、私有知识库部署

## 🌟 项目优势（简历加分项）

1. **区别于普通 RAG**：市面上绝大多数 RAG 仅支持文本，本项目实现**图文视频三模态**
2. **工程化完整**：前端 UI + 数据存储 + 向量检索 + LLM 问答全链路
3. **可商用落地**：真正可部署企业内部知识库系统
4. **持久化设计**：解决传统 RAG 重启丢失数据的痛点

## 📄 开源协议

MIT License