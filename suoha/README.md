# 梭哈技能 - 完整研发工作流

## 简介

"梭哈"技能是一个完整的端到端研发工作流自动化工具，覆盖从需求分析到代码提交的全流程。通过协调 OpenClaw 和 Claude Code 两个 AI 助手，实现高效的项目开发。

**核心理念：** 一键触发，全流程自动化

## 功能特点

✅ **智能项目定位** - 自动识别项目路径
✅ **需求分析** - 结构化输出功能清单
✅ **协调执行** - OpenClaw + Claude Code 协同工作
✅ **代码评审** - 自动进行代码质量检查
✅ **自动提交** - 智能生成版本号和提交信息
✅ **用户确认** - 关键节点阻塞等待用户确认

## 工作流程

```
步骤1: 项目定位 → 步骤2: 需求分析 → [用户确认] → 步骤3: 代码开发 → 步骤4: 评审提交
(OpenClaw)      (OpenClaw)                           (Claude Code)    (Claude Code)
```

### 执行者划分

**OpenClaw（步骤 1-2）**
- 项目路径定位
- 需求文档分析
- 功能清单输出
- 启动 Claude Code

**Claude Code（步骤 3-4）**
- 技术方案设计
- 代码实现
- 代码评审
- Git 提交推送

### 关键节点

#### 🔒 步骤 2 → 步骤 3：必须等待用户确认

**流程：**
1. OpenClaw 输出功能清单
2. **阻塞等待用户明确确认**
3. 收到"确认"/"是"/"好的"后才启动 Claude Code
4. 传递完整上下文到 Claude Code

**确认信息示例：**
```
项目位置：C:\code\athena-server
功能清单：
| 序号 | 功能点 |
|:----:|--------|
| 1 | 用户登录功能 |
| 2 | 数据导出功能 |

【注意】确认后将启动 Claude Code 执行后续开发流程
是否进入开发？[必须等待用户明确回复"确认"或"是"]
```

#### 🔄 步骤 4：自动评审与提交循环

```
4.1 代码评审 → 通过？
    ├─ 是 → 4.3 提交代码 → 结束
    └─ 否 → 4.2 修复问题 → 重新 4.1
```

## 触发词

以下任一触发词都会启动梭哈流程：

- `梭哈`
- `干活`
- `开始开发`
- `全流程开发`

## 使用示例

### 场景 1：基于需求文档开发

```
用户: 梭哈 https://syounggroup.feishu.cn/docx/xxxx

OpenClaw:
1. 读取飞书文档
2. 分析需求
3. 输出功能清单
4. 等待确认...

用户: 确认

OpenClaw:
5. 启动 Claude Code
6. 传递上下文
7. 汇报状态

Claude Code:
8. 需求澄清
9. 技术方案设计
10. 代码实现
11. 自动评审
12. 提交推送
```

### 场景 2：口头描述开发

```
用户: 开始开发，我要加个用户登录功能

OpenClaw:
1. 识别项目（默认 KOL）
2. 整理需求描述
3. 输出功能清单
4. 等待确认...

用户: 好的，开始

（后续流程同上）
```

## 依赖技能

梭哈技能协调以下子技能：

1. **project-check** - 项目路径匹配
2. **code-review** - 代码审查
3. **code-review-update** - 代码修复
4. **commit-push** - Git 提交

## 配置要求

### 必需配置

1. **Claude Code 已安装**
   ```bash
   # 验证安装
   claude --version
   ```

2. **项目路径配置**（如果使用自定义项目）
   - 配置文件：`project-check/.env`
   - 格式：`PROJECT_XXX=项目路径`

### 可选配置

- **Git 用户信息**：用于自动提交
- **Jenkins 配置**：用于触发构建
- **SonarQube 配置**：用于代码分析

## Windows 环境注意事项

### 问题 1：PowerShell 不支持 `&&`

**错误方式：**
```bash
cd C:\code\project && claude  # ❌ 失败
```

**正确方式：**
```bash
# 使用 exec 工具的 workdir 参数
exec:command "claude" + workdir="C:\code\project" + background=true + pty=true
```

### 问题 2：保持 stdin 开放

Claude Code 是交互式 TUI 程序，需要保持 stdin 开放。

**错误方式：**
```javascript
write + eof=true  // ❌ 过早关闭 stdin
```

**正确方式：**
```javascript
process:action send-keys + literal="长文本上下文..."  // ✅ 保持开放
process:action send-keys + keys=["Return"]
```

## 输出格式

### 步骤 2：功能清单

```
📍 项目定位
路径：C:\code\athena-server
项目：KOL 业务系统

📋 需求分析
功能清单：
| 序号 | 功能点 | 优先级 |
|:----:|--------|:------:|
| 1 | 用户登录功能 | P0 |
| 2 | 数据导出 | P1 |
| 3 | 权限管理 | P1 |

⚠️ 确认后将启动 Claude Code 执行开发
是否进入开发？[请回复"确认"或"是"]
```

### 步骤 3：开发进行中

```
✅ Claude Code 已启动
✅ 上下文已传递

🔄 当前状态：步骤 3 - 代码开发
- 需求澄清：✅ 完成
- 技术方案：⏳ 进行中
- 代码实现：⏸️ 待开始
```

### 步骤 4：完成总结

```
🎉 梭哈流程全部完成！

【执行结果汇总】
✓ 功能清单：已完成 3 个功能点
✓ 修改文件：LoginController.java, ExportService.java（共 5 个文件）
✓ Git 提交：abc123 - "feat: 用户登录和数据导出功能"
✓ 推送结果：已推送到远端 main 分支

完整工作流已结束！🚀
```

## 常见问题

### Q1: 如何中断梭哈流程？

**A:** 在步骤 2 确认环节回复"取消"或"不"，流程将终止，不会启动 Claude Code。

### Q2: 步骤 3 开发过程中如何调整需求？

**A:** 直接在 Claude Code 对话中说明调整内容，Claude Code 会处理并更新方案。

### Q3: 代码评审不通过怎么办？

**A:** Claude Code 会自动调用 `code-review-update` 修复问题，然后重新评审，直到通过为止。

### Q4: 如何跳过某些步骤？

**A:** 梭哈是全流程自动化技能，不支持跳过步骤。如需单独执行某个步骤，请直接调用对应技能：
- `/code-review` - 单独代码评审
- `/commit-push` - 单独提交推送

### Q5: Windows 上 Claude Code 启动失败？

**A:** 检查：
1. Claude Code 是否已安装：`claude --version`
2. 是否使用 `pty=true` 参数
3. 是否使用 `send-keys` 传递输入而非 `write + eof`

## 技术细节

### 进程管理

使用 `process` 工具管理 Claude Code 后台进程：

```javascript
// 启动
exec:command "claude" + background=true + pty=true + workdir="{path}"

// 等待初始化
process:action poll + sessionId="{id}"

// 传递上下文
process:action send-keys + sessionId="{id}" + literal="{context}"

// 确认执行
process:action send-keys + sessionId="{id}" + keys=["Return"]
```

### 上下文传递

传递给 Claude Code 的上下文包含：

```
项目位置：{路径}
功能清单：
1. 功能点 1
2. 功能点 2
...

当前步骤：3（需求澄清 → 技术方案 → 代码开发）
持续保持会话活跃，直到评审提交完成
```

### 状态监控

使用 `monitor-agent.md` 中的监控逻辑追踪 Claude Code 状态：
- 会话活跃度
- 步骤进度
- 错误检测

## 相关文档

- **Windows 指南**：`docs/windows-guide.md`
- **监控代理**：`monitor-agent.md`
- **技能定义**：`SKILL.md`

## 更新日志

### v1.0.0 (2026-02-06)

初始版本，支持：
- OpenClaw + Claude Code 协同工作流
- 自动需求分析和代码开发
- 自动代码评审和提交
- Windows 环境支持

## 许可证

MIT
