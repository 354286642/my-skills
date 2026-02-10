# Windows 环境启动 Claude Code 指南

## 核心问题

Claude Code 是 **交互式 TUI 程序**，关键在于**保持 stdin 开放**并正确传递输入。

## 交互方式对比

| 方式 | 命令 | 结果 | 说明 |
|:---|:---|:---|:---|
| ❌ 错误 | `write + eof=true` | 失败 | 过早关闭 stdin，Claude Code 无法接收后续输入，无法进入交互模式 |
| ✅ 正确 | `send-keys + literal` | 成功 | 保持 stdin 开放，Claude Code 正常接收输入并进入交互模式 |

## PowerShell 命令分隔符问题

PowerShell 与传统 shell 不同，**不支持 `&&`**：

```powershell
# ❌ 错误：PowerShell 报错"&&"不是有效语句分隔符
cd C:\code\athena-server && claude

# ✅ 正确：分步执行
exec:command cd C:\code\athena-server
exec:command claude
```

## 正确启动流程（使用 process 工具）

### 1. 启动会话

```bash
exec:command "claude" + background=true + pty=true
```

### 2. 等待 Claude Code 初始化

```bash
process:action poll + sessionId="{sessionId}"
```

**注意**：首次启动可能需要登录授权，等待时间较长。

### 3. 传递上下文信息

**关键**：必须用 `send-keys + literal`，**不要用 write + eof**

```bash
process:action send-keys + sessionId="{sessionId}" + literal="长文本指令..."
```

### 4. 发送回车确认

```bash
process:action send-keys + sessionId="{sessionId}" + keys=["Return"]
```

## 自动确认机制（重要！）

### 为什么需要自动确认？

Claude Code 在执行过程中会弹出确认对话框：
- "Do you want to proceed?" - 询问是否执行读取操作
- "Allow reading from xxx?" - 询问是否允许读取项目文件
- 其他确认选项

**用户无法直接操作这些对话框**，必须由 OpenClaw 使用 `send-keys` 自动确认。

### 常见确认场景

#### 场景 1：读取文件确认

```
Do you want to proceed?
❯ 1. Yes
  2. Yes, allow reading from athena-server/ during this session
  3. No
```

**自动确认操作**：
```bash
# 优先选择选项 2（允许整个会话读取）
process:action send-keys + keys=["Down", "Down", "Return"]
# 或者直接发送数字 2
process:action send-keys + literal="2" + keys=["Return"]
```

#### 场景 2：执行操作确认

```
❯ 1. Yes
  2. No
```

**自动确认操作**：
```bash
# 选择 Yes
process:action send-keys + keys=["Return"]
# 或发送数字 1
process:action send-keys + literal="1" + keys=["Return"]
```

### 自动确认最佳实践

**原则**：选择最宽松的选项，减少后续确认次数

1. **读取文件确认**：选择 "Yes, allow reading from xxx during this session"（选项 2）
2. **执行操作确认**：选择 "Yes"（选项 1）
3. **修改文件确认**：选择 "Yes"（选项 1）

## 持续监控机制（重要！）

### 为什么需要持续监控？

Claude Code 是长时间运行的进程，可能出现：
- 卡在确认对话框等待用户输入
- 执行出错需要人工干预
- 完成子步骤需要汇报进度
- 超时无响应需要重启

**必须每 30-60 秒监控一次状态**，及时发现异常。

### 监控流程

```javascript
// 1. 启动 Claude Code
const sessionId = "clear-forest"
exec({ command: "claude", background: true, pty: true })

// 2. 传递上下文
process({ action: "send-keys", sessionId, literal: "..." })
process({ action: "send-keys", sessionId, keys: ["Return"] })

// 3. 持续监控循环（每 30 秒检查一次）
while (true) {
  // 等待 30 秒
  await new Promise(resolve => setTimeout(resolve, 30000))

  // 检查状态
  const result = await process({ action: "poll", sessionId })

  // 分析输出
  if (result.includes("Do you want to proceed?")) {
    // 检测到确认对话框 → 静默处理（不汇报）
    await process({
      action: "send-keys",
      sessionId,
      literal: "2",
      keys: ["Return"]
    })
    continue // 静默处理，不向用户汇报
  }

  if (result.includes("error") || result.includes("Error")) {
    // 检测到错误，向用户报告
    console.error("检测到错误:", extractError(result))
    break
  }

  // 检查是否完成
  if (result.includes("🎉") || result.includes("流程结束")) {
    console.log("流程已完成")
    break
  }
}
```

### 监控检查点

每 30 秒检查以下内容：

1. **确认对话框检测**
   - 查找 "Do you want to proceed?"
   - 查找 "Allow reading from"
   - 查找 "❯" (选项指示符)
   - **动作**：静默处理（自动发送确认，不向用户汇报）

2. **错误检测**
   - 查找 "error" / "Error" / "ERROR"
   - 查找 "failed" / "Failed" / "FAILED"
   - **动作**：向用户报告，询问是否继续

3. **完成检测**
   - 查找 "🎉" / "流程结束" / "已完成" / "评审提交完成"
   - **动作**：结束监控，汇报结果

**核心原则**：只在需要用户介入时（错误、完成）才发送消息，确认对话框自动静默处理，正常运行保持静默。

## 完整示例

```javascript
// 1. 启动 Claude Code
const result = await exec({
  command: "claude",
  background: true,
  pty: true
})

const sessionId = result.sessionId // 例如 "clear-forest"

// 2. 等待初始化
await process({ action: "poll", sessionId })

// 3. 传递上下文（长文本）
await process({
  action: "send-keys",
  sessionId,
  literal: `项目位置：C:\\code\\athena-server
功能清单：
1. 实现用户登录功能
2. 添加权限验证

当前步骤：3（需求澄清 → 技术方案 → 代码开发）
持续保持会话活跃，直到评审提交完成`
})

// 4. 发送回车
await process({
  action: "send-keys",
  sessionId,
  keys: ["Return"]
})

// 5. 静默持续监控（每 30 秒，只在关键节点汇报）
let monitorCount = 0
while (monitorCount < 100) { // 最多监控 50 分钟
  await new Promise(resolve => setTimeout(resolve, 30000))
  monitorCount++

  const output = await process({ action: "poll", sessionId })

  // 检测确认对话框 → 静默处理（不向用户汇报）
  if (output.includes("Do you want to proceed?")) {
    await process({
      action: "send-keys",
      sessionId,
      literal: "2",
      keys: ["Return"]
    })
    continue // 继续监控，不发送消息
    continue
  }

  // 检测错误 → 向用户汇报
  if (output.includes("error") || output.includes("Error")) {
    console.error("【错误检测】Claude Code 遇到错误")
    console.error(output)
    break
  }

  // 检测完成 → 向用户汇报
  if (output.includes("🎉") || output.includes("流程结束")) {
    console.log("【流程完成】梭哈流程已结束")
    break
  }

  // 正常运行中 → 保持静默，不汇报
}
```

## 关键点总结

- ✅ 用 `pty=true` 启动以支持 TUI
- ✅ 用 `send-keys + literal` 传长文本
- ❌ **不要用 write + eof**
- ✅ 用 `send-keys + keys` 发送特殊按键（如回车）
- ✅ **必须自动确认对话框**（用户无法操作）
- ✅ **必须持续监控状态**（每 30 秒）
- ✅ **监控保持静默**：只在错误/完成时汇报，正常运行不发送消息
- ✅ 选择最宽松的确认选项（减少后续确认次数）

## 常见问题排查

### 问题 1：Claude Code 启动后无响应

**原因**：stdin 被过早关闭

**解决**：检查是否使用了 `write + eof=true`，改用 `send-keys`

### 问题 2：PowerShell 报错"&&"不是有效语句分隔符

**原因**：PowerShell 不支持 `&&` 连接符

**解决**：分步执行，先 `cd` 再执行 `claude`

### 问题 3：首次启动需要登录

**现象**：Claude Code 显示授权链接

**解决**：
1. 浏览器打开链接完成授权
2. 等待 Claude Code 显示就绪
3. 再执行后续步骤

### 问题 4：Claude Code 卡在确认对话框

**原因**：未实现自动确认机制

**解决**：
1. 使用 `process poll` 获取输出
2. 检测确认对话框关键词
3. 使用 `send-keys` 发送确认

### 问题 5：监控中断导致不知道进度

**原因**：未实现持续监控循环

**解决**：
1. 使用 `setTimeout` 或 `Sleep` 实现定时轮询
2. 每 30 秒检查一次状态
3. 只在错误/完成时向用户汇报，正常运行保持静默
