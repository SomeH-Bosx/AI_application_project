## Embedding模型的选择

Embedding模型将文本等离散数据转换为低维、稠密的向量，捕捉其语义信息。

向量空间中的距离（如余弦相似度）可反映文本间的语义相似度

* MTEB榜单（Massive Text Embedding Benchmark）

  全面的测评基准，涵盖了分类、聚类、检索、排序等8大类任务和58个数据集。可看到不同模型的性能表现对比。

  https://huggingface.co/spaces/mteb/leaderboard

  【国内用阿里云魔搭——搜mteb】

  https://www.modelscope.cn/docs/model-evaluation/user-guides/backend/rageval-backend/mteb

## 向量数据库

用于存储和查询由非结构化文本（如文本、图片、音视频）转化而来的高维向量嵌入（embedding）

* 价值：①为LLM提供长期记忆；②实现私有知识库的问答和搜索；③赋能推荐系统、以图搜图等多应用。

* 常见向量数据库

  * FAISS
  * Elasticsearch
  * Milvus
  * Pinecone

* 将数据导入向量数据库

  1. 数据清洗和准备（确保质量）

  2. 数据向量化（embedding）

     文本：bge-m，Qwen3-Embedding，Jina-Embedding等

     图片：CLIP，ResNet等

  3. 数据与元数据（Metadata）一同导入

     * 向量
     * 唯一ID
     * 元数据(Metadata)

## 最简 RAG（检索增强生成）语义检索完整 Demo

技术栈：**阿里云百炼 text-embedding-v4（文本向量化） + FAISS（本地向量检索库）**

实现流程：

知识库文本 → 调用 API 转为语义向量 → 存入 FAISS 索引 → 用户提问也转为向量 → FAISS 找出语义最相近文档 → 取出原文用于给大模型做上下文。

简单一句话：**用语义相似度查找和用户问题相关的知识库资料，不再局限关键词匹配。**

### Step1 导入包与初始化客户端

### Step2 准备知识库文档

```python
documents = [
    {
        "id": "doc1",
        "text": "迪士尼乐园的门票一经售出，原则上不予退换。但在特殊情况下，如恶劣天气导致园区关闭，可在官方指引下进行改期或退款。",
        "metadata": {"source": "official_faq_v1.pdf", "category": "退票政策", "author": "Admin"}
    },
    # 省略doc2/doc3/doc4
]
```

模拟知识库：

- `text`：核心段落文本（要向量化的内容）
- `metadata`：附加元数据：来源文件、分类、作者等，检索结果展示、过滤时使用。

> 在真实项目中，这里一般是**文档切片（chunk）**，长 PDF / 网页先拆分小段文本。

### Step3 循环调用 Embedding 接口生成向量

调用阿里云 `text-embedding-v4`，输出**1024 维浮点语义向量**；

三个列表并行保存：

- `vectors_list`：向量数组
- `metadata_store`：原始文档 + 元数据
- `vector_ids`：自定义 ID（这里直接使用循环下标 `0,1,2,3`）

#### 关键转换代码（FAISS 强制要求）

```python
vectors_np = np.array(vectors_list).astype('float32')
vector_ids_np = np.array(vector_ids)
```

⚠️ **FAISS 只接受 float32 的 numpy 二维数组**

API 返回的 list 是 float64，不转换会引发性能问题甚至报错。

### Step4 创建 FAISS 索引，存入向量

1. **IndexFlatL2**

   - 暴力全量检索，**精确搜索**；
   - 使用**L2 欧式距离**；
   - 距离数值越小 → 两个向量语义越相似；
   - 适合小数据集；上万条以上建议换成 HNSW/IVF 索引加速。

2. **IndexIDMap（非常重要）**

   FAISS 原生索引默认只用 0 开始自增内部序号；

   `IndexIDMap` 包装之后，可以**绑定你自己定义的业务 ID**；

   `add_with_ids(向量数组, id数组)` 实现向量 ↔ ID 绑定；

   后续 search 返回的不再是数组下标，而是你存入的自定义 ID。

> 本 Demo 中 ID 和 metadata_store 列表下标一致，拿到 ID 就可以直接取出文档。

### Step5 用户查询向量化 + FAISS 检索

用户问题同样调用 Embedding 接口，转为 1024 维向量；

```
index.search(查询向量, k)
```

- `k=2`：召回语义最接近的**前 2 条**；
- 返回两个数组：
  - `distances`：每条结果对应的 L2 距离
  - `retrieved_ids`：匹配到的向量自定义 ID

### Step6 遍历打印检索结果

- `retrieved_ids[0][i]`：取第一条查询对应的第 i 个匹配 ID；
- `doc_id == -1`：代表不足 k 条匹配结果；
- 通过 ID 去 `metadata_store` 取出原始知识库段落；

#### 运行预期输出

查询：`我想了解一下迪士尼门票的退款流程`

会优先召回 doc1、doc3（退票政策相关文本），doc2 会员、doc4 园区公告距离更大，不会被召回。

### 索引变化

### 一、先区分代码里**所有名称不同的 ID（极易混淆）**

把四类 ID 先定义清楚，再梳理流转链路：

1. **业务文档字符串 ID：doc ["id"]**

   `"doc1"、"doc2"、"doc3"、"doc4"`

   字符串类型，仅存在`documents`原始数据；

   ⚠️ **FAISS 只支持整数 ID，不能直接存入索引**。

   本 Demo 没有把它作为向量主键，仅做展示。

2. **循环下标 i（自定义整数 ID）**

   遍历 `enumerate(documents)` 得到：`0,1,2,3`

   存入列表 `vector_ids = [0,1,2,3]`

   这就是**传给 FAISS 的自定义外部 ID**。

3. **FAISS 底层原生内部序号（IndexFlatL2 内部 ID）**

   原生`IndexFlatL2`内部自动生成：`0,1,2,3`

> 本案例刚好和 i 相等，只是巧合；一旦删除向量，两者不再一致！

1. 检索返回 ID：retrieved_ids [0][i]

   经过

   ```
   IndexIDMap
   ```

   翻译后输出的 = 上面第 2 类：

   ```
   0/1/2/3
   ```

> 本 Demo 巧合：`i == FAISS外部ID == metadata_store列表下标`
>
> 所以拿到 ID 直接 `metadata_store[doc_id]` 就能取出文档。

### 二、索引对象层级关系（索引 “包装” 链路）

```python
# ① 底层裸索引：只存向量，无自定义ID功能
index_flat_l2 = faiss.IndexFlatL2(dimension)

# ② 包装器：套一层ID翻译中介
index = faiss.IndexIDMap(index_flat_l2)
```

层级嵌套：

```
外层对象 index（IndexIDMap）
        ↓内部持有引用
内层对象 index_flat_l2（IndexFlatL2）
```

- **index_flat_l2**：负责向量存储、L2 距离相似度计算；只认识底层内部序号；不支持`add_with_ids`。

- index（IndexIDMap 实例）：对外唯一操作入口；维护一张映射表：

  ```
  【外部自定义ID】 ↔ 【底层IndexFlatL2内部序号】
  ```

> 通俗理解：
>
> IndexIDMap 不改动检索逻辑，只做**ID 翻译转发**；所有增删查向量，必须使用外层变量`index`，禁止直接操作`index_flat_l2`。

### 三、完整时序：ID & 索引变化全流程

#### 阶段 1：遍历文档，生成向量 + 绑定自定义 ID

```python
for i, doc in enumerate(documents):
    vector_ids.append(i)       # i=0,1,2,3 作为外部整数ID
    metadata_store.append(doc) # metadata_store[0] = doc1 ...
```

映射关系此时建立（代码层面内存映射）：

```
外部ID(i) → metadata_store下标 → 完整文档+元数据
0 → doc1
1 → doc2
2 → doc3
3 → doc4
```

#### 阶段 2：构建 FAISS 双层索引

```python
index_flat_l2 = faiss.IndexFlatL2(1024)
index = faiss.IndexIDMap(index_flat_l2)
index.add_with_ids(vectors_np, vector_ids_np)
```

执行`add_with_ids`内部发生两件事：

1. 向量送入内层`index_flat_l2`保存，底层自动分配**内部序号：0,1,2,3**
2. IndexIDMap 生成映射表：

```
外部自定义ID → 底层内部序号
0 → 0
1 → 1
2 → 2
3 → 3
```

✅ 完整链路汇总（写入阶段）

文本 → 向量 → 存入内层索引

```
外部ID(i)` ⇋ IndexIDMap 映射表 ⇋ `底层内部序号
```

#### 阶段 3：检索查询阶段

```python
distances, retrieved_ids = index.search(query_vector, k)
```

内部执行顺序：

1. 查询向量下发给内层`index_flat_l2`，算出最相似向量，返回**底层内部序号**
2. IndexIDMap 查表，把「底层内部序号」反向翻译成**外部自定义 ID**
3. 将外部 ID 装入`retrieved_ids`返回给业务代码

示例查询 “迪士尼退款流程”，检索得到：

```
retrieved_ids[0] = [0,2]
```

对应外部 ID 0、2

#### 阶段 4：业务代码通过 ID 找回原始文档

```python
doc_id = retrieved_ids[0][i]
retrieved_doc = metadata_store[doc_id]
```

利用 Demo 约定：**外部 ID = metadata_store 列表下标**，直接寻址拿到文本与元数据。

### 四、全局完整映射链条（最重要总结）

```
doc["id"]（字符串doc1/doc2）
       ↓（代码循环enumerate）
外部自定义整数ID i (0,1,2,3)
       ↓（送入IndexIDMap）
IndexIDMap内部映射表
       ↓
底层IndexFlatL2原生内部序号(0,1,2,3)
       ←【向量保存在这一层】

检索反向：
底层内部序号 → IndexIDMap翻译 → 外部ID(i) → metadata_store[i] → 原始文档文本+元数据
```

### 五、关键坑点提醒（本 Demo 存在的简化风险）

1. 现在 ID 相等只是巧合！

   如果后续调用 

   ```
   index.remove_ids(np.array([0]))
   ```

    删除一条向量：

- 底层内部序号会发生重组，不再连续；

- 外部自定义 ID 依然由你控制，二者不再一一对应；

  此时绝对不能再用外部 ID 当作 metadata_store 列表下标

> 生产正确做法：不要用列表，改用字典
>
> `meta_dict = {external_id: doc}`，通过 key 查找，规避下标错乱。

1. IndexFlatL2 原生无法接收字符串 ID，所有向量关联 ID 必须是整数。

2. FAISS 索引本身

   只存向量，不保存文本、元数据；

   所有原始文本、metadata 必须外部自行维护映射。

### 六、极简一句话总结

`IndexIDMap`是套在`IndexFlatL2`外面的 ID 翻译层；

程序循环生成整数 i 作为统一 ID，一边对接 FAISS 索引，一边作为元数据列表下标；

检索时 FAISS 底层算出相似度，经过翻译返回 i，代码凭借 i 取出对应的知识库文档。

### 外部ID和内部ID不一致：绑定用户自定义id

新增映射容器

```python
# 映射1：字符串业务ID → FAISS整数ID
strid2faissid = {}
# 映射2：FAISS整数ID → 字符串业务ID
faissid2strid = {}
# 元数据改用字典：key=字符串doc1,doc2
metadata_store = {}
```

* 当前整套 ID 流转链路（改造后）

```
doc["id"] 字符串：doc1 / doc2
        ↓（映射表）
FAISS外部整数ID：1000、1001、1002
        ↓存入 IndexIDMap
IndexIDMap映射表：整数ID ↔ 底层IndexFlatL2内部序号
        ↓
向量存储在底层索引

检索反向：
底层内部序号 → IndexIDMap → FAISS整数ID → 映射表 → doc1字符串ID → metadata_store[doc1]拿到文档
```

* 和你旧版本最大区别

  - 旧代码：**FAISS 整数 ID = list 下标**，脆弱，删除向量直接崩；

  - 新版本：**FAISS 整数 ID 只是中间媒介**，业务主键永远是 `doc1` 字符串，元数据使用字典存储，支持向量删除、增量新增文档。

* 拓展：如果你后续持久化

把 `strid2faissid`、`metadata_store` 存入 json/sqlite，重启程序加载映射表，就可以实现：

加载 faiss 索引文件 → 不用重新向量化，直接检索。


# 误区和限制

## 1. L2 距离认知误区

代码使用 `IndexFlatL2`，输出**平方欧氏距离**

✅ 数值越小 = 语义越接近

不要当成余弦相似度理解。

如果你想要余弦相似度检索：

向量先归一化，改用 `IndexFlatIP`（内积索引）。

## 2. 数据规模限制

`IndexFlatL2` 暴力检索，几千条以内体验良好；

> 超过 1 万条建议使用 IndexHNSWFlat，速度大幅提升。

## 3. 当前方案短板（Demo 简化实现）

- `metadata_store` 只是内存列表，程序关闭丢失；生产环境需要持久化（json/sqlite/redis）；
- FAISS 索引没有持久化，每次启动都要重新生成向量；可以用 `faiss.write_index()` 保存索引文件；
- 没有实现向量删除、增量更新；
- 没有做检索结果过滤、相似度阈值筛选（例如距离大于某个值直接丢弃，避免无关文本）。