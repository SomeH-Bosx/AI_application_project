# 🤖 AI_application_project｜大模型&NLP实战项目合集
> 轻量化开源AI应用Demo仓库｜向量检索 / 本地离线RAG / Word2Vec词向量 / 文本推荐系统
<div align="center">

### ✨ 仓库核心亮点
🚀 **全离线本地方案**：Ollama私有大模型PDF问答，数据不上云，隐私安全
📄 **RAG完整工程**：两套Faiss向量库PDF问答Demo，从底层向量检索到文档问答全覆盖
🔍 **传统NLP基础**：Word2Vec词向量训练、文本向量化全套可运行代码
🏨 **推荐系统实战**：基于文本相似度的酒店智能推荐系统，课程作业/毕设直接复用
💡 **零门槛入门**：纯Python轻量化技术栈，无复杂环境配置，开箱即用学习案例

</div>

## 项目简介
本仓库为个人AI应用实战项目合集，收录**向量检索、本地RAG文档问答、词向量训练、推荐系统**等多套完整可运行Demo，全部基于开源轻量化技术栈实现，适合NLP、大语言模型应用入门学习。

## 仓库目录结构

AI_application_project/

├── CASE - 向量数据库        # Faiss 向量库基础 Demo，文档向量化入库、检索流程

├── Case-ChatPDF-Faiss    # 基于 Faiss 的 PDF 文档问答简易 RAG 系统

├── ollama-pdf-local-rag  # Ollama 本地大模型 + PDF 可视化 RAG 完整演示项目

├── hotel_recommendation  # 酒店智能推荐系统（基于文本相似度检索）

├── word2vec              # Word2Vec 词向量训练、文本向量转换实战代码

└── LICENSE               # 开源协议文件

## 各子项目说明
### 1. Case-ChatPDF-Faiss
- 技术栈：Python + Faiss + PDF解析 + 文本嵌入
- 功能：读取本地PDF文档，文本切块向量化存入Faiss向量库，基于相似度检索实现文档专属问答RAG
- 适用场景：本地私有文档知识库、离线PDF问答工具开发

### 2. CASE-向量数据库
- 轻量化Faiss入门工程
- 包含文本向量化、向量构建索引、相似度查询、向量持久化全套基础示例
- 适合从零学习向量数据库底层逻辑

### 3. ollama-pdf-local-rag
- 本地离线RAG完整方案，基于Ollama部署开源大模型
- 新增可视化交互能力，上传PDF即可本地私有知识库问答
- 全程无需调用第三方API，数据完全本地存储，隐私友好

### 4. hotel_recommendation 酒店推荐系统
- 基于文本余弦相似度的智能酒店推荐Demo
- 通过用户需求文本匹配酒店描述向量，返回匹配度最高的酒店列表
- 配套标准化README文档，可直接扩展为线上推荐服务

### 5. word2vec 词向量项目
- Gensim Word2Vec词向量训练实战代码
- 实现文本语料训练词向量、向量存储加载、词语相似度计算、文本向量化转换
- 传统NLP词表示基础工程，是向量检索、分类任务前置基础

## 环境通用依赖
所有项目统一基于Python3.8+，核心公共依赖：
```bash
pip install faiss-cpu gensim numpy pandas PyPDF2 sentence-transformers ollama
```

各子文件夹内附带独立`requirements.txt`，可进入对应目录单独安装项目专属依赖。

## 快速上手

1. 克隆仓库

```bash
git clone 仓库地址
cd AI_application_project
```

1. 进入目标项目文件夹，阅读子目录内 README
2. 安装依赖，运行 demo 主程序即可体验完整功能

## 适用人群

- NLP / 大模型初学者，学习向量检索、RAG 检索增强生成
- 需要离线本地文档问答、私有知识库开发的开发者
- 毕业设计、课程大作业参考工程（推荐系统、词向量、RAG 多方向完整示例）

## License

本项目开源，遵循根目录`LICENSE`协议，可自由学习、二次开发，商用请遵守协议条款。

------

### 补充说明

仓库持续更新各类 AI 应用 Demo，后续会新增更多本地大模型、多模态、向量工程实战案例，欢迎 Star 收藏！