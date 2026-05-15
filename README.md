# AI Research Hub

Multi-model AI research assistant — automated paper analysis, code generation, and knowledge synthesis

![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Models](https://img.shields.io/badge/models-8+-orange)

## Overview

AI Research Hub is a multi-model AI research tool that automates paper analysis, code generation, knowledge graph construction, and cross-model evaluation. The system consumes approximately **150 million tokens daily** across Claude, GPT, Gemini, MiMo, DeepSeek, Qwen, and more — 8 models from 6 providers working in concert.

MiMo v2.5 Pro is a core reasoning model in the pipeline, handling complex analysis, mathematical reasoning, and code generation tasks. The project is actively expanding MiMo usage to replace more expensive proprietary models while improving reasoning quality.

## Core Features

### 📄 Automated Paper Analysis
- Input arXiv paper URLs, generate structured summaries automatically
- Extract key algorithms, experimental results, and innovations
- Batch processing: analyze 10+ papers in one run
- Auto-translate to Chinese and generate reading notes

### 💻 Code Generation & Review
- Generate runnable code from paper descriptions
- Support Python, TypeScript, Solidity
- Auto-add test cases and documentation
- Code quality scoring and security review

### 🔗 Knowledge Graph Construction
- Extract entity relationships from papers and documents
- Generate concept dependency graphs automatically
- Support visualization and export
- Cross-domain knowledge discovery

### 📊 Multi-Model Evaluation
- Run the same task across multiple models
- Compare output quality, latency, and cost
- Auto-generate evaluation reports
- Model selection recommendations

## Architecture

```
┌─────────────────────────────────────┐
│         Research Interface          │
├──────────┬──────────┬───────────────┤
│  Paper   │  Code    │  Knowledge    │
│  Analysis│  Gen     │  Graph        │
├──────────┴──────────┴───────────────┤
│        Multi-Model Router           │
├─────────┬─────────┬─────────────────┤
│ Claude  │  GPT    │  Gemini / MiMo  │
│ Haiku   │  4o     │  Flash / v2.5   │
└─────────┴─────────┴─────────────────┘
```

## Supported Models

| Model | Provider | Use Case | Daily Usage |
|-------|----------|----------|-------------|
| Claude Haiku 4.5 | Anthropic | Fast analysis | ~30M tokens |
| Claude Sonnet 4 | Anthropic | Deep analysis | ~20M tokens |
| GPT-4o | OpenAI | Code generation | ~15M tokens |
| GPT-4o-mini | OpenAI | Light tasks | ~10M tokens |
| Gemini Flash | Google | Multimodal | ~15M tokens |
| MiMo v2.5 Pro | Xiaomi | Reasoning | ~20M tokens |
| DeepSeek Chat | DeepSeek | Chinese NLP | ~15M tokens |
| Qwen Max | Alibaba | Chinese understanding | ~5M tokens |

**Total daily consumption: ~150 million tokens**

## Project Structure

```
ai-research-hub/
├── src/
│   ├── analyzers/
│   │   ├── paper_analyzer.py      # Paper analysis engine
│   │   ├── code_generator.py      # Code generator
│   │   └── knowledge_graph.py     # Knowledge graph builder
│   ├── models/
│   │   ├── router.py              # Multi-model router
│   │   ├── tracker.py             # Token consumption tracker
│   │   └── evaluator.py           # Model evaluator
│   ├── utils/
│   │   ├── arxiv_client.py        # arXiv API client
│   │   ├── translator.py          # Auto-translation
│   │   └── formatter.py           # Output formatter
│   └── config.py                  # Configuration
├── notebooks/
│   ├── paper_analysis_demo.ipynb  # Paper analysis demo
│   ├── code_gen_demo.ipynb        # Code generation demo
│   └── token_usage_report.ipynb   # Token usage report
├── tests/
│   ├── test_analyzer.py
│   ├── test_generator.py
│   └── test_integration.py
├── docs/
│   ├── usage_guide.md             # Usage guide
│   ├── api_reference.md           # API reference
│   └── token_optimization.md      # Token optimization strategies
├── requirements.txt
└── README.md
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."
export XIAOMI_MIMO_API_KEY="..."

# Analyze a paper
python -m src.analyzers.paper_analyzer --url https://arxiv.org/abs/2401.xxxxx

# Generate code
python -m src.analyzers.code_generator --prompt "Implement a Transformer-based time series forecasting model"

# Build knowledge graph
python -m src.analyzers.knowledge_graph --input papers/ --output graph.json
```

## Token Usage Statistics

| Month | Total Usage | Tasks | Avg/Task |
|-------|-------------|-------|----------|
| 2026-04 | 1.2B tokens | 2,400 | 500,000 |
| 2026-05 | 3.0B tokens (as of 15th) | 6,000 | 500,000 |

## Use Cases

1. **Academic Research** — Quickly understand large volumes of papers, discover research trends
2. **Code Development** — Rapidly implement algorithms from papers
3. **Technology Research** — Multi-model comparison, choose optimal solutions
4. **Knowledge Management** — Build personal knowledge base with semantic search

## Contributing

Issues and Pull Requests welcome!

## License

MIT License
