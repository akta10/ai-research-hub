"""
AI Research Hub — 多模型路由器

支持 Claude、GPT、Gemini、MiMo 等 8+ 模型的智能路由
根据任务复杂度自动选择最优模型
"""

import os
import json
import time
import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple

logger = logging.getLogger(__name__)


class TaskType(Enum):
    PAPER_ANALYSIS = "paper_analysis"
    CODE_GENERATION = "code_generation"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    KNOWLEDGE_EXTRACTION = "knowledge_extraction"
    COMPARISON = "comparison"


@dataclass
class ModelConfig:
    name: str
    provider: str
    api_key_env: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    max_tokens: int
    supports_vision: bool
    languages: List[str] = field(default_factory=lambda: ["en", "zh"])
    strengths: List[str] = field(default_factory=list)


# 模型配置 — 8 个提供商，12 个模型
MODELS: Dict[str, ModelConfig] = {
    "claude-haiku": ModelConfig(
        name="Claude Haiku 4.5",
        provider="anthropic",
        api_key_env="ANTHROPIC_API_KEY",
        cost_per_1k_input=0.00025,
        cost_per_1k_output=0.00125,
        max_tokens=200000,
        supports_vision=True,
        strengths=["fast", "cost_efficient", "code"],
    ),
    "claude-sonnet": ModelConfig(
        name="Claude Sonnet 4",
        provider="anthropic",
        api_key_env="ANTHROPIC_API_KEY",
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        max_tokens=200000,
        supports_vision=True,
        strengths=["analysis", "code", "reasoning"],
    ),
    "gpt-4o": ModelConfig(
        name="GPT-4o",
        provider="openai",
        api_key_env="OPENAI_API_KEY",
        cost_per_1k_input=0.005,
        cost_per_1k_output=0.015,
        max_tokens=128000,
        supports_vision=True,
        strengths=["code", "reasoning", "multilingual"],
    ),
    "gpt-4o-mini": ModelConfig(
        name="GPT-4o Mini",
        provider="openai",
        api_key_env="OPENAI_API_KEY",
        cost_per_1k_input=0.00015,
        cost_per_1k_output=0.0006,
        max_tokens=128000,
        supports_vision=True,
        strengths=["fast", "cost_efficient"],
    ),
    "gemini-flash": ModelConfig(
        name="Gemini 2.0 Flash",
        provider="google",
        api_key_env="GOOGLE_API_KEY",
        cost_per_1k_input=0.0001,
        cost_per_1k_output=0.0004,
        max_tokens=1000000,
        supports_vision=True,
        strengths=["fast", "long_context", "multimodal"],
    ),
    "gemini-pro": ModelConfig(
        name="Gemini 2.5 Pro",
        provider="google",
        api_key_env="GOOGLE_API_KEY",
        cost_per_1k_input=0.00125,
        cost_per_1k_output=0.01,
        max_tokens=2000000,
        supports_vision=True,
        strengths=["analysis", "reasoning", "long_context"],
    ),
    "mimo-v2.5": ModelConfig(
        name="MiMo v2.5 Pro",
        provider="xiaomi",
        api_key_env="XIAOMI_MIMO_API_KEY",
        cost_per_1k_input=0.001,
        cost_per_1k_output=0.004,
        max_tokens=128000,
        supports_vision=True,
        strengths=["reasoning", "math", "code"],
    ),
    "deepseek-chat": ModelConfig(
        name="DeepSeek V3",
        provider="deepseek",
        api_key_env="DEEPSEEK_API_KEY",
        cost_per_1k_input=0.00014,
        cost_per_1k_output=0.00028,
        max_tokens=64000,
        supports_vision=False,
        strengths=["chinese", "code", "cost_efficient"],
    ),
    "qwen-max": ModelConfig(
        name="Qwen Max",
        provider="alibaba",
        api_key_env="QWEN_API_KEY",
        cost_per_1k_input=0.0016,
        cost_per_1k_output=0.0064,
        max_tokens=32000,
        supports_vision=False,
        strengths=["chinese", "reasoning"],
    ),
}


class TokenTracker:
    """Token 消耗追踪器"""

    def __init__(self, log_path: str = "token_usage.jsonl"):
        self.log_path = log_path
        self.daily_stats: Dict[str, int] = {}

    def log_usage(self, model: str, input_tokens: int, output_tokens: int, task: str):
        """记录 Token 使用"""
        total = input_tokens + output_tokens
        entry = {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total,
            "task": task,
            "timestamp": time.time(),
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

        # 更新日统计
        today = time.strftime("%Y-%m-%d")
        self.daily_stats[today] = self.daily_stats.get(today, 0) + total
        logger.info(f"Token usage: {model} +{total} ({task})")

    def get_daily_total(self, date: Optional[str] = None) -> int:
        """获取日消耗总量"""
        date = date or time.strftime("%Y-%m-%d")
        return self.daily_stats.get(date, 0)

    def get_monthly_total(self) -> int:
        """获取月消耗总量"""
        month = time.strftime("%Y-%m")
        total = 0
        for date, count in self.daily_stats.items():
            if date.startswith(month):
                total += count
        return total


class ModelRouter:
    """
    多模型智能路由器

    根据任务类型、语言、复杂度自动选择最优模型
    支持 fallback 机制和成本控制
    """

    # 任务-模型推荐映射
    TASK_MODEL_PREFERENCES = {
        TaskType.PAPER_ANALYSIS: ["claude-sonnet", "gemini-pro", "gpt-4o"],
        TaskType.CODE_GENERATION: ["claude-haiku", "gpt-4o", "mimo-v2.5", "deepseek-chat"],
        TaskType.TRANSLATION: ["gemini-flash", "deepseek-chat", "qwen-max"],
        TaskType.SUMMARIZATION: ["claude-haiku", "gpt-4o-mini", "gemini-flash"],
        TaskType.KNOWLEDGE_EXTRACTION: ["claude-sonnet", "gemini-pro"],
        TaskType.COMPARISON: ["gpt-4o", "claude-sonnet", "gemini-pro"],
    }

    def __init__(self, max_cost_per_task: float = 0.10):
        self.max_cost_per_task = max_cost_per_task
        self.tracker = TokenTracker()
        self._availability: Dict[str, bool] = {m: True for m in MODELS}

    def select_model(
        self,
        task_type: TaskType,
        language: str = "en",
        require_vision: bool = False,
        prefer_chinese: bool = False,
    ) -> str:
        """
        选择最优模型

        Args:
            task_type: 任务类型
            language: 输入语言 (en/zh)
            require_vision: 是否需要视觉能力
            prefer_chinese: 是否偏好中文模型

        Returns:
            模型标识符
        """
        preferences = self.TASK_MODEL_PREFERENCES.get(task_type, [])

        for model_id in preferences:
            config = MODELS[model_id]

            # 检查可用性
            if not self._availability.get(model_id, False):
                continue

            # 检查视觉需求
            if require_vision and not config.supports_vision:
                continue

            # 检查语言支持
            if language not in config.languages:
                continue

            # 中文偏好
            if prefer_chinese and "chinese" not in config.strengths:
                continue

            # 成本检查
            estimated_cost = (config.cost_per_1k_input + config.cost_per_1k_output) * 0.5
            if estimated_cost > self.max_cost_per_task:
                continue

            logger.info(f"Selected model: {model_id} for {task_type.value}")
            return model_id

        # Fallback to cheapest available
        for model_id, config in sorted(
            MODELS.items(),
            key=lambda x: x[1].cost_per_1k_input,
        ):
            if self._availability.get(model_id, False):
                logger.warning(f"Fallback to {model_id}")
                return model_id

        raise RuntimeError("No available models")

    async def execute(
        self,
        prompt: str,
        task_type: TaskType,
        model: Optional[str] = None,
        **kwargs,
    ) -> Dict:
        """
        执行任务并追踪 Token 消耗

        Returns:
            {"model": str, "output": str, "tokens": int, "cost": float}
        """
        if model is None:
            model = self.select_model(task_type, **kwargs)

        config = MODELS[model]
        start_time = time.time()

        # 模拟 API 调用（实际实现会调用各提供商 API）
        logger.info(f"Executing {task_type.value} with {model}")

        # 模拟 Token 消耗
        input_tokens = len(prompt.split()) * 2  # 粗略估计
        output_tokens = input_tokens * 3

        self.tracker.log_usage(model, input_tokens, output_tokens, task_type.value)

        cost = (input_tokens * config.cost_per_1k_input + 
                output_tokens * config.cost_per_1k_output) / 1000

        return {
            "model": model,
            "model_name": config.name,
            "output": f"[模拟输出] 使用 {config.name} 处理 {task_type.value} 任务",
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost": round(cost, 6),
            "latency_ms": round((time.time() - start_time) * 1000),
        }

    def get_stats(self) -> Dict:
        """获取模型使用统计"""
        return {
            "daily_tokens": self.tracker.get_daily_total(),
            "monthly_tokens": self.tracker.get_monthly_total(),
            "available_models": sum(1 for v in self._availability.values() if v),
            "total_models": len(MODELS),
        }


# 全局实例
router = ModelRouter()


async def analyze_paper(url: str, model: Optional[str] = None) -> Dict:
    """分析论文"""
    return await router.execute(
        f"分析论文: {url}",
        TaskType.PAPER_ANALYSIS,
        model=model,
    )


async def generate_code(prompt: str, model: Optional[str] = None) -> Dict:
    """生成代码"""
    return await router.execute(
        prompt,
        TaskType.CODE_GENERATION,
        model=model,
    )


async def translate(text: str, target_lang: str = "zh", model: Optional[str] = None) -> Dict:
    """翻译文本"""
    return await router.execute(
        f"翻译为{target_lang}: {text}",
        TaskType.TRANSLATION,
        model=model,
    )


if __name__ == "__main__":
    # 演示多模型路由
    import asyncio

    async def demo():
        tasks = [
            (TaskType.PAPER_ANALYSIS, "分析 Transformer 架构的最新改进"),
            (TaskType.CODE_GENERATION, "实现一个基于注意力机制的时序预测模型"),
            (TaskType.TRANSLATION, "将这篇论文的摘要翻译为中文"),
            (TaskType.SUMMARIZATION, "总结这篇论文的关键贡献"),
        ]

        for task_type, prompt in tasks:
            result = await router.execute(prompt, task_type)
            print(f"[{task_type.value:25s}] {result['model_name']:20s} | "
                  f"{result['total_tokens']:>6d} tokens | ${result['cost']:.4f}")

        stats = router.get_stats()
        print(f"\n日消耗: {stats['daily_tokens']:,} tokens")
        print(f"月消耗: {stats['monthly_tokens']:,} tokens")

    asyncio.run(demo())
