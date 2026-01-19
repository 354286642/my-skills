# commit-push

Git 自动提交与 Jenkins 构建技能，自动化代码提交和构建流程。

## 功能描述

自动执行 Git 提交流程，包括生成版本号、创建提交信息、推送到远程仓库，并可触发 Jenkins 构建。

## 目录结构

```
commit-push/
├── scripts/
│   ├── .env               # Jenkins 配置
│   ├── .env.example       # 配置模板
│   └── jenkins_build.py   # Jenkins 触发脚本
└── SKILL.md               # 技能配置文件
```

## 使用方法

### 基本用法（需确认）

```
/commit-push
```

显示预览信息，用户确认后执行提交和推送。

### 自动执行

```
/commit-push y             # 自动提交并推送
```

跳过确认，直接执行提交和推送。

### 仅预览

```
/commit-push n             # 仅预览，不执行
```

显示将要执行的提交信息，但不实际提交。

### 触发 Jenkins 构建

```
/commit-push b             # 提交后触发 Jenkins 构建
```

执行完整的提交流程，并在推送后触发 Jenkins 构建。

## 版本号管理

### 版本号格式

```
V<major>.<minor>.<patch> <description>
```

例如：`V1.0.1 修复用户登录问题`

### 版本号规则

- **major**: 主版本号，重大功能变更
- **minor**: 次版本号，新功能添加
- **patch**: 补丁版本号，bug 修复

版本号会根据 git 历史自动递增。

## 提交信息生成

技能会分析当前的代码改动，自动生成包含以下内容的提交信息：

- 版本号
- 改动类型（feat/fix/docs/refactor等）
- 改动描述
- 相关文件列表

### 编码处理

中文提交信息会自动转换为 UTF-8 编码，确保在各种环境下正确显示。

## Jenkins 集成

### 配置

复制 `scripts/.env.example` 为 `.env` 并配置：

```env
JENKINS_URL=http://your-jenkins-server
JENKINS_USER=your-username
JENKINS_TOKEN=your-api-token
JENKINS_JOB=your-job-name
```

### 构建触发

使用 `/commit-push b` 时会：

1. 执行 git 提交和推送
2. 等待远程仓库更新
3. 调用 Jenkins API 触发构建
4. 返回构建 URL

### Jenkins 脚本

`jenkins_build.py` 支持：

- 触发指定 Job 构建
- 传递构建参数
- 获取构建状态
- 查询构建日志

## SonarQube 支持

提交信息中会包含 SonarQube 分析标记：

```
[ci] [sonarqube]
```

确保 Jenkins Job 配置了 SonarQube 分析步骤。

## 工作流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ 检测改动    │ ──▶ │ 生成版本号  │ ──▶ │ 创建提交    │
└─────────────┘     └─────────────┘     └─────────────┘
                                                │
                                                ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Jenkins 构建 │ ◀─▶ │ 推送代码    │ ◀───│ 用户确认    │
└─────────────┘     └─────────────┘     └─────────────┘
```

## 依赖项

- Git
- Python 3
- python-jenkins (可选，用于 Jenkins 集成)

## 注意事项

1. 执行前请确保已配置 git 用户信息
2. 确保有远程仓库的推送权限
3. Jenkins 集成需要有效的 API token
4. 建议在执行前先 stash 或提交未暂存的改动
