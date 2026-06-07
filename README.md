# AI Code Reviewer - 智能代码审查助手

> 基于DeepSeek API的自动化代码审查工具，零依赖，单文件即可运行。

## 功能特点

- **智能审查** - 调用DeepSeek大模型，自动发现Bug、安全漏洞、性能问题
- **零依赖** - 纯Python标准库，无需pip install任何第三方包
- **多语言支持** - 支持30+编程语言（Python/JS/TS/Java/C++/Go/Rust等）
- **多种模式** - 支持单文件、整个目录、Git Diff三种审查模式
- **CI/CD集成** - 内置GitHub Actions支持，自动输出到Step Summary
- **结构化报告** - 按严重程度分类（🔴严重 🟡中等 🟢建议），给出评分和修复建议

## 快速开始

### 1. 设置API Key

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

> 获取API Key: [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)

### 2. 审查单个文件

```bash
python ai_code_reviewer.py --file main.py
```

### 3. 审查整个项目

```bash
python ai_code_reviewer.py --dir ./src
```

### 4. 审查Git Diff

```bash
git diff > changes.patch
python ai_code_reviewer.py --diff changes.patch
```

## 使用方法

### 命令行参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--file` | `-f` | 审查单个代码文件 |
| `--dir` | `-d` | 审查整个目录 |
| `--diff` | | 审查Git diff文件 |
| `--api-key` | | DeepSeek API Key（或设置环境变量） |
| `--model` | `-m` | 模型名称（默认: deepseek-chat） |
| `--api-url` | | 自定义API地址 |
| `--output` | `-o` | 保存报告到文件 |
| `--extensions` | `-e` | 指定文件扩展名 |
| `--max-files` | | 最大审查文件数（默认: 20） |
| `--temperature` | | 生成温度 0-1（默认: 0.3） |
| `--ci` | | CI/CD模式 |

### 环境变量

| 变量名 | 说明 |
|--------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥（必需） |
| `DEEPSEEK_API_URL` | 自定义API地址（可选） |
| `DEEPSEEK_MODEL` | 模型名称（可选） |

## 使用示例

### 示例1：审查单个Python文件并保存报告

```bash
python ai_code_reviewer.py \
  --file my_app.py \
  --output review_report.md
```

输出示例：
```
AI Code Reviewer v1.0.0
Model: deepseek-chat
API: https://api.deepseek.com/chat/completions
----------------------------------------
[Review] 正在审查: my_app.py

# AI Code Review Report

## 概览
这是一个Flask Web应用，整体结构清晰...

## 🔴 严重问题
1. **SQL注入漏洞** (第42行)
   - 直接拼接用户输入到SQL查询中
   - 修复：使用参数化查询
   ```python
   # Before
   cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
   # After
   cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
   ```

## 🟡 中等问题
...

## 🟢 改进建议
...

## 评分与总结
- 评分: 7/10
- 总结: 代码整体可读性好，但存在SQL注入等安全问题需要立即修复。
```

### 示例2：审查整个项目目录

```bash
python ai_code_reviewer.py \
  --dir ./my-project/src \
  --extensions .py .js .ts \
  --max-files 10 \
  --output full_review.md
```

### 示例3：在Pull Request中自动审查（GitHub Actions）

```yaml
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Generate diff
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > pr_changes.patch
      - name: AI Code Review
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: |
          python ai_code_reviewer.py \
            --diff pr_changes.patch \
            --ci \
            --output review.md
```

## 审查报告格式

| 级别 | 标记 | 说明 |
|------|------|------|
| 严重 | 🔴 | Bug、安全漏洞、数据丢失风险 |
| 中等 | 🟡 | 性能问题、设计缺陷、可维护性 |
| 建议 | 🟢 | 代码风格、命名规范、可读性 |

## 支持的语言

Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, HTML, CSS, SCSS, SQL, Shell, YAML, JSON, XML, TOML, Vue, Svelte 等30+种语言。

## 系统要求

- Python 3.6+
- DeepSeek API Key
- 网络连接（调用API）

---

## 💰 商品信息

| 项目 | 内容 |
|------|------|
| **闲鱼售价** | **¥39**（原价¥99，限时特惠） |
| **一句话卖点** | 一行命令审查30+语言代码，AI自动发现Bug和安全漏洞——程序员的代码保镖 |
| **交付形式** | 完整Python源码(421行) + 详细README文档 + GitHub Actions配置模板 + MIT开源 |
| **运行环境** | Python 3.6+，需DeepSeek API Key（注册免费送500万token） |
| **适合人群** | 学生毕设 / 初中级程序员 / 技术团队负责人 / 开源项目维护者 |
| **上架状态** | ✅ 可上架 |

> 📦 购买即获：源码 + 文档 + CI/CD模板 + 永久使用 + 持续更新

## 常见问题

**Q: 支持其他LLM API吗？**
A: 支持！通过 `--api-url` 参数指定任何OpenAI兼容的API端点即可。

**Q: 审查大项目会很慢吗？**
A: 串行调用API，每个文件约5-15秒。使用 `--max-files` 控制数量。

**Q: 会修改我的代码吗？**
A: 绝对不会！工具只读取和分析代码，生成报告，不修改任何文件。

## 许可证

MIT License
