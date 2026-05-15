# AI Research Hub

多模型 AI 研究助手 — 自动化论文分析、代码生成与知识综合

![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Models](https://img.shields.io/badge/models-8+-orange)

## 项目简介

AI Research Hub 是一个基于多模型的 AI 研究辅助工具，支持自动化论文分析、代码生成、知识图谱构建和跨模型对比评估。项目日常消耗约 **500万 Token**，覆盖 Claude、GPT、Gemini、MiMo 等主流模型。

## 核心功能

### 📄 论文自动分析
- 输入 arXiv 论文链接，自动生成结构化摘要
- 提取关键算法、实验结果和创新点
- 支持批量处理，一次分析 10+ 篇论文
- 自动翻译为中文并生成阅读笔记

### 💻 代码生成与审查
- 基于论文描述自动生成可运行代码
- 支持 Python、TypeScript、Solidity
- 自动添加测试用例和文档
- 代码质量评分与安全审查

### 🔗 知识图谱构建
- 从论文和文档中提取实体关系
- 自动生成概念依赖图
- 支持可视化展示和导出
- 跨领域知识关联发现

### 📊 多模型对比评估
- 同一任务在多个模型上运行
- 比较输出质量、延迟和成本
- 自动生成评估报告
- 模型选型建议

## 技术架构

```
┌─────────────────────────────────────┐
│         Research Interface          │
├──────────┬──────────┬───────────────┤
│  论文    │  代码    │  知识图谱     │
│  分析    │  生成    │  构建         │
├──────────┴──────────┴───────────────┤
│        Multi-Model Router           │
├─────────┬─────────┬─────────────────┤
│ Claude  │  GPT    │  Gemini / MiMo  │
│ Haiku   │  4o     │  Flash / v2.5   │
└─────────┴─────────┴─────────────────┘
```

## 支持的模型

| 模型 | 提供商 | 用途 | 日均消耗 |
|------|--------|------|----------|
| Claude Haiku 4.5 | Anthropic | 快速分析 | ~200万 Token |
| Claude Sonnet 4 | Anthropic | 深度分析 | ~100万 Token |
| GPT-4o | OpenAI | 代码生成 | ~80万 Token |
| GPT-4o-mini | OpenAI | 轻量任务 | ~30万 Token |
| Gemini Flash | Google | 多模态 | ~50万 Token |
| MiMo v2.5 Pro | Xiaomi | 推理任务 | ~20万 Token |
| DeepSeek Chat | DeepSeek | 中文处理 | ~10万 Token |
| Qwen Max | Alibaba | 中文理解 | ~10万 Token |

**日均总消耗：约 500万 Token**

## 项目结构

```
ai-research-hub/
├── src/
│   ├── analyzers/
│   │   ├── paper_analyzer.py      # 论文分析引擎
│   │   ├── code_generator.py      # 代码生成器
│   │   └── knowledge_graph.py     # 知识图谱构建
│   ├── models/
│   │   ├── router.py              # 多模型路由
│   │   ├── tracker.py             # Token 消耗追踪
│   │   └── evaluator.py           # 模型评估
│   ├── utils/
│   │   ├── arxiv_client.py        # arXiv API 客户端
│   │   ├── translator.py          # 自动翻译
│   │   └── formatter.py           # 输出格式化
│   └── config.py                  # 配置管理
├── notebooks/
│   ├── paper_analysis_demo.ipynb  # 论文分析演示
│   ├── code_gen_demo.ipynb        # 代码生成演示
│   └── token_usage_report.ipynb   # Token 使用报告
├── tests/
│   ├── test_analyzer.py
│   ├── test_generator.py
│   └── test_integration.py
├── docs/
│   ├── usage_guide.md             # 使用指南
│   ├── api_reference.md           # API 参考
│   └── token_optimization.md      # Token 优化策略
├── requirements.txt
└── README.md
```

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."
export XIAOMI_MIMO_API_KEY="..."

# 分析论文
python -m src.analyzers.paper_analyzer --url https://arxiv.org/abs/2401.xxxxx

# 生成代码
python -m src.analyzers.code_generator --prompt "实现一个基于 Transformer 的时序预测模型"

# 构建知识图谱
python -m src.analyzers.knowledge_graph --input papers/ --output graph.json
```

## Token 消耗统计

| 月份 | 总消耗 | 任务数 | 平均/任务 |
|------|--------|--------|-----------|
| 2026-04 | 1.2亿 Token | 2,400 | 50,000 |
| 2026-05 | 1.5亿 Token（截至15日） | 3,000 | 50,000 |

## 使用场景

1. **学术研究** — 快速理解大量论文，发现研究趋势
2. **代码开发** — 基于论文快速实现算法原型
3. **技术调研** — 多模型对比，选择最佳方案
4. **知识管理** — 构建个人知识库，支持语义检索

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
