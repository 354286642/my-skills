---
name: enum-dict
description: 枚举与字典SQL生成工具，将中文描述批量转换为字典键值对和可执行的MySQL插入脚本。
trigger: 当用户需要将中文枚举选项转换为字典键值对和SQL插入脚本时触发。支持文本输入和图片粘贴。
---

### 目标
将用户输入的中文描述（文本或图片），自动转换为「字典键值对」+「可执行的MySQL 8.0插入脚本」，需严格遵循预设规则。

### 交互输入参数
在开始处理前，必须通过 `AskUserQuestion` 工具询问用户以下三个参数：

1. **tenant_id**（租户ID）：例如 `athena-service`
2. **description**（字典描述）：例如 `达人黑名单对应种草相关的类型`
3. **type**（字典类型）：例如 `athena_work_black_remark`

### 输入方式支持
- 文本输入：用户直接输入中文描述，每行一个选项
- 图片粘贴：用户粘贴包含中文选项的截图

### 字典键值对生成规则
1. **格式要求**：输出为 `字典值(中文名称)` 的格式，示例：`DELAYED_DRAFT_OVER_A_MONTH("脱稿一个月以上"),`
   - 末尾需加英文逗号
   - 中文名称用英文双引号包裹

2. **字典值（Key）生成**：
   - 步骤1：将中文描述翻译成**精简、语义完全匹配的英文**（优先用常用词汇，避免冗余，禁止意译）
   - 步骤2：将英文转换为「全大写+下划线分隔」的格式（单词间用下划线连接，无空格/特殊字符）

3. **中文名称**：完全保留原中文描述，不得修改

### SQL脚本生成规则（MySQL 8.0）

1. **多条SQL合并**：使用一条 `INSERT INTO ... VALUES` 语句，通过逗号分隔多个值，不要拆分为多条SQL

2. **字段取值规则**：
   | 字段名         | 取值规则                                                                 |
   |----------------|--------------------------------------------------------------------------|
   | id             | 基于当前时间戳生成id（总长度18位数字字符串，示例：`'202509201030450001'`）  |
   | value          | 字典值（大写下划线英文，与字典键值对中的Key完全一致）                     |
   | label          | 中文名称（原中文，与字典键值对中的中文完全一致）                         |
   | type           | 用户输入的字典类型                                                        |
   | description    | 用户输入的字典描述                                                        |
   | sort           | 按输入行顺序递增（第一行`1`，第二行`2`，…）                              |
   | parent_id      | `'0'`                                                                    |
   | create_by      | 空字符串 `''`                                                            |
   | create_date    | 当前系统时间（格式：`'YYYY-MM-DD HH:MM:SS'`）                            |
   | update_by      | 空字符串 `''`                                                            |
   | update_date    | 与 `create_date` 完全一致                                                |
   | remarks        | 空字符串 `''`                                                            |
   | del_flag       | `'0'`                                                                    |
   | tenant_id      | 用户输入的租户id                                                          |

3. **SQL语句格式**：使用标准SQL语法，字段顺序与示例一致，字符串值用单引号包裹

### 输出格式要求
分模块用标题清晰区分输出：

```markdown
### 字典键值对列表
`KEY1("选项1"),`
`KEY2("选项2"),`

### SQL脚本列表
```sql
INSERT INTO common.dict (id, value, label, `type`, description, sort, parent_id, create_by, create_date, update_by, update_date, remarks, del_flag, tenant_id)
VALUES
('202509201030450001', 'KEY1', '选项1', '{用户输入的type}', '{用户输入的description}', 1, '0', '', '2024-05-21 10:35:12', '', '2024-05-21 10:35:12', '', '0', '{用户输入的tenant_id}'),
('202509201030450002', 'KEY2', '选项2', '{用户输入的type}', '{用户输入的description}', 2, '0', '', '2024-05-21 10:35:12', '', '2024-05-21 10:35:12', '', '0', '{用户输入的tenant_id}');
```
```

### 执行流程

1. **询问用户参数**：使用 `AskUserQuestion` 询问 tenant_id、description、type

2. **获取输入内容**：
   - 如果用户输入文本，直接使用
   - 如果用户粘贴图片

3. **生成输出**：
   - 根据规则生成字典键值对列表
   - 根据规则生成SQL脚本列表
   - 按照输出格式要求展示结果

### 示例

**输入**（文本）：
```
脱稿一个月以上
未提交审核
已通过验收
```

**用户输入参数**：
- tenant_id: `athena-service`
- description: `达人黑名单对应种草相关的类型`
- type: `athena_work_black_remark`

**输出**：

### 字典键值对列表
`DELAYED_DRAFT_OVER_A_MONTH("脱稿一个月以上"),`
`NOT_SUBMITTED_FOR_REVIEW("未提交审核"),`
`PASSED_ACCEPTANCE("已通过验收"),`

### SQL脚本列表
```sql
INSERT INTO common.dict (id, value, label, `type`, description, sort, parent_id, create_by, create_date, update_by, update_date, remarks, del_flag, tenant_id)
VALUES
('202509201030450001', 'DELAYED_DRAFT_OVER_A_MONTH', '脱稿一个月以上', 'athena_work_black_remark', '达人黑名单对应种草相关的类型', 1, '0', '', '2024-05-21 10:35:12', '', '2024-05-21 10:35:12', '', '0', 'athena-service'),
('202509201030450002', 'NOT_SUBMITTED_FOR_REVIEW', '未提交审核', 'athena_work_black_remark', '达人黑名单对应种草相关的类型', 2, '0', '', '2024-05-21 10:35:12', '', '2024-05-21 10:35:12', '', '0', 'athena-service'),
('202509201030450003', 'PASSED_ACCEPTANCE', '已通过验收', 'athena_work_black_remark', '达人黑名单对应种草相关的类型', 3, '0', '', '2024-05-21 10:35:12', '', '2024-05-21 10:35:12', '', '0', 'athena-service');
```
