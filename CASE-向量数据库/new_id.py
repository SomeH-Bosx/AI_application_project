import os
import numpy as np
import faiss
from openai import OpenAI

# Step1. 初始化 API 客户端
try:
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
except Exception as e:
    print("初始化OpenAI客户端失败，请检查环境变量'DASHSCOPE_API_KEY'是否已设置。")
    print(f"错误信息: {e}")
    exit()

# Step2. 准备示例文本和元数据
documents = [
    {
        "id": "doc1",
        "text": "迪士尼乐园的门票一经售出，原则上不予退换。但在特殊情况下，如恶劣天气导致园区关闭，可在官方指引下进行改期或退款。",
        "metadata": {"source": "official_faq_v1.pdf", "category": "退票政策", "author": "Admin"}
    },
    {
        "id": "doc2",
        "text": "购买“奇妙年卡”的用户，可以享受一年内多次入园的特权，并且在餐饮和购物时有折扣。",
        "metadata": {"source": "annual_pass_rules.docx", "category": "会员权益", "author": "MarketingDept"}
    },
    {
        "id": "doc3",
        "text": "对于在线购买的迪士尼门票，如果需要退票，必须在票面日期前48小时通过原购买渠道提交申请，并可能收取手续费。",
        "metadata": {"source": "online_policy.html", "category": "退票政策", "author": "E-commerceTeam"}
    },
    {
        "id": "doc4",
        "text": "园区内的“加勒比海盗”项目因年度维护，将于下周暂停开放。",
        "metadata": {"source": "maintenance_notice.txt", "category": "园区公告", "author": "OpsDept"}
    }
]

# Step3. 新增ID映射容器 + 向量存储容器
# 双向映射：业务字符串ID <-> FAISS可用整数ID
strid2intid = dict()  # key: doc1/doc2  业务ID  value: FAISS数字ID
intid2strid = dict()  # key: FAISS数字ID value: doc1/doc2 业务ID
metadata_store = dict()  # 元数据字典，key=业务字符串ID(doc1)
vectors_list = []
vector_ids = []  # 存入FAISS的整数ID数组
faiss_auto_id = 1000  # FAISS起始数字ID，从1000开始区分测试下标

print("正在为文档生成向量...")
for doc in documents:
    business_str_id = doc["id"]  # 业务唯一ID：doc1 doc2 doc3 doc4
    # 分配FAISS专用整数ID
    faiss_int_id = faiss_auto_id
    faiss_auto_id += 1

    # 绑定双向映射关系
    strid2intid[business_str_id] = faiss_int_id
    intid2strid[faiss_int_id] = business_str_id
    metadata_store[business_str_id] = doc  # 元数据按业务ID存储

    try:
        # 调用Embedding接口生成向量
        completion = client.embeddings.create(
            model="text-embedding-v4",
            input=doc["text"],
            dimensions=1024,
            encoding_format="float"
        )
        vector = completion.data[0].embedding
        vectors_list.append(vector)
        vector_ids.append(faiss_int_id)
        print(f"  - 已处理文档 {business_str_id}，分配FAISS整数ID:{faiss_int_id}")
    except Exception as e:
        print(f"处理文档 '{business_str_id}' 时出错: {e}")
        continue

# 转换为FAISS要求的float32 numpy数组
vectors_np = np.array(vectors_list).astype('float32')
vector_ids_np = np.array(vector_ids, dtype="int64")  # FAISS强制int64类型ID

# Step4. 构建FAISS双层索引（逻辑不变）
dimension = 1024
k = 2

# 底层L2索引
index_flat_l2 = faiss.IndexFlatL2(dimension)
# 包装ID映射层，支持自定义整数ID
index = faiss.IndexIDMap(index_flat_l2)
# 写入向量+FAISS整数ID
index.add_with_ids(vectors_np, vector_ids_np)

print(f"\nFAISS 索引已成功创建，共包含 {index.ntotal} 个向量。")

# Step5. 检索示例1：查询退款流程
query_text = "我想了解一下迪士尼门票的退款流程"
print(f"\n正在为查询文本生成向量: '{query_text}'")
try:
    query_completion = client.embeddings.create(
        model="text-embedding-v4",
        input=query_text,
        dimensions=1024,
        encoding_format="float"
    )
    # 构造FAISS标准二维float32查询向量
    query_vector = np.array([query_completion.data[0].embedding]).astype('float32')
    distances, retrieved_ids = index.search(query_vector, k)

    print("\n--- 搜索结果（查询：退款流程） ---")
    for i in range(k):
        faiss_int_id = retrieved_ids[0][i]
        if faiss_int_id == -1:
            print(f"\n排名 {i+1}: 未找到更多结果。")
            continue
        # FAISS数字ID反向转换为业务字符串ID
        business_doc_id = intid2strid[faiss_int_id]
        retrieved_doc = metadata_store[business_doc_id]

        print(f"\n--- 排名 {i+1} (L2距离: {distances[0][i]:.4f}) ---")
        print(f"FAISS内部整数ID: {faiss_int_id}")
        print(f"业务文档ID: {business_doc_id}")
        print(f"原始文本: {retrieved_doc['text']}")
        print(f"元数据: {retrieved_doc['metadata']}")
except Exception as e:
    print(f"执行搜索时发生错误: {e}")

# Step6. 检索示例2：查询购卡策略（你之前的测试query）
query_text2 = '有无什么购卡策略？'
print(f"\n正在为查询文本生成向量: '{query_text2}'")
try:
    query_completion2 = client.embeddings.create(
        model="text-embedding-v4",
        input=query_text2,
        dimensions=1024,
        encoding_format="float"
    )
    query_vector2 = np.array([query_completion2.data[0].embedding]).astype('float32')
    distances2, retrieved_ids2 = index.search(query_vector2, k)

    print("\n--- 搜索结果（查询：购卡策略） ---")
    for i in range(k):
        faiss_int_id = retrieved_ids2[0][i]
        if faiss_int_id == -1:
            print(f"\n排名 {i+1}: 未找到更多结果。")
            continue
        business_doc_id = intid2strid[faiss_int_id]
        retrieved_doc2 = metadata_store[business_doc_id]

        print(f"\n--- 排名 {i+1} (L2距离: {distances2[0][i]:.4f}) ---")
        print(f"FAISS内部整数ID: {faiss_int_id}")
        print(f"业务文档ID: {business_doc_id}")
        print(f"原始文本: {retrieved_doc2['text']}")
        print(f"元数据: {retrieved_doc2['metadata']}")
except Exception as e:
    print(f"执行搜索时发生错误: {e}")