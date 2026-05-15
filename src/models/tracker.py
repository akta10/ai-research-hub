"""
AI Research Hub — Token 消耗追踪器

实时追踪多模型 Token 消耗，生成使用报告
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Optional


class TokenTracker:
    """Token 消耗追踪与报告"""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "token_usage.jsonl")
        self._ensure_log_file()

    def _ensure_log_file(self):
        """确保日志文件存在"""
        if not os.path.exists(self.log_file):
            open(self.log_file, "w").close()

    def log(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        task_type: str,
        cost: float = 0.0,
    ):
        """记录 Token 使用"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "task_type": task_type,
            "cost": cost,
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_daily_usage(self, date: Optional[str] = None) -> Dict:
        """获取指定日期的使用统计"""
        date = date or datetime.now().strftime("%Y-%m-%d")
        stats = defaultdict(lambda: {"tokens": 0, "count": 0, "cost": 0.0})

        with open(self.log_file) as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                entry_date = entry["timestamp"][:10]
                if entry_date == date:
                    model = entry["model"]
                    stats[model]["tokens"] += entry["total_tokens"]
                    stats[model]["count"] += 1
                    stats[model]["cost"] += entry.get("cost", 0)

        return {
            "date": date,
            "models": dict(stats),
            "total_tokens": sum(s["tokens"] for s in stats.values()),
            "total_cost": sum(s["cost"] for s in stats.values()),
            "total_requests": sum(s["count"] for s in stats.values()),
        }

    def get_monthly_usage(self, month: Optional[str] = None) -> Dict:
        """获取月度使用统计"""
        month = month or datetime.now().strftime("%Y-%m")
        model_stats = defaultdict(lambda: {"tokens": 0, "count": 0, "cost": 0.0})
        daily_stats = defaultdict(int)

        with open(self.log_file) as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                entry_month = entry["timestamp"][:7]
                if entry_month == month:
                    model = entry["model"]
                    model_stats[model]["tokens"] += entry["total_tokens"]
                    model_stats[model]["count"] += 1
                    model_stats[model]["cost"] += entry.get("cost", 0)
                    daily_stats[entry["timestamp"][:10]] += entry["total_tokens"]

        return {
            "month": month,
            "models": dict(model_stats),
            "daily": dict(daily_stats),
            "total_tokens": sum(s["tokens"] for s in model_stats.values()),
            "total_cost": sum(s["cost"] for s in model_stats.values()),
            "total_requests": sum(s["count"] for s in model_stats.values()),
        }

    def generate_report(self, days: int = 30) -> str:
        """生成使用报告"""
        monthly = self.get_monthly_usage()
        daily = self.get_daily_usage()

        report = f"""# AI Research Hub — Token 使用报告

## 月度统计 ({monthly['month']})

| 指标 | 数值 |
|------|------|
| 总消耗 | {monthly['total_tokens']:,} Token |
| 总请求 | {monthly['total_requests']:,} 次 |
| 总成本 | ${monthly['total_cost']:.2f} |

### 模型分布

| 模型 | Token 消耗 | 请求次数 | 成本 |
|------|-----------|----------|------|
"""
        for model, stats in sorted(
            monthly["models"].items(),
            key=lambda x: x[1]["tokens"],
            reverse=True,
        ):
            report += f"| {model} | {stats['tokens']:,} | {stats['count']:,} | ${stats['cost']:.4f} |\n"

        report += f"""
### 今日统计 ({daily['date']})

| 指标 | 数值 |
|------|------|
| 消耗 | {daily['total_tokens']:,} Token |
| 请求 | {daily['total_requests']:,} 次 |
| 成本 | ${daily['total_cost']:.4f} |

---
*报告由 AI Research Hub 自动生成*
"""
        return report


# 全局实例
tracker = TokenTracker()
