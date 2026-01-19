# Claude Code Skills

自定义 Claude Code 技能集合，用于增强 AI 编程助手在软件开发工作流中的自动化能力。

## 目录结构

```
skills/
├── apifox-tests/          # Apifox 自动化测试执行技能
├── code-review/           # 代码审查分发入口技能
├── code-review-update/    # 代码审查后自动修复技能
├── commit-push/           # Git 自动提交与构建技能
└── enum-dict/             # 枚举字典 SQL 生成技能
```

## 技能说明

### 1. apifox-tests - Apifox 自动化测试

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

## 许可证

MIT
