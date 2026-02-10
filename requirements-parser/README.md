# 需求分析技能

## 简介

自动读取飞书需求文档，智能提取故事和需求明细，自动添加到多维表格的故事看板和任务看板。

## 功能特点

✅ **自动解析**：智能识别飞书文档中的故事和需求点
✅ **避免重复**：检查故事是否已存在，避免重复创建
✅ **批量创建**：一次性创建所有任务记录
✅ **自动关联**：任务自动关联到对应的故事
✅ **配置灵活**：通过环境变量配置看板信息

## 快速开始

### 1. 配置环境变量

```bash
cd C:\Users\jueshi\.claude\skills\requirements-parser
cp .env.example .env
```

编辑 `.env` 文件，填写以下必填项：

```env
# 故事看板链接（完整URL）
REQUIREMENTS_STORY_URL=https://syounggroup.feishu.cn/base/ZWDwbEspya3xQ9stBo6cqIW3n4e?table=tblCn5HjmcZEDfgX

# 任务看板链接（完整URL）
REQUIREMENTS_TASK_URL=https://syounggroup.feishu.cn/base/ZWDwbEspya3xQ9stBo6cqIW3n4e?table=tbl8nb16fng5DQdJ
```

### 2. 获取配置参数

直接从飞书多维表格复制完整链接即可：

**故事看板：**
1. 打开故事看板
2. 复制浏览器地址栏的完整 URL
3. 粘贴到 `REQUIREMENTS_STORY_URL`

**任务看板：**
1. 打开任务看板
2. 复制浏览器地址栏的完整 URL
3. 粘贴到 `REQUIREMENTS_TASK_URL`

示例：
```env
REQUIREMENTS_STORY_URL=https://syounggroup.feishu.cn/base/ZWDwbEspya3xQ9stBo6cqIW3n4e?table=tblCn5HjmcZEDfgX
REQUIREMENTS_TASK_URL=https://syounggroup.feishu.cn/base/ZWDwbEspya3xQ9stBo6cqIW3n4e?table=tbl8nb16fng5DQdJ
```

### 3. 使用技能

在对话中提供飞书文档链接，例如：

> 帮我分析这个需求文档：https://syounggroup.feishu.cn/docx/EYHCdZwfBoLWszxhdehcoyEcnzb

技能将自动：
1. 读取文档内容
2. 提取故事和需求
3. 更新故事看板
4. 创建任务记录
5. 汇报处理结果

## 支持的文档格式

### 表格形式（推荐）

| 序号 | 故事 | 日期 | 产品经理 |
|------|------|------|----------|
| 1 | 机器人链接提取优化 | 12.30 | 十锦 |
| 2 | 种草计提自动化优化 | 12.30 | 十锦 |

每个故事标题下包含详细的需求说明。

### 标题形式

使用二级标题（##）作为故事标题，下方为需求详情。

```markdown
## 机器人链接提取优化

需求背景：...
需求详情：...
```

## 可选配置

### 默认负责人

```env
# 默认产品负责人 User ID（从飞书用户信息中获取）
REQUIREMENTS_DEFAULT_PM_ID=ou_xxxxxxxxxxxxx

# 默认开发负责人 User ID
REQUIREMENTS_DEFAULT_DEV_ID=ou_xxxxxxxxxxxxx
```

**如何获取 User ID：**
查看故事看板中已有记录，产品负责人字段的值即为 User ID（格式：`ou_xxxxxxxxxxxxx`）

### 默认版本

```env
# 默认影响版本
REQUIREMENTS_DEFAULT_VERSION=v7.0.0
```

## 输出示例

```
✅ 需求文档解析完成

📄 文档：KOL V7.0.0版本需求

📊 处理结果：
	识别故事：6 个
	已存在故事：6 个（跳过创建）
	新创建任务：16 个

📋 任务清单：
1. 机器人链接提取优化
   ✅ 优化分发链接的系统识别与自动上传

2. 种草计提自动化优化
   ✅ 筛选计划-计划限制调整
   ✅ 计划数据调整-待执行超级验收支持传SAP
   ✅ 状态付款条件调整

3. 小红书聚光财务需求
   ✅ 小红书聚光-账户维护信息优化
   ✅ 小红书聚光-修改账户信息操作记录
   ✅ 小红书聚光-新增接口对接

...（后续省略）
```

## 字段映射

### 故事看板字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 故事名称 | Text | 主键，从文档提取 |
| 故事描述 | Text | 使用文档标题或版本 |
| 产品负责人 | User | 从文档的"产品经理"列提取 |
| 故事负责人 | User | 可配置默认值 |
| 开发完成时间 | DateTime | 可选，留空 |
| 状态 | SingleSelect | 默认"未开始" |
| 影响版本 | SingleSelect | 使用配置的默认版本 |
| 备注 | SingleSelect | 可选 |

### 任务看板字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 任务名称 | Text | 主键，格式：{故事}-{需求简述} |
| 开发备注 | Text | 需求点的详细说明 |
| 工时 | Number | 可选，留空待后续填写 |
| 关联故事 | SingleLink | 自动关联到对应故事 |
| 状态 | SingleSelect | 默认"未开始" |
| 开发人员 | User | 可选，留空待分配 |
| 影响版本 | Lookup | 自动从故事看板查找 |
| 联调备注 | Text | 可选 |

## 注意事项

1. **文档权限**：确保 OpenClaw 有访问目标文档和多维表格的权限
2. **名称匹配**：产品负责人的名称需要与飞书用户名称完全一致
3. **字段结构**：如果看板字段结构变化，可能需要更新技能
4. **关联关系**：任务通过 record_id 关联到故事，确保故事已存在
5. **重复检查**：技能会检查故事是否已存在，避免重复创建

## 故障排查

### 问题：无法读取文档

**可能原因：**
- 文档链接不正确
- 没有访问权限

**解决方法：**
- 检查文档链接是否完整
- 确认飞书插件已正确配置
- 确认有访问文档的权限

### 问题：无法创建记录

**可能原因：**
- 配置参数不正确
- 没有多维表格编辑权限
- 字段结构不匹配

**解决方法：**
- 检查 `.env` 文件中的配置是否正确
- 确认有编辑多维表格的权限
- 使用 `feishu_bitable_list_fields` 查看实际字段结构

### 问题：任务无法关联故事

**可能原因：**
- 故事不存在
- record_id 不正确

**解决方法：**
- 确保故事已创建
- 检查故事看板中的记录 ID

## 更新日志

### v1.0.0 (2026-02-10)

初始版本，支持：
- 读取飞书文档
- 提取故事和需求
- 创建故事和任务记录
- 自动关联任务到故事
- 避免重复创建故事

## 许可证

MIT
