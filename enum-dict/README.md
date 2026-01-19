# enum-dict

枚举字典 SQL 生成工具，将中文描述批量转换为字典键值对和可执行的 MySQL 插入脚本。

## 功能描述

将中文枚举描述转换为数据库字典表所需的格式，输出字典键值对和 MySQL INSERT 语句。

## 目录结构

```
enum-dict/
└── SKILL.md               # 技能配置文件
```

## 使用方法

### 基本用法

```
/enum-dict
```

进入交互模式，按提示输入信息。

### 输入方式

#### 方式一：文本输入

直接粘贴中文枚举描述，每行一个：

```
用户状态
启用
禁用
待审核
已锁定
```

#### 方式二：图片输入

粘贴包含枚举描述的图片，技能会自动识别其中的文字。

## 输出格式

### 字典键值对

```
USER_STATUS("用户状态"),
ENABLED("启用"),
DISABLED("禁用"),
PENDING("待审核"),
LOCKED("已锁定"),
```

**命名规则:**
- 全大写
- 使用下划线分隔单词
- 自动去重和排序

### MySQL 插入脚本

```sql
-- MySQL 8.0
INSERT INTO sys_dict (tenant_id, dict_key, dict_value, dict_type, description, create_time, update_time)
VALUES
  ('{tenant_id}', 'USER_STATUS', '用户状态', '{type}', '{description}', NOW(), NOW()),
  ('{tenant_id}', 'ENABLED', '启用', '{type}', '{description}', NOW(), NOW()),
  ('{tenant_id}', 'DISABLED', '禁用', '{type}', '{description}', NOW(), NOW()),
  ('{tenant_id}', 'PENDING', '待审核', '{type}', '{description}', NOW(), NOW()),
  ('{tenant_id}', 'LOCKED', '已锁定', '{type}', '{description}', NOW(), NOW())
ON DUPLICATE KEY UPDATE
  dict_value = VALUES(dict_value),
  description = VALUES(description),
  update_time = NOW();
```

## 必需参数

执行时需要用户提供以下参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| tenant_id | 租户 ID | `000000` |
| description | 字典描述 | `用户状态字典` |
| type | 字典类型 | `user_status` |

## 输出示例

### 输入

```
订单状态
待支付
已支付
已发货
已完成
已取消
```

### 参数

- tenant_id: `000000`
- description: `订单状态字典`
- type: `order_status`

### 输出 - 字典键值对

```
ORDER_STATUS("订单状态"),
UNPAID("待支付"),
PAID("已支付"),
SHIPPED("已发货"),
COMPLETED("已完成"),
CANCELLED("已取消"),
```

### 输出 - SQL

```sql
INSERT INTO sys_dict (tenant_id, dict_key, dict_value, dict_type, description, create_time, update_time)
VALUES
  ('000000', 'ORDER_STATUS', '订单状态', 'order_status', '订单状态字典', NOW(), NOW()),
  ('000000', 'UNPAID', '待支付', 'order_status', '订单状态字典', NOW(), NOW()),
  ('000000', 'PAID', '已支付', 'order_status', '订单状态字典', NOW(), NOW()),
  ('000000', 'SHIPPED', '已发货', 'order_status', '订单状态字典', NOW(), NOW()),
  ('000000', 'COMPLETED', '已完成', 'order_status', '订单状态字典', NOW(), NOW()),
  ('000000', 'CANCELLED', '已取消', 'order_status', '订单状态字典', NOW(), NOW())
ON DUPLICATE KEY UPDATE
  dict_value = VALUES(dict_value),
  description = VALUES(description),
  update_time = NOW();
```

## 特性

- **自动去重**: 相同的键值只保留一个
- **智能命名**: 根据中文含义生成英文键名
- **批量处理**: 一次可处理多个枚举项
- **多格式输出**: 同时生成键值对和 SQL
- **图片识别**: 支持从图片提取文字

## 注意事项

1. 生成的键名可能需要人工校对
2. 特殊字符（如括号、引号）会被自动处理
3. SQL 脚本兼容 MySQL 8.0+
4. 建议在执行 SQL 前先检查生成的语句
