---
name: suoha
description: 完整研发工作流：需求分析 → 开发 → 代码评审 → 提交。触发词：梭哈、干活、开始开发、全流程开发
---

## 快速开始

**执行者划分：**
- OpenClaw（步骤 1-2）：项目定位、需求分析
- Claude Code（步骤 3-4）：代码开发、评审、提交

**关键警告**：
- ⚠️ **OpenClaw 严禁自行读取/修改代码，必须启动 Claude Code 执行开发任务**
- ⚠️ **严禁跳过步骤 2 的用户确认直接启动 Claude Code**
- ⚠️ **步骤 2 必须阻塞等待用户明确确认后才能进入步骤 3**

**执行顺序**（严格禁止打乱）：
1. 步骤 1：定位项目（调用 project-check）
2. 步骤 2：分析需求，输出功能清单
3. **【阻塞等待】用户确认功能清单**
4. 步骤 3：只有在用户确认后才启动 Claude Code
5. 步骤 4：自动执行评审与提交

---

## 工作流

```
步骤1: 项目定位 → 步骤2: 需求分析 → [用户确认] → 步骤3: 开发(由Claude Code执行) → 步骤4: 评审提交
(OpenClaw)      (OpenClaw)                           (Claude Code)                (Claude Code)
```

**【执行顺序强制要求】**：
1. 必须严格按顺序执行：步骤 1 → 步骤 2 → [等待确认] → 步骤 3 → 步骤 4
2. **步骤 2 和步骤 3 之间必须有明确的用户确认环节**
3. **禁止跳过步骤 2 的用户确认直接执行步骤 3**
4. **禁止将步骤 1-2 和步骤 3 合并执行**

---

### 步骤 1：项目定位

调用 `project-check` 技能匹配项目路径。未识别则使用 KOL 项目。

---

### 步骤 2：需求分析与计划

**职责**：分析需求 → 输出结构化功能清单 → **持久化状态并阻塞等待用户确认**

**【严厉禁止】**：
- ❌ **绝对禁止**跳过用户确认直接进入步骤 3
- ❌ **绝对禁止**在用户回复"确认"之前启动 Claude Code
- ❌ **绝对禁止**将步骤 2 和步骤 3 合并执行

**动作**：
1. 获取需求（文档链接 → 浏览器提取；直接描述 → 整理）
2. 结构化功能清单（补充隐含需求）
3. **输出确认信息并阻塞等待**：
```
项目位置：xxx
功能清单：
| 序号 | 功能点 |
|:----:|--------|
| 1 | xx |
| 2 | xx |

【注意】确认后将启动 Claude Code 执行后续开发流程
是否进入开发？[必须等待用户明确回复"确认"或"是"后才能进入步骤3]
```

5. **只有在收到用户明确确认后**（如"确认"、"是"、"好的"等），才能执行步骤 3
6. 如果用户提出疑问或修改意见，先处理问题，重新输出确认信息，再次阻塞等待

---

### 步骤 3：代码开发（Claude Code 执行）

**【前置条件】**：
- ✅ 用户已在步骤 2 明确确认功能清单
- ✅ 用户已回复"确认"、"是"或类似同意词语
- ❌ **如果用户未确认，绝对禁止执行本步骤**

**【启动 Claude Code】**（启动后立即传递上下文并确认）：

```bash
# 使用 process 工具启动
exec:command "claude" + background=true + pty=true + workdir="{项目路径}"

# 等待初始化完成
process:action poll + sessionId="{返回的sessionId}"

# 传递上下文
process:action send-keys + sessionId="{sessionId}" + literal="项目位置：{路径}
功能清单：{步骤2的清单}

当前步骤：3（需求澄清 → 技术方案 → 代码开发）
持续保持会话活跃，直到评审提交完成"

# 立即发送回车确认
process:action send-keys + sessionId="{sessionId}" + keys=["Return"]
```

**【向用户汇报启动状态】**：
```
✅ Claude Code 已启动
✅ 上下文已传递并确认

当前状态：步骤 3 - 代码开发进行中
```

**开发流程**：
- 需求澄清 → 技术方案 → 代码开发
- 技术方案需用户确认后开始编码
- 保持会话活跃直到步骤4完成

---

### 步骤 4：评审与提交（Claude Code 自动执行）

**自动流程**（无需用户手动触发）：
```
4.1 /code-review
  ├─ 通过 → 4.3 /commit-push → 结束
  └─ 不通过 → 4.2 /code-review-update → 重新 4.1 → 循环
```

**子步骤说明**：
- 4.1 代码评审：调用 `/code-review`，输出评审结果
- 4.2 修复问题：调用 `/code-review-update`，输出修复内容
- 4.3 提交代码：调用 `/commit-push`，输出 Git 结果

**【进度摘要】**（步骤 4 完成后）：
```
【进度】步骤 4 - 代码评审与提交
- 评审结果：通过（发现问题 N 个，已修复）
- 提交结果：已推送到远端
- Commit：abc123 - "功能：xxx"
```

---

## 关键交接点

1. **步骤 2 → 3**：
   - 用户确认后，OpenClaw 启动 Claude Code
   - 使用 process 工具传递完整上下文
   - 发送回车确认开始执行

2. **步骤 3.2 → 3.3**：用户确认技术方案后开始编码
3. **步骤 3 → 4**：代码开发完成后自动触发评审流程

---

## 用户回复"确认"时的处理流程

当收到用户回复"确认"、"是"、"好的"等时：

直接进入**步骤 3**，启动 Claude Code 并传递上下文（见上文步骤 3 说明）。

---

## Windows 环境启动 Claude Code

**关键问题**：Claude Code 是交互式 TUI 程序，需保持 stdin 开放

| 方式 | 结果 | 说明 |
|:---|:---:|:---|
| ❌ write + eof=true | 失败 | 过早关闭 stdin |
| ✅ send-keys + literal | 成功 | 保持 stdin 开放 |

**正确启动流程**（使用 process 工具）：
```
1. exec:command "claude" + background=true + pty=true
2. process:action poll（等待初始化）
3. process:action send-keys + literal="长文本上下文..."
4. process:action send-keys + keys=["Return"]
```

**常见问题**：
- PowerShell 不支持 `&&`：分步执行 cd 和 claude
- 必须用 `send-keys` 传输入，不能用 `write + eof`

---

## Windows 启动 Claude Code 重要说明

Claude Code 是交互式 TUI 程序，需保持 stdin 开放。

**关键问题**：PowerShell 不支持 `&&` 操作符

| 方式 | 结果 | 说明 |
|:---|:---|:---|
| ❌ `cd C:\code\athena-server && claude` | 失败 | PowerShell 不支持 `&&` |
| ❌ `write + eof=true` | 失败 | 过早关闭 stdin |
| ✅ `exec + workdir + background + pty` | 成功 | 正确启动方式 |

**正确启动流程**：
```bash
1. exec:command "claude" + workdir="{项目路径}" + background=true + pty=true
2. process:action poll（等待初始化）
3. process:action send-keys + literal="长文本上下文..."
4. process:action send-keys + keys=["Return"]
```

**更多详情**：参见 `docs/windows-guide.md`

---

## 完成后总结

```
🎉 梭哈流程全部完成！

【执行结果汇总】
- 功能清单：已完成 N 个功能点
- 修改文件：xxx.java, yyy.vue（共 N 个文件）
- Git 提交：abc123 - "功能：xxx"
- 推送结果：已推送到远端

完整工作流已结束！🚀
```
