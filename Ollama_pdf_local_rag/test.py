from langchain_ollama import OllamaLLM

# 对接本地Ollama qwen7b模型
llm = OllamaLLM(model="qwen2.5:7b")

# 简单提问测试
res = llm.invoke("简单介绍RAG检索增强生成技术，适合企业私有化部署的优势")
print(res)