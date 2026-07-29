# 屏蔽langchain-community弃用警告
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import gradio as gr
import os
import shutil
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# 全局目录
VECTOR_DB_PATH = "./chroma_db"
UPLOAD_CACHE_DIR = "./upload_cache"
os.makedirs(UPLOAD_CACHE_DIR, exist_ok=True)

# Ollama模型，固定标准端口
llm = OllamaLLM(model="qwen2.5:7b", base_url="http://127.0.0.1:11434")
embedding = OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11434")

# 文本分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", "。", "！", "？", "，", " "]
)

# 强约束提示词
prompt_template = """
仅依据下方上下文回答，禁止编造外部知识。
若无相关内容，直接回复：文档中未找到相关内容。

上下文：{context}
问题：{question}
"""
fixed_prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])


# 上传PDF（每次重建全新向量库，杜绝维度冲突）
def load_pdf_and_build_db(pdf_file):
    try:
        if not pdf_file:
            return "错误：请先上传PDF文件"
        # 永久缓存PDF
        fname = os.path.basename(pdf_file.name)
        cache_path = os.path.join(UPLOAD_CACHE_DIR, fname)
        shutil.copy(pdf_file, cache_path)
        # 彻底删除旧向量库，避免冲突
        if os.path.exists(VECTOR_DB_PATH):
            shutil.rmtree(VECTOR_DB_PATH)
        # 加载文档
        loader = PDFPlumberLoader(cache_path)
        docs = loader.load()
        if len(docs) == 0:
            return "错误：PDF无可用文字（扫描图片）"
        split_docs = text_splitter.split_documents(docs)
        # 新建向量库
        Chroma.from_documents(split_docs, embedding, persist_directory=VECTOR_DB_PATH)
        return f"导入完成！切割 {len(split_docs)} 段文本"
    except Exception as e:
        return f"导入异常：{str(e)}"


# 问答函数：适配Gradio 6.x 强制messages格式
def chat_with_rag(question, chat_history):
    try:
        q = question.strip()
        if not q:
            return "", chat_history
        if not os.path.exists(VECTOR_DB_PATH):
            ans = "错误：请先上传PDF文档"
            chat_history.append({"role": "user", "content": q})
            chat_history.append({"role": "assistant", "content": ans})
            return "", chat_history
        # 加载向量库
        db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embedding)
        retriever = db.as_retriever(search_kwargs={"k": 5})
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": fixed_prompt}
        )
        res = qa.invoke({"query": q})
        answer = res["result"]
        # Gradio 6.x 标准messages格式
        chat_history.append({"role": "user", "content": q})
        chat_history.append({"role": "assistant", "content": answer})
        return "", chat_history
    except Exception as e:
        err = f"查询异常：{str(e)}"
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": err})
        return "", chat_history


# 清空对话
def clear_history():
    return []


# 全部重置
def reset_all():
    if os.path.exists(VECTOR_DB_PATH):
        shutil.rmtree(VECTOR_DB_PATH)
    if os.path.exists(UPLOAD_CACHE_DIR):
        for f in os.listdir(UPLOAD_CACHE_DIR):
            os.remove(os.path.join(UPLOAD_CACHE_DIR, f))
    return "已清空全部知识库", "", []


# 界面（Gradio 6.x 兼容版）
with gr.Blocks(title="本地离线知识库问答系统") as demo:
    gr.Markdown("# Ollama+LangChain 私有化RAG工具（Gradio 6.x 兼容版）")

    # 内存状态缓存，切换主题不丢失对话
    chat_state = gr.State([])

    with gr.Row():
        pdf_upload = gr.File(label="上传PDF知识库", file_types=[".pdf"])
        upload_btn = gr.Button("导入文档", variant="primary")
        reset_btn = gr.Button("重置全部知识库", variant="stop")

    status = gr.Textbox(label="状态", interactive=False)
    
    # ⚠️ Gradio 6.x 移除了type参数，默认且仅支持messages格式
    chatbot = gr.Chatbot(label="问答历史", height=400)

    with gr.Row():
        question = gr.Textbox(label="提问", scale=8)
        submit = gr.Button("查询知识库", scale=1)
        clear_btn = gr.Button("清空对话", scale=1)

    # 绑定交互事件
    upload_btn.click(load_pdf_and_build_db, inputs=[pdf_upload], outputs=[status])
    submit.click(chat_with_rag, inputs=[question, chat_state], outputs=[question, chatbot])
    question.submit(chat_with_rag, inputs=[question, chat_state], outputs=[question, chatbot])
    clear_btn.click(clear_history, outputs=[chatbot])
    reset_btn.click(reset_all, outputs=[status, pdf_upload, chatbot])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1")