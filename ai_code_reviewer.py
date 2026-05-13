#!/usr/bin/env python3
"""
AI Code Reviewer - 基于DeepSeek API的智能代码审查工具
自动分析代码质量、发现潜在Bug、提出改进建议，并生成结构化审查报告。

Author: AI Tools Workshop
Version: 1.0.0
License: MIT
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

# ============================================================
# 配置
# ============================================================
DEFAULT_API_URL = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.3


# ============================================================
# HTTP 客户端（纯标准库，零依赖）
# ============================================================

def _make_http_request(url, headers, body=None, method="POST", timeout=120):
    """纯标准库 HTTP 请求，兼容 Python 3.6+"""
    import urllib.request
    import urllib.error
    req = urllib.request.Request(url, data=body, method=method)
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": resp.status, "body": resp.read().decode("utf-8")}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "body": e.read().decode("utf-8", errors="replace")}
    except Exception as e:
        return {"status": 0, "body": str(e)}


def call_deepseek_api(api_key, prompt, model=None, max_tokens=None,
                      temperature=None, api_url=None):
    """调用 DeepSeek Chat API"""
    if model is None: model = DEFAULT_MODEL
    if max_tokens is None: max_tokens = DEFAULT_MAX_TOKENS
    if temperature is None: temperature = DEFAULT_TEMPERATURE
    if api_url is None: api_url = DEFAULT_API_URL

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "\u4f60\u662f\u4e00\u4f4d\u8d44\u6df1\u4ee3\u7801\u5ba1\u67e5\u4e13\u5bb6\uff0c\u64c5\u957f\u53d1\u73b0\u4ee3\u7801\u4e2d\u7684Bug\u3001\u5b89\u5168\u6f0f\u6d1e\u3001\u6027\u80fd\u95ee\u9898\u548c\u8bbe\u8ba1\u7f3a\u9677\u3002\u8bf7\u7528\u4e2d\u6587\u56de\u7b54\u3002"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    result = _make_http_request(api_url, headers, json.dumps(payload).encode("utf-8"))
    if result["status"] != 200:
        raise RuntimeError("API\u8bf7\u6c42\u5931\u8d25 (HTTP {}): {}".format(
            result["status"], result["body"][:500]))
    data = json.loads(result["body"])
    return data["choices"][0]["message"]["content"]


# ============================================================
# 文件读取
# ============================================================

def read_file_content(filepath):
    """读取文件内容，自动检测编码"""
    for enc in ["utf-8", "utf-8-sig", "gbk", "gb2312", "latin-1"]:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    return None


def collect_code_files(path, extensions=None, exclude_dirs=None):
    """收集指定路径下的代码文件"""
    if extensions is None:
        extensions = [
            ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp",
            ".h", ".hpp", ".cs", ".go", ".rs", ".rb", ".php", ".swift",
            ".kt", ".scala", ".html", ".css", ".scss", ".less", ".vue",
            ".svelte", ".sql", ".sh", ".bash", ".ps1", ".yaml", ".yml",
            ".json", ".xml", ".toml"
        ]
    if exclude_dirs is None:
        exclude_dirs = {
            "node_modules", ".git", "__pycache__", "venv", ".venv", "env",
            "dist", "build", ".idea", ".vscode", "target", "vendor", ".tox",
            ".mypy_cache", ".pytest_cache", "egg-info"
        }
    files = []
    p = Path(path)
    if p.is_file():
        files.append(str(p))
        return files
    for root, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in extensions:
                files.append(os.path.join(root, fname))
    return sorted(files)


# ============================================================
# Prompt 构建
# ============================================================

REVIEW_PROMPT_TEMPLATE = """请对以下 {language} 代码进行专业审查，生成详细的审查报告。

## 要求
1. 按严重程度分类：🔴 严重问题(Bug/安全) / 🟡 中等问题(性能/设计) / 🟢 建议改进(风格/可读性)
2. 每个问题标注行号范围
3. 给出具体的修复建议和示例代码
4. 最后给出整体评分(1-10)和总结

## 代码信息
- 文件: {filename}
- 语言: {language}
- 代码行数: {lines}

## 代码内容
```{language}
{code}
```

请按以下格式输出：

# 代码审查报告

## 概览
[简短概述代码功能和整体质量]

## 🔴 严重问题
[列出严重Bug和安全漏洞，无则标注"无"]

## 🟡 中等问题
[列出性能和设计问题]

## 🟢 改进建议
[列出代码风格和可读性建议]

## 评分与总结
- 评分: X/10
- 总结: [一段话总结]
"""

DIFF_REVIEW_PROMPT = """请审查以下 Git Diff，关注变更中引入的问题。

## 文件: {filename}

```diff
{diff}
```

请重点检查：
1. 新引入的Bug或逻辑错误
2. 安全漏洞
3. 性能退化
4. 缺失的错误处理
5. 代码风格问题

按严重程度分类输出（🔴严重 / 🟡中等 / 🟢建议），并给出修复建议。
"""


# ============================================================
# 语言检测与Prompt工具
# ============================================================

def detect_language(filename):
    """根据文件扩展名检测编程语言"""
    ext_map = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".jsx": "jsx", ".tsx": "tsx", ".java": "java",
        ".c": "c", ".cpp": "cpp", ".h": "c", ".hpp": "cpp",
        ".cs": "csharp", ".go": "go", ".rs": "rust",
        ".rb": "ruby", ".php": "php", ".swift": "swift",
        ".kt": "kotlin", ".scala": "scala",
        ".html": "html", ".css": "css", ".scss": "scss",
        ".sql": "sql", ".sh": "bash", ".yaml": "yaml",
        ".json": "json", ".xml": "xml", ".toml": "toml",
        ".vue": "vue", ".svelte": "svelte",
    }
    return ext_map.get(os.path.splitext(filename)[1].lower(), "text")


def build_review_prompt(code, filename, language=None):
    """构建代码审查 Prompt"""
    if language is None:
        language = detect_language(filename)
    return REVIEW_PROMPT_TEMPLATE.format(
        language=language, filename=filename,
        lines=len(code.splitlines()), code=code)


def build_diff_review_prompt(diff_content, filename="multiple files"):
    """构建 Diff 审查 Prompt"""
    return DIFF_REVIEW_PROMPT.format(filename=filename, diff=diff_content)


# ============================================================
# 报告生成
# ============================================================

def generate_report(content_str, filename):
    """生成格式化的审查报告"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hdr = "# AI Code Review Report\n\n"
    hdr += "- **File**: `{}`\n".format(filename)
    hdr += "- **Time**: {}\n".format(ts)
    hdr += "- **Reviewer**: AI Code Reviewer (DeepSeek)\n\n"
    hdr += "{}\n\n".format("=" * 60)
    return hdr + content_str


def save_report(report, output_path):
    """保存报告到文件"""
    d = os.path.dirname(output_path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print("[OK] 报告已保存到: {}".format(output_path))


# ============================================================
# GitHub Actions 集成
# ============================================================

def set_github_output(key, value):
    """设置 GitHub Actions 输出变量"""
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        delim = "ghadelimiter_{}".format(abs(hash(key)) % 100000)
        with open(gh_output, "a", encoding="utf-8") as f:
            f.write("{}<<{}\n{}\n{}\n".format(key, delim, value, delim))
    print("[GitHub Actions] Output: {}".format(key))


def write_github_summary(report):
    """写入 GitHub Actions Job Summary"""
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(report + "\n\n")
        print("[GitHub Actions] 已写入 Step Summary")
    else:
        print("[Info] 非GitHub Actions环境，跳过Summary写入")


# ============================================================
# 核心审查流程
# ============================================================

def review_single_file(filepath, api_key, model=None, api_url=None):
    """审查单个代码文件"""
    print("[Review] 正在审查: {}".format(filepath))
    code = read_file_content(filepath)
    if code is None:
        print("[WARN] 无法读取文件: {}".format(filepath))
        return "# 无法读取文件: {}\n\n跳过。".format(filepath)
    language = detect_language(filepath)
    prompt = build_review_prompt(code, os.path.basename(filepath), language)
    result = call_deepseek_api(api_key, prompt, model=model, api_url=api_url)
    return generate_report(result, filepath)


def review_directory(dirpath, api_key, model=None, api_url=None,
                     extensions=None, max_files=20):
    """审查目录下所有代码文件"""
    files = collect_code_files(dirpath, extensions=extensions)
    if not files:
        return "# 未找到可审查的代码文件\n\n请检查路径和文件扩展名。"
    if len(files) > max_files:
        print("[WARN] 发现 {} 个文件，仅审查前 {} 个（可通过 --max-files 调整）".format(
            len(files), max_files))
        files = files[:max_files]
    reports = []
    for i, f in enumerate(files, 1):
        print("\n--- [{}/{}] ---".format(i, len(files)))
        try:
            reports.append(review_single_file(f, api_key, model=model, api_url=api_url))
        except Exception as e:
            reports.append("# 审查失败: {}\n\n错误: {}".format(f, str(e)))
            print("[ERROR] {}".format(e))
    return "\n\n---\n\n".join(reports)


def review_diff(diff_path, api_key, model=None, api_url=None):
    """审查 Git Diff 文件"""
    print("[Review Diff] {}".format(diff_path))
    diff_content = read_file_content(diff_path)
    if diff_content is None:
        raise RuntimeError("无法读取diff文件: {}".format(diff_path))
    prompt = build_diff_review_prompt(diff_content)
    result = call_deepseek_api(api_key, prompt, model=model, api_url=api_url)
    return generate_report(result, diff_path)


# ============================================================
# CLI 入口
# ============================================================

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="AI Code Reviewer - 基于DeepSeek API的智能代码审查工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""使用示例:
  # 审查单个文件
  python ai_code_reviewer.py --file main.py

  # 审查整个项目
  python ai_code_reviewer.py --dir ./src

  # 审查Git Diff（CI/CD集成）
  python ai_code_reviewer.py --diff diff.patch

  # 指定模型和输出
  python ai_code_reviewer.py --file app.py --model deepseek-reasoner -o report.md

  # GitHub Actions 模式
  python ai_code_reviewer.py --dir ./src --ci

环境变量:
  DEEPSEEK_API_KEY    DeepSeek API密钥（必需）
  DEEPSEEK_API_URL    API地址（可选，默认官方地址）
  DEEPSEEK_MODEL      模型名称（可选）
""")

    # 输入源（互斥）
    ig = parser.add_mutually_exclusive_group(required=True)
    ig.add_argument("--file", "-f", help="审查单个代码文件")
    ig.add_argument("--dir", "-d", help="审查整个目录")
    ig.add_argument("--diff", help="审查Git diff文件（unified diff格式）")

    # 可选参数
    parser.add_argument("--api-key", help="DeepSeek API Key（也可通过环境变量设置）")
    parser.add_argument("--model", "-m", help="模型名称（默认: deepseek-chat）")
    parser.add_argument("--api-url", help="API地址（支持自定义/代理地址）")
    parser.add_argument("--output", "-o", help="报告输出文件路径")
    parser.add_argument("--extensions", "-e", nargs="+", help="要审查的文件扩展名（如 .py .js）")
    parser.add_argument("--max-files", type=int, default=20, help="最大审查文件数（默认: 20）")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS, help="API最大token数")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE, help="生成温度（0-1）")
    parser.add_argument("--ci", action="store_true", help="CI/CD模式（GitHub Actions集成）")

    args = parser.parse_args()

    # 获取API Key
    api_key = args.api_key or os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("[ERROR] 请设置 DEEPSEEK_API_KEY 环境变量或使用 --api-key 参数")
        sys.exit(1)

    api_url = args.api_url or os.environ.get("DEEPSEEK_API_URL", DEFAULT_API_URL)
    model = args.model or os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL)

    print("AI Code Reviewer v1.0.0")
    print("Model: {}".format(model))
    print("API: {}".format(api_url))
    print("-" * 40)

    try:
        # 执行审查
        if args.file:
            report = review_single_file(args.file, api_key, model=model, api_url=api_url)
        elif args.dir:
            report = review_directory(args.dir, api_key, model=model, api_url=api_url,
                                     extensions=args.extensions, max_files=args.max_files)
        elif args.diff:
            report = review_diff(args.diff, api_key, model=model, api_url=api_url)

        # 输出结果
        if args.output:
            save_report(report, args.output)
        else:
            print("\n" + report)

        # GitHub Actions 集成
        if args.ci:
            write_github_summary(report)
            score_match = re.search(r"评分[：:]\s*(\d+(?:\.\d+)?)[/／]10", report)
            if score_match:
                set_github_output("review_score", score_match.group(1))
            set_github_output("review_status", "completed")

        print("\n[DONE] 审查完成!")

    except KeyboardInterrupt:
        print("\n[ABORT] 用户中断")
        sys.exit(130)
    except Exception as e:
        print("\n[FATAL] {}".format(e))
        if args.ci:
            set_github_output("review_status", "failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
