# 屏蔽弃用警告
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.chains import RetrievalQA

# 1. 大模型保留qwen2.5:7b，向量模型换成专用nomic-embed-text
llm = OllamaLLM(model="qwen2.5:7b")
embedding = OllamaEmbeddings(model="nomic-embed-text")

# 2. 加载PDF文档
loader = PyPDFLoader("附件1.2024年省大学生计算机设计大赛通知.pdf")
docs = loader.load()

# 3. 文本切分
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80
)
split_docs = text_splitter.split_documents(docs)

# 4. 本地持久化向量库
vector_db = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding,
    persist_directory="./chroma_db"
)

# 5. 检索问答链
retriever = vector_db.as_retriever(search_kwargs={"k": 3})
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

# 6. 问答测试
if __name__ == "__main__":
    question = "这是一个怎么样的比赛？"
    answer = qa_chain.invoke({"query": question})
    print(answer["result"])