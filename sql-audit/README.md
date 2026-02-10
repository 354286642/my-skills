# sql-audit

SQL工单自动审核技能，用于自动审核指定组别和状态的SQL工单。

## 功能描述

自动登录SQL审核系统，查找符合条件的工单（组别：【HERMES市场-HERMES_KOL】，状态：【等待审核人审核】），并依次点击审核通过。

## 目录结构

```
sql-audit/
├── SKILL.md               # 技能核心逻辑（AI执行流程）
├── .env.example           # 环境变量模板（配置示例）
└── README.md              # 本文件（使用指南）
```

## 快速开始

### 1. 环境配置

首次使用需要配置环境变量：

```bash
# 进入技能目录
cd C:\Users\jueshi\.claude\skills\sql-audit

# 复制配置模板
copy .env.example .env

# 编辑配置文件
notepad .env
```

### 2. 填写配置

在 `.env` 文件中填写以下必填项：

```bash
# SQL 审核系统地址
SQL_AUDIT_URL=https://sql.syounggroup.com/sqlworkflow/

# 登录凭据
SQL_AUDIT_USERNAME=your_username_here
SQL_AUDIT_PASSWORD=your_password_here
```

### 3. 执行审核

配置完成后，直接触发技能即可：

```
审下工单
```

或

```
/sql-audit
```

## 配置说明

### 必填项

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `SQL_AUDIT_URL` | SQL审核系统地址 | `https://sql.syounggroup.com/sqlworkflow/` |
| `SQL_AUDIT_USERNAME` | 登录用户名 | `jueshi` |
| `SQL_AUDIT_PASSWORD` | 登录密码 | `your_password` |

### 可选项（有默认值）

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `SQL_AUDIT_GROUP` | 目标组别 | `HERMES市场-HERMES_KOL` |
| `SQL_AUDIT_STATUS` | 目标状态 | `等待审核人审核` |
| `SQL_AUDIT_TIMEOUT` | 超时时间（秒） | `30` |
| `SQL_AUDIT_PAGE_LOAD_WAIT` | 页面加载等待（毫秒） | `3000` |
| `SQL_AUDIT_ACTION_DELAY` | 操作间隔（毫秒） | `1000` |

### 完整配置示例

```bash
# SQL 审核系统配置
SQL_AUDIT_URL=https://sql.syounggroup.com/sqlworkflow/

# 登录凭据（必填）
SQL_AUDIT_USERNAME=jueshi
SQL_AUDIT_PASSWORD=your_password_here

# 目标组别（可选，默认：HERMES市场-HERMES_KOL）
SQL_AUDIT_GROUP=HERMES市场-HERMES_KOL

# 目标状态（可选，默认：等待审核人审核）
SQL_AUDIT_STATUS=等待审核人审核

# 超时设置（可选，默认：30秒）
SQL_AUDIT_TIMEOUT=30

# 页面加载等待时间（可选，默认：3000毫秒）
SQL_AUDIT_PAGE_LOAD_WAIT=3000

# 操作间隔时间（可选，默认：1000毫秒）
SQL_AUDIT_ACTION_DELAY=1000
```

## 使用方法

### 基本用法

```
/sql-audit
```

执行后会自动：
1. 打开 SQL 审核系统
2. 使用配置的凭据自动登录
3. 查找符合条件的工单
4. 依次点击审核通过
5. 输出审核结果摘要

### 自定义参数（覆盖 .env 配置）

```
# 指定不同的组别
/sql-audit --group "其他组别"

# 指定不同的状态
/sql-audit --status "待审核"
```

## 工作流程

1. **加载配置**：从 `.env` 读取 URL、用户名、密码等
2. **打开页面**：访问 SQL 审核系统
3. **自动登录**：使用配置的凭据登录
4. **查找工单**：筛选指定组别和状态的工单
5. **批量审核**：
   - 如无符合条件的工单，提示并结束
   - 如有工单，依次进入详情并审核
6. **输出结果**：显示审核成功数量和工单列表

## 审核条件

| 条件 | 默认值 | 说明 |
|------|--------|------|
| 组别 | 【HERMES市场-HERMES_KOL】 | 可在 `.env` 中修改 |
| 状态 | 【等待审核人审核】 | 可在 `.env` 中修改 |

## 前置条件

- ✅ 已配置 `.env` 文件（包含登录凭据）
- ✅ 有访问SQL审核系统的权限
- ✅ 有审核目标组别工单的权限
- ✅ OpenClaw 浏览器服务已启动

### 启动浏览器服务

```bash
# 检查浏览器状态
openclaw browser --browser-profile openclaw status

# 如未启动，运行
openclaw browser --browser-profile openclaw start
```

## 安全说明

### 环境变量安全

⚠️ **重要提示：**
- `.env` 文件包含敏感信息（密码），**不要提交到 Git**
- `.gitignore` 已配置自动忽略 `.env` 文件
- 只提交 `.env.example` 模板文件
- 定期更换密码，确保账号安全

### 审核安全

- 审核操作会记录在系统中
- 建议定期检查自动审核的工单是否正确
- 对于重要的SQL工单，建议人工复核

## 技术实现

- **浏览器自动化**：使用 OpenClaw 浏览器控制
- **智能定位**：通过文本匹配和DOM结构定位元素
- **容错处理**：处理页面加载延迟、元素定位失败等情况
- **日志记录**：记录每个工单的审核状态

## 故障排查

### 问题1：提示"请先配置 .env 文件"

**解决方法：**
```bash
cd C:\Users\jueshi\.claude\skills\sql-audit
copy .env.example .env
notepad .env
```
填写必填项（URL、用户名、密码）。

### 问题2：登录失败

**可能原因：**
- 用户名或密码错误
- 网络连接问题
- SQL审核系统维护中

**解决方法：**
- 检查 `.env` 中的凭据是否正确
- 手动访问 SQL 审核系统确认可用
- 联系系统管理员

### 问题3：找不到工单列表

**可能原因：**
- 页面结构发生变化
- 权限不足

**解决方法：**
- 手动访问 SQL 审核系统确认页面正常
- 检查是否有审核目标组别的权限
- 如页面结构变化，需要更新技能配置

### 问题4：浏览器未启动

**解决方法：**
```bash
# 启动 OpenClaw Gateway
openclaw gateway restart

# 启动浏览器
openclaw browser --browser-profile openclaw start
```

## 注意事项

1. 本技能仅审核指定组别的工单，不会影响其他组的工单
2. 仅审核"等待审核人审核"状态的工单
3. 建议在非高峰期使用，避免对系统造成压力
4. 审核操作会有系统日志，确保可追溯
5. 如遇页面结构变化导致无法定位元素，需要更新技能配置

## 许可证

MIT
