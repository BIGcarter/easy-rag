# 动手实现一个简易版 RAG！

> Retrieval-Augmented Generation from scratch with Python, Qwen3 & ChromaDB

>改编自[B站视频《从零写AI RAG 个人知识库》](https://www.bilibili.com/video/BV168j7zCE6D/?spm_id_from=333.1391.0.0)。

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
  <img src="https://img.shields.io/badge/build-passing-brightgreen" />
</p>

---

## 📖 项目简介

本仓库演示了 **RAG（Retrieval-Augmented Generation）** 的最小可用实现：

1. **向量化 (Embedding)** — 借助 [Qwen3-Embedding](https://github.com/QwenLM/Qwen3-Embedding) 模型将文本转为向量；
2. **检索 (Retrieval)** — 利用 [ChromaDB](https://github.com/chroma-core/chroma) 持久化并按相似度召回文档块；
3. **生成 (Generation)** — 把检索结果与用户问题拼接后，交给大模型生成答案。
4. **Agent辅助搜索（Agentic Search）** — 利用LLM的Function Call能力，指定搜索文档的特定区域，减少检索量（TBD）

在向量化阶段，针对不同的文档格式可使用不同的文档分割方法：
  
- Markdown ✅
  - 按段分割（匹配"\n\n"字符，简单粗暴）
  - 按Header分割Section，Section内再按token数进行重叠窗口细分，将文档的metadata一起放入向量库中，实现定点检索。
- Microsoft doc （TBD）
- PDF (TBD)

整个流程仅依赖 ~100 行 Python 代码，方便理解与二次开发。



## 🚀 快速开始

### 1. 克隆项目
```bash
$ git clone https://github.com/BIGcarter/easy-rag.git
$ cd easy-rag
```

### 2. 创建 Conda 环境
```bash
$ conda create -n easy-rag python=3.10
$ conda activate easy-rag
```

### 3. 安装依赖
```bash
$ pip install -r requirements.txt
```
<details>
<summary>requirements.txt（参考）</summary>

```
openai>=1.25.0
chromadb>=0.5.0
python-dotenv>=1.0.0
```
</details>

### 4. 配置环境变量
项目通过 **阿里云百炼 OpenAI 兼容接口** 调用 Qwen 模型：

```bash
export ALI_API_KEY="<你的 API Key>"
export ALI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
```

> 也可在根目录新建 `.env` 文件，写入同名变量后自动加载。

### 5. 运行 Demo
```bash
$ python main.py
```
终端将输出用户问题与 AI 回答。

## 🗂️ 目录结构
```
├── embed.py        # 文本分块 + 向量化 + 写入 ChromaDB
├── main.py         # 检索 + 生成（RAG 主逻辑）
├── test_novel.md   # 示例知识库：架空穿越小说片段
├── chroma.db/      # Chroma 持久向量库（首次运行后自动生成）
└── README.md
```

## 🔍 工作流程
| 步骤 | 文件 | 关键函数 | 说明 |
| ---- | ---- | -------- | ---- |
| 1 | `embed.py` | `get_chunks()` | 将长文档按 Markdown 标题或空行切块 |
| 2 |  | `embed()` | 使用 `text-embedding-v4` 生成 1024 维向量 |
| 3 |  | `create_db()` | 向 ChromaDB `Newton` 集合写入 `id/document/embedding` |
| 4 | `main.py` | `search_db()` | 通过查询向量召回 `n_results` 条最相近文档 |
| 5 |  | `chat.completions.create()` | 将检索结果填入 Prompt，让 `qwen-plus-2025-04-28` 回答 |

> 以上 1-3 步仅在首次运行或源文档更新后执行；检索与生成可迭代调用，高效低延迟。

## 🔧 自定义
- **接入其他模型**：更换 `model_config` 中的 `model` / `base_url` 即可。
- **修改分块策略**：在 `get_chunks()` 中加入正则或 `tiktoken` 字数限制。
- **调整召回数量**：在 `search_db()` 中修改 `n_results`。
- **替换知识库**：把你的 Markdown/TXT 路径填入 `main.py:file`。

<!-- ## 📈 Roadmap
- [ ] 支持 PDF / HTML 等多格式解析
- [ ] Streamlit 网页 Demo
- [ ] 自动评测（retrieval precision / answer faithfulness）
- [ ] Docker 一键部署 -->

## 🤝 贡献
欢迎提交 PR / Issue 与我一起改进！


## 运行例子

**1️⃣ 牛顿掌管钦天监之后，还做了什么事，获得了百姓的认可？**

**Answer：**

牛顿掌管钦天监之后，不仅负责观星测象，还着手厘清天下田亩、更定税制。他采用新的测量方法，运用几何学原理和三角测法，将不规则的田亩划分为三角形、方矩等形状，并通过精密计算重新核定田亩面积和赋税。

这种方法精准高效，使得隐匿田亩逃税的行为无所遁形，从而实现了赋役公平，改善了百姓负担。起初百姓对此持怀疑态度，但随着赋税更加合理，许多原本因赋税不公而苦恼的平民得到了实际利益，因此逐渐认可了他的做法，并“额手称庆”。最终，牛顿赢得了百姓的支持与赞誉。

---

**2️⃣ 牛顿在军事上有什么作为？**

**Answer：**

牛顿在军事上的作为主要体现在以下几个方面：

1. **制造“千里镜”（望远镜）**  
   牛顿制造了一架长达六尺、粗如碗口的铜管望远镜。此物被用于战场侦察，在皇帝登临德胜门敌楼时，通过它能够清晰地看到北方敌营的细节，包括敌军的刁斗器具和士卒的须眉。

2. **改良配重投石机**  
   他改良了传统的配重投石机，调整梢杆曲度与配重，并运用数学原理（抛物线理论）精确计算抛射轨迹。试射时，斗大的石弹呼啸而出，精准度极高，远超旧式弩炮。此武器对瓦剌军队造成重大打击，直接导致瓦剌遣使乞和，解除了关城之围。

3. **利用巨镜聚焦阳光奇袭敌军粮仓**  
   在督军雁门关期间，牛顿命人连夜赶制数百面等人的巨镜，镜面平滑如银湖。他选择晴朗天气亲自率死士绕行险峻山径，将巨镜运至俯瞰敌军粮仓的山脊，计划利用镜面反射阳光烧毁敌军粮草，从而削弱敌军后勤补给能力。

---

**3️⃣你觉得牛顿对于自己原来的世界的感情如何？**

**Answer：**

从文档内容来看，牛顿虽然身处一个完全陌生的古代东方王朝背景中，却始终保持着对自己原本世界的深深执着。这种情感体现在以下几个方面：

1. **科学使命的坚守**  
   牛顿即便卷入宫廷纷争和战争危机，仍未放弃学术追求。他在宴散人静时“褪去华服”，取出藏在蟒袍中的《自然哲学的数学原理》手稿继续写作，表明他对科学研究的热爱与责任感超越了外界环境变化。

2. **理性精神的体现**  
   无论是用万有引力定律预测日食、改革田亩赋税，还是制造望远镜与抛物线投石机，牛顿始终以理性态度面对世界。他试图用自身知识体系理解和改变这个陌生世界，体现了对科学世界观的坚定信念。

3. **文化疏离感的暗示**  
   牛顿行为多次与周围环境格格不入，如蟒袍中藏莎草纸稿、使用鹅毛笔书写拉丁文而非汉文，透露出他对当前世界文化的疏离感，以及对原世界的怀念与认同。

4. **理想主义者的孤独**  
   尽管获得皇帝赏识并立下功勋，牛顿并未真正融入朝廷体系，甚至成为世家大族眼中钉，遭到刺杀威胁。他坚持自我，显示出对原世界价值观的忠诚。

**总结**  
牛顿对自己原来世界的情感深沉而坚定。即使身处异域、披上官袍，他依旧心系科学探索，展现出跨越时空的理想主义者情怀。

---

