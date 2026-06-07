# AI Code Reviewer - 智能代码审查助手

<p align="center">
  <a href="https://github.com/wynn2025/ai-code-reviewer/stargazers">
    <img src="https://img.shields.io/github/stars/wynn2025/ai-code-reviewer?style=social" alt="GitHub Stars">
  </a>
  <a href="https://github.com/wynn2025/ai-code-reviewer/watchers">
    <img src="https://img.shields.io/github/watchers/wynn2025/ai-code-reviewer?style=social" alt="GitHub Watchers">
  </a>
  <a href="https://github.com/wynn2025/ai-code-reviewer/forks">
    <img src="https://img.shields.io/github/forks/wynn2025/ai-code-reviewer?style=social" alt="GitHub Forks">
  </a>
  <a href="https://github.com/wynn2025/ai-code-reviewer/issues">
    <img src="https://img.shields.io/github/issues/wynn2025/ai-code-reviewer" alt="GitHub Issues">
  </a>
  <a href="https://github.com/wynn2025/ai-code-reviewer/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/wynn2025/ai-code-reviewer" alt="License">
  </a>
</p>

<p align="center">
  <strong>⭐ 如果这个项目对你有帮助，请给一个Star！你的支持是我持续更新的动力 ⭐</strong>
</p>

<p align="center">
  <a href="https://github.com/wynn2025/ai-code-reviewer"><strong>🚀 立即使用</strong></a> •
  <a href="https://github.com/wynn2025/ai-code-reviewer/issues"><strong>🐛 报告Bug</strong></a> •
  <a href="https://github.com/wynn2025/ai-code-reviewer/issues"><strong>💡 功能建议</strong></a> •
  <a href="#贡献指南"><strong>🤝 贡献代码</strong></a>
</p>

---

> 基于DeepSeek API的自动化代码审查工具，零依赖，单文件即可运行。支持30+编程语言，智能发现Bug、安全漏洞、性能问题，并提供修复建议。

---

## ✨ 功能特点

- **🔍 智能审查** - 调用DeepSeek大模型，自动发现Bug、安全漏洞、性能问题
- **📦 零依赖** - 纯Python标准库，无需pip install任何第三方包
- **🌍 多语言支持** - 支持30+编程语言（Python/JS/TS/Java/C++/Go/Rust等）
- **⚡ 多种模式** - 支持单文件、整个目录、Git Diff三种审查模式
- **🔄 CI/CD集成** - 内置GitHub Actions支持，自动输出到Step Summary
- **📊 结构化报告** - 按严重程度分类（🔴严重 🟡中等 🟢建议），给出评分和修复建议

---

## 🎯 适用场景

| 场景 | 说明 | 收益 |
|------|------|------|
| **个人项目** | 定期审查自己的代码，提前发现问题 | 提升代码质量，减少Bug |
| **团队协作** | Code Review前自动扫描，提高审查效率 | 节省50%+ Review时间 |
| **开源项目** | 自动检查PR，维护代码标准 | 提升项目可信度 |
| **学习提升** | 分析AI的审查建议，学习最佳实践 | 快速提升编程能力 |
| **企业CI/CD** | 集成到DevOps流程，自动把关代码质量 | 降低线上事故风险 |
| **学生作业** | 检查作业代码，发现常见错误 | 获得更好成绩 |

---

## 📸 效果展示

<!-- 
![审查报告示例](docs/screenshots/review-report.png)
![GitHub Actions集成](docs/screenshots/github-actions.png)
![命令行输出](docs/screenshots/cli-output.png)
-->

> 更多截图请查看 [docs/screenshots/](docs/screenshots/)

---

## 🚀 快速开始

### 方法1：直接下载使用

```bash
# 下载脚本
wget https://raw.githubusercontent.com/wynn2025/ai-code-reviewer/main/ai_code_reviewer.py

# 设置API Key
export DEEPSEEK_API_KEY="your-api-key"

# 运行审查
python ai_code_reviewer.py --file your_code.py
```

### 方法2：克隆仓库

```bash
git clone https://github.com/wynn2025/ai-code-reviewer.git
cd ai-code-reviewer
python ai_code_reviewer.py --file example.py
```

---

## 📖 详细使用指南

### 1. 设置API Key

```bash
export DEEPSEEK_API_KEY="***"
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

---

## 📋 命令行参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--file` | `-f` | 审查单个代码文件 | `--file main.py` |
| `--dir` | `-d` | 审查整个目录 | `--dir ./src` |
| `--diff` | | 审查Git diff文件 | `--diff changes.patch` |
| `--api-key` | | DeepSeek API Key | `--api-key sk-xxx` |
| `--model` | `-m` | 模型名称（默认: deepseek-chat） | `--model deepseek-coder` |
| `--api-url` | | 自定义API地址 | `--api-url https://api.xxx.com` |
| `--output` | `-o` | 保存报告到文件 | `--output report.md` |
| `--extensions` | `-e` | 指定文件扩展名 | `--extensions .py .js .ts` |
| `--max-files` | | 最大审查文件数（默认: 20） | `--max-files 50` |
| `--temperature` | | 生成温度 0-1（默认: 0.3） | `--temperature 0.5` |
| `--ci` | | CI/CD模式 | `--ci` |

---

## 🌐 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥（必需） | `sk-xxx` |
| `DEEPSEEK_API_URL` | 自定义API地址（可选） | `https://api.xxx.com` |
| `DEEPSEEK_MODEL` | 模型名称（可选） | `deepseek-coder` |

---

## 💡 使用示例

### 示例1：审查单个Python文件并保存报告

```bash
python ai_code_reviewer.py \
  --file my_app.py \
  --output review_report.md
```

**输出示例：**
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

---

## 📊 审查报告格式

| 级别 | 标记 | 说明 | 示例 |
|------|------|------|------|
| 严重 | 🔴 | Bug、安全漏洞、数据丢失风险 | SQL注入、XSS、未处理的异常 |
| 中等 | 🟡 | 性能问题、设计缺陷、可维护性 | N+1查询、重复代码、命名不当 |
| 建议 | 🟢 | 代码风格、命名规范、可读性 | 缺少注释、过长函数、格式问题 |

---

## 🌍 支持的语言

Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, HTML, CSS, SCSS, SQL, Shell, YAML, JSON, XML, TOML, Vue, Svelte 等30+种语言。

---

## ⚙️ 系统要求

- Python 3.6+
- DeepSeek API Key
- 网络连接（调用API）

---

## 🗺️ Roadmap

- [ ] 支持更多AI模型（GPT-4、Claude等）
- [ ] 添加VS Code插件
- [ ] 支持自动修复建议
- [ ] 添加代码复杂度分析
- [ ] 支持批量审查历史提交
- [ ] 添加团队协作功能

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

详细指南请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 💬 社区与支持

- **GitHub Issues**: [报告问题](https://github.com/wynn2025/ai-code-reviewer/issues)
- **讨论区**: [GitHub Discussions](https://github.com/wynn2025/ai-code-reviewer/discussions)
- **邮箱支持**: support@example.com

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

<div align="center">

## 💰 购买支持

如果这个项目对你有帮助，可以考虑：

- ⭐ **给个Star** - 这是对我最大的支持！
- 💰 **闲鱼购买** - 获取完整源码 + 详细文档 + 终身更新
- 🤝 **赞助项目** - 支持持续开发

**闲鱼购买链接**: [AI代码审查工具](https://goofish.com/item/xxx) ¥39（原价¥99，限时特惠）

---

**⭐ 如果觉得有用，请给一个Star！你的支持是我持续更新的动力 ⭐**

[![GitHub Stars](https://img.shields.io/github/stars/wynn2025/ai-code-reviewer?style=social)](https://github.com/wynn2025/ai-code-reviewer/stargazers)

</div>
