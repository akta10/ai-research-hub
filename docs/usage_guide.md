# 使用指南

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

```bash
# 方式一：环境变量
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."
export XIAOMI_MIMO_API_KEY="..."

# 方式二：.env 文件
cp .env.example .env
# 编辑 .env 填入你的 API 密钥
```

### 3. 分析论文

```python
from src.analyzers.paper_analyzer import analyzer

# 分析单篇论文
result = await analyzer.analyze_from_url("https://arxiv.org/abs/2401.xxxxx")
print(result.chinese_summary)

# 生成中文笔记
notes = await analyzer.generate_chinese_notes(result)
print(notes)
```

### 4. 生成代码

```python
from src.models.router import generate_code, TaskType

# 基于论文生成代码
result = await generate_code("实现一个基于 Transformer 的时序预测模型")
print(result["output"])
print(f"Token 消耗: {result['total_tokens']}")
```

## 高级用法

### 批量分析

```python
urls = [
    "https://arxiv.org/abs/2401.00001",
    "https://arxiv.org/abs/2401.00002",
    "https://arxiv.org/abs/2401.00003",
]

results = await analyzer.batch_analyze(urls, model="claude-haiku")
for r in results:
    print(f"{r.title}: {r.relevance_score:.0%}")
```

### 模型对比

```python
from src.models.router import router, TaskType

# 同一任务在不同模型上运行
models = ["claude-haiku", "gpt-4o", "gemini-flash"]
for model in models:
    result = await router.execute(
        "总结这篇论文的核心贡献",
        TaskType.SUMMARIZATION,
        model=model,
    )
    print(f"{model}: {result['total_tokens']} tokens, ${result['cost']:.4f}")
```

### 生成使用报告

```python
from src.models.tracker import tracker

# 生成月度报告
report = tracker.generate_report(days=30)
print(report)
```

## Token 优化建议

1. **选择合适的模型** — 简单任务用 Haiku/Flash，复杂任务用 Sonnet/GPT-4o
2. **缓存结果** — 相同论文不重复分析
3. **批量处理** — 一次请求处理多篇论文
4. **控制输出长度** — 设置合理的 max_tokens
5. **使用中文模型** — 中文任务优先用 MiMo/DeepSeek/Qwen

## 常见问题

**Q: 如何查看 Token 消耗？**
A: 访问 `http://localhost:8080/stats` 或查看 `logs/token_usage.jsonl`

**Q: 支持哪些论文格式？**
A: 支持 arXiv 链接、PDF 文件、纯文本

**Q: 如何添加新模型？**
A: 在 `src/models/router.py` 的 `MODELS` 字典中添加配置

## 相关链接

- [arXiv API 文档](https://info.arxiv.org/help/api/index.html)
- [Anthropic API 文档](https://docs.anthropic.com/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [Google AI 文档](https://ai.google.dev/)
