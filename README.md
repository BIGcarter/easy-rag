# 动手实现一个简易版 RAG！

> Retrieval-Augmented Generation from scratch with Python, OpenAI & ChromaDB

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

整个流程仅依赖 ~100 行 Python 代码，方便理解与二次开发。

## 🚀 快速开始

### 1. 克隆项目
```bash
$ git clone https://github.com/<your-name>/easy-rag.git
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


