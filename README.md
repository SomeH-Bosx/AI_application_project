# 🤖 AI_application_project｜NLP & 本地大模型实战项目合集

<div align="center">

> 轻量化开源 AI 实战仓库｜向量检索 / 离线 RAG / Query 改写优化 / Word2Vec / 文本推荐系统

## ✨ 仓库核心亮点

🚀 **全离线私有化部署**：Ollama 本地大模型 PDF 可视化 RAG，数据不上云，隐私可控

📄 **多层级 RAG 完整工程**：两套 Faiss 基础 RAG + Query 优化增强方案，覆盖从入门到性能调优

🔧 **RAG 进阶优化**：独立 Query 改写 Demo，解决用户提问模糊、检索召回不足痛点

🔍 **传统 NLP 基础工程**：Word2Vec 词向量训练、文本向量化全套可运行代码

🏨 **推荐系统实战案例**：文本相似度酒店推荐，课程作业 / 毕业设计直接复用

💡 **低门槛学习**：纯 Python 轻量化栈，无复杂云服务依赖，开箱即用 Demo

</div>

------

## 📋 项目简介

本仓库为个人 AI 应用实战合集，收录**向量数据库、检索增强生成 (RAG)、Query 优化、词向量、文本推荐**五大方向完整可运行 Demo，全部基于开源本地技术栈开发，适合 NLP、大模型应用初学者、课程大作业、毕业设计参考学习。

## 📂 仓库目录结构

```
AI_application_project/
├── CASE-向量数据库        # Faiss向量库基础Demo，文档向量化、建索引、相似度检索全流程
├── CASEA-Query改写       # RAG进阶优化模块：Query重写拓展Demo，优化检索召回效果
├── Case-ChatPDF-Faiss    # 基于Faiss的简易PDF问答RAG系统，基础文档问答流程
├── ollama-pdf-local-rag  # Ollama本地大模型可视化PDF RAG，完整离线私有知识库方案
├── hotel_recommendation  # 酒店智能推荐系统，基于文本余弦相似度匹配推荐
├── word2vec              # Word2Vec词向量训练、文本向量转换传统NLP实战代码
├── README.md             # 仓库总说明文档
└── LICENSE               # 开源协议文件
```

## 📖 各子项目详细说明

### 1. CASEA-Query 改写（RAG 进阶优化）

- 核心作用：解决用户原始问句模糊、语义简短、关键词缺失导致检索召回差的问题
- 功能：大模型自动扩写、拆分、同义拓展用户 Query，多维度检索提升 RAG 回答准确率
- 适用：所有向量检索、知识库问答系统性能优化拓展

### 2. Case-ChatPDF-Faiss

- 技术栈：Python + Faiss + PyPDF2 + Sentence-Transformers
- 流程：PDF 文本分段 → 文本嵌入向量化 → Faiss 构建向量索引 → 相似度检索匹配文档片段
- 定位：轻量化入门级 PDF 本地问答 RAG，无第三方大模型 API 依赖

### 3. CASE - 向量数据库

- Faiss 底层入门工程，向量检索基础教程
- 包含向量构建、索引持久化、相似度 TopK 查询、批量文档入库全套示例
- 适合从零理解向量数据库检索底层原理

### 4. ollama-pdf-local-rag

- 完整离线闭环 RAG 方案，本地 Ollama 部署开源大模型
- 配套可视化交互界面，上传 PDF 即可构建私有本地知识库
- 融合 Query 改写逻辑，检索精度更高，数据全程本地存储，隐私安全

### 5. hotel_recommendation 酒店推荐系统

- 基于文本相似度的内容推荐 Demo
- 根据用户需求文本，与酒店描述向量匹配，返回相似度排序推荐列表
- 可直接作为推荐系统课程作业、毕设基础工程

### 6. word2vec 词向量项目

- Gensim 实现 Word2Vec 词向量训练、保存与加载
- 支持词语相似度计算、整句文本向量化转换
- 传统 NLP 基础，向量检索、文本分类任务前置学习案例

## ⚙️ 通用环境依赖

所有项目基于 Python 3.11，公共核心依赖：

```bash
pip install faiss-cpu gensim numpy pandas PyPDF2 sentence-transformers ollama
```

每个子目录内置独立`requirements.txt`，进入对应文件夹可单独安装项目专属依赖。

## 🚀 快速上手

1. 克隆仓库到本地

```bash
git clone 你的仓库地址
cd AI_application_project
```

1. 选择需要学习的项目文件夹，阅读子目录内独立 README
2. 安装项目依赖，直接运行 Demo 主程序即可完整体验功能

## 👥 适用人群

- NLP、大模型应用入门学习者，系统学习向量检索、RAG 全链路
- 需要搭建离线私有知识库、本地文档问答工具的开发者
- 计算机相关专业学生，课程大作业、毕业设计全套参考案例
- 想优化 RAG 检索效果，学习 Query 改写等进阶调优方案的工程师

## 📜 License

本项目开源，遵循仓库根目录`LICENSE`协议，可自由学习、二次开发；商用场景请严格遵守协议条款。

------

### 💡 更新说明

仓库持续迭代 RAG 进阶技术，后续将新增多模态检索、向量数据库对比、Agent 实战等 Demo，欢迎 Star 收藏持续跟进！





## 克隆单个文件夹：稀疏检出（完整 Git 能力，可提交更新）

适合你后续要修改代码、push 回仓库，保留 git 版本记录

### 步骤

1. 新建空文件夹，进入目录

```bash
mkdir Multimodal-RAG-Demo
cd Multimodal-RAG-Demo
```

1. 初始化空 git 仓库

```bash
git init
# 关联远程仓库地址
git remote add origin https://github.com/你的用户名/Multimodal-RAG-Assistant.git
```

1. 开启稀疏检出模式

```bash
git config core.sparseCheckout true
```

1. 配置要下载的**单个文件夹路径**

- 只拉取根目录全部文件（README、requirements、.gitignore）：

```bash
echo "/*" >> .git/info/sparse-checkout
```

- 排除素材文件夹（示例：只不要 disney_knowledge_base）

```bash
echo "!disney_knowledge_base/" >> .git/info/sparse-checkout
```

- 如果你只想拉取仓库里某一个子文件夹（比如 `demo/`）：

```bash
echo "demo/" >> .git/info/sparse-checkout
```

1. 拉取代码（浅克隆减少体积）

```bash
# 拉取main分支，只下载指定目录
git pull origin main --depth=1
```

### 适配你的项目场景

你的项目不需要克隆素材 / 向量库文件夹，稀疏配置直接写：

```bash
# 只下载根目录源码文件，屏蔽素材库
echo "/*" >> .git/info/sparse-checkout
echo "!disney_knowledge_base/" >> .git/info/sparse-checkout
```

执行后只会下载 `gradio_app.py`、README、requirements、.gitignore，不会下载知识库文件夹。