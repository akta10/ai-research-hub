# Usage Guide

## Installation

```bash
git clone https://github.com/akta10/ai-research-hub.git
cd ai-research-hub
pip install -r requirements.txt
```

## Configuration

Set environment variables for the models you want to use:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."      # Claude models
export OPENAI_API_KEY="sk-..."             # GPT models
export GOOGLE_API_KEY="AIza..."            # Gemini models
export XIAOMI_MIMO_API_KEY="..."           # MiMo models
export DEEPSEEK_API_KEY="..."              # DeepSeek models
export DASHSCOPE_API_KEY="..."             # Qwen models
```

## Paper Analysis

```python
from src.analyzers.paper_analyzer import PaperAnalyzer

analyzer = PaperAnalyzer(model="claude-haiku-4.5")
result = analyzer.analyze("https://arxiv.org/abs/2401.xxxxx")
print(result.summary)
print(result.key_findings)
```

## Code Generation

```python
from src.analyzers.code_generator import CodeGenerator

generator = CodeGenerator(model="mimo-v2.5-pro")
code = generator.generate(
    prompt="Implement a Transformer-based time series forecasting model",
    language="python",
    include_tests=True
)
print(code)
```

## Token Tracking

```python
from src.models.tracker import TokenTracker

tracker = TokenTracker()
daily = tracker.get_daily_usage()
monthly = tracker.get_monthly_usage()
print(f"Today: {daily['total_tokens']:,} tokens")
print(f"This month: {monthly['total_tokens']:,} tokens")
```

## Multi-Model Routing

```python
from src.models.router import MultiModelRouter

router = MultiModelRouter()
result = router.route(
    task="Analyze this paper's methodology",
    task_type="analysis",
    preferred_provider="anthropic"
)
```

## Token Optimization Tips

1. Use Claude Haiku for simple tasks — 10x cheaper than Sonnet
2. Use GPT-4o-mini for lightweight tasks — 60x cheaper than GPT-4o
3. Use MiMo v2.5 Pro for reasoning — best quality-to-cost ratio for complex tasks
4. Batch papers together to reduce per-request overhead
5. Cache results for repeated queries
6. Use the tracker to identify cost hotspots

## Usage Statistics

The system processes approximately 150 million tokens daily:

- **Input tokens:** ~100M/day (paper content, prompts, context)
- **Output tokens:** ~50M/day (summaries, code, analysis)
- **Monthly total:** ~3B tokens (partial month)
- **Tasks per day:** ~1,500
- **Avg tokens per task:** ~100,000
