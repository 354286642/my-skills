# Claude Code Skills

自定义 Claude Code 技能集合，用于增强 AI 编程助手在软件开发工作流中的自动化能力。

## 目录结构

```
skills/
├── suoha/                # 完整研发工作流自动化技能
├── code-review/           # 代码审查分发入口技能
├── code-review-update/    # 代码审查后自动修复技能
├── commit-push/           # Git 自动提交与构建技能
├── enum-dict/             # 枚举字典 SQL 生成技能
├── project-check/         # 项目路径匹配技能
├── requirements-parser/   # 飞书需求文档自动解析技能
├── sql-audit/            # SQL 工单自动审核技能
└── apifox-tests/          # Apifox 自动化测试执行技能
```

## 技能说明

### 1. suoha - 完整研发工作流自动化

端到端研发工作流自动化，覆盖需求分析、代码开发、评审、提交全流程。

**触发词:** 梭哈、干活、开始开发、全流程开发

**工作流:**
```
步骤1: 项目定位 → 步骤2: 需求分析 → [用户确认] → 步骤3: 代码开发 → 步骤4: 评审提交
(OpenClaw)      (OpenClaw)                           (Claude Code)    (Claude Code)
```

**功能:**
- 协调 OpenClaw 和 Claude Code
- 智能需求分析和功能清单输出
- 自动代码评审和修复
- 自动 Git 提交和推送

**用法示例:**
```
梭哈                       # 启动全流程开发
开始开发 https://syounggroup.feishu.cn/docx/xxxx
```

---

### 2. code-review - 代码审查分发器

根据参数路由到不同的代码审查模式。

**支持模式:**
- `main` (默认): Java 标准代码审查，关注功能正确性、安全性、最佳实践
- `kol`: KOL 专家视角审查，关注架构设计、可维护性、性能

**用法示例:**
```
/code-review               # 默认模式审查待提交代码
/code-review kol           # KOL 专家模式
/code-review abc123        # 审查指定提交
```

---

### 3. code-review-update - 代码自动修复

根据 code-review 的审查建议自动修复代码问题。

**修复策略:**
- P0: 必须修复 (安全漏洞、严重 bug)
- P1: 应该修复 (性能问题、逻辑错误)
- P2: 建议修复 (代码规范、可读性)

**用法示例:**
```
/code-review-update        # 根据审查结果自动修复
```

---

### 4. commit-push - Git 自动提交与构建

自动化 Git 提交流程，支持版本号管理和 Jenkins 构建。

**命令参数:**
- `/commit-push` - 标准流程，需要确认
- `/commit-push y` - 自动执行提交推送
- `/commit-push n` - 仅预览备注
- `/commit-push b` - 触发 Jenkins 构建

**特性:**
- 自动生成版本号 (格式: V1.0.1 描述)
- 中文自动转 UTF-8 编码
- 支持 SonarQube 分析

---

### 5. enum-dict - 枚举字典 SQL 生成

将中文枚举描述转换为字典键值对和 MySQL 插入脚本。

**输入方式:** 文本输入或图片粘贴

**输出格式:**
- 字典键值对: `KEY("中文名称"),`
- SQL 插入脚本 (MySQL 8.0)

**用法示例:**
```
/enum-dict                 # 交互式输入枚举描述
```

---

### 6. project-check - 项目路径匹配

匹配项目名称到实际项目路径，支持多别名和多位置匹配。

**功能:**
- 支持项目别名配置
- 多路径自动搜索
- 默认项目回退

**用法示例:**
```
project-check KOL          # 返回 KOL 项目路径
project-check athena       # 返回 athena 项目路径
```

---

### 7. requirements-parser - 飞书需求文档解析

自动读取飞书需求文档，提取故事和需求明细，添加到多维表格的故事看板和任务看板。

**功能:**
- 智能识别故事和需求点
- 避免重复创建故事
- 批量创建任务记录
- 自动关联任务到故事

**用法示例:**
```
requirements-parser https://syounggroup.feishu.cn/docx/xxxx
```

---

### 8. sql-audit - SQL 工单自动审核

自动登录 SQL 审核系统，查找指定组别和状态的工单，并自动点击审核通过。

**功能:**
- 自动登录 SQL 审核系统
- 批量审核工单
- 支持组别和状态筛选

**用法示例:**
```
sql-audit                  # 审核默认组别的工单
```

---

### 9. apifox-tests - Apifox 自动化测试

执行 Apifox API 自动化测试并解读结果。

**触发场景:**
- 代码修改后验证接口可用性
- git commit/push 前的接口检查
- 发布版本前的回归测试
- 合并到 main 分支前的自动化检查

**支持环境:** dev, test, prod

**用法示例:**
```
/apifox-tests              # 选择测试场景执行
/apifox-tests dev          # 在开发环境执行
```

## 技术栈

- **脚本语言:** Node.js (JavaScript), Python 3
- **依赖:** dotenv, jenkins-api
- **Git 集成:** 是 (代码审查、提交推送)
- **CI/CD:** Jenkins (构建触发)

## 项目特点

1. **模块化设计** - 每个技能独立目录，职责清晰
2. **配置化** - 支持 `.env` 文件管理环境变量
3. **可扩展** - 易于添加新的技能模块
4. **工作流集成** - 涵盖开发、测试、审查、提交、构建全流程
5. **多平台支持** - 飞书、SQL审核、Jenkins等第三方集成
6. **AI 协同** - OpenClaw 与 Claude Code 协同工作

## 技能分类

### 代码质量
- `code-review` - 代码审查
- `code-review-update` - 代码修复

### 开发流程
- `suoha` - 完整研发工作流
- `commit-push` - Git 自动提交

### 测试与验证
- `apifox-tests` - API 自动化测试
- `sql-audit` - SQL 工单审核

### 需求与配置
- `requirements-parser` - 需求文档解析
- `project-check` - 项目路径匹配
- `enum-dict` - 枚举字典生成

## 快速开始

### 安装依赖

```bash
# 进入技能目录
cd C:\Users\jueshi\.claude\skills

# 安装通用依赖（如果需要）
npm install dotenv
```

### 配置技能

各技能的配置文件位于对应目录下的 `.env` 文件：

```bash
# 示例：配置 SQL 审核
cd sql-audit
cp .env.example .env
# 编辑 .env 填写配置

# 示例：配置需求解析
cd requirements-parser
cp .env.example .env
# 编辑 .env 填写飞书看板链接
```

### 使用技能

在支持的 AI 助手（OpenClaw / Claude Code）中输入触发词或命令：

```
/code-review              # 代码审查
梭哈                       # 全流程开发
/apifox-tests             # 执行 API 测试
```

## 开发指南

### 创建新技能

1. 在 `skills/` 目录下创建新文件夹
2. 创建 `SKILL.md` 文件定义技能逻辑
3. 创建 `README.md` 文档说明使用方法
4. （可选）创建 `.env.example` 配置模板
5. 更新本 `README.md` 添加技能说明

### 技能模板

```markdown
---
name: your-skill
description: "技能描述"
---

# 技能名称

## 技能目标

描述技能要完成的任务...

## 工作流程

### 步骤 1: xxx
...

### 步骤 2: xxx
...

## 使用示例

...

## 配置说明

...
```

## 许可证

MIT

## 更新日志

### 2026-02-10

- ✅ 为 `suoha` 技能添加详细的 README.md 文档
- ✅ 更新总 README，新增 4 个技能说明（project-check, requirements-parser, sql-audit, suoha）
- ✅ 重组技能分类，新增"技能分类"章节
- ✅ 添加"快速开始"和"开发指南"章节
- ✅ 完善目录结构，反映当前实际技能列表

### 2025-02-06

- ✅ 初始版本，包含 5 个核心技能（apifox-tests, code-review, code-review-update, commit-push, enum-dict）
