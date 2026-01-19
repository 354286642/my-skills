---
name: commit-push
description: 自动化 Git 提交流程，包含版本号管理、提交信息确认和编码处理。支持触发 Jenkins 构建。
trigger: 当用户要求提交代码、推送更改或生成提交备注时触发。支持命令行参数：`/commit-push y` 可自动执行提交和推送，`/commit-push b` 可触发 Jenkins 构建。
---

### 目标
根据本地待提交的代码，自动生成符合规范的提交备注，询问用户确认，并完成代码提交与推送。支持触发 Jenkins 构建。

### 命令参数
- `/commit-push` - 标准流程，生成备注后需要用户确认
- `/commit-push y` - 自动执行，生成备注后直接提交并推送，无需确认
- `/commit-push n` - 仅生成备注预览，不执行提交
- `/commit-push b` - 触发 Jenkins 构建（可选参数：`-u 用户名`, `-s 启用SonarQube`）

### 提交备注规范
1.  格式：`V1.0.1 xxxx` (版本号 + 描述)。
2.  版本号逻辑：
	- 默认获取 Git 最近一次提交的版本号。
	- 仅检索最近的 10 条提交记录作为参考。
	- 如版本号末尾存在_fix等字符，去除掉，仅保留纯版本号。
3.  编码处理：
	- 若提交信息包含中文，必须将中文内容自动转换为 UTF-8 十六进制编码。
	- 执行命令格式：`git commit -m $'...'`。

###  工作流程
#### 第一步：解析命令参数
首先检查用户输入的命令参数：
- 检测命令中是否包含 `y` 或 `Y` 参数（如 `/commit-push y`）
- 检测命令中是否包含 `n` 或 `N` 参数（如 `/commit-push n`）
- 检测命令中是否包含 `b` 或 `B` 参数（如 `/commit-push b`）
- 记录参数模式到变量 `auto_mode`：`auto_submit` | `preview_only` | `build_mode` | `standard`

#### 第二步：生成备注
	- 分析待提交的代码变更。
	- 生成符合上述规范的默认提交信息。

#### 第三步：根据参数执行
**如果 `auto_mode = auto_submit`（命令含 y 参数）：**
- 显示：当前提交备注为：{生成的备注}
- 显示：检测到自动提交参数，直接执行提交与推送...
- 跳过确认，直接执行提交与推送

**如果 `auto_mode = preview_only`（命令含 n 参数）：**
- 显示：当前提交备注为：{生成的备注}
- 显示：预览模式，不执行提交
- 结束流程
	
**如果 `auto_mode = build_mode`（命令含 b 参数）：**
- 流程：自动提交 + 推送 + 触发 Jenkins 构建
- 先执行提交与推送（同 auto_submit 流程）
- 推送成功后，再执行 Jenkins 构建：
  - 执行命令：`python scripts/jenkins_build.py [-u 用户名] [-s]`
    - 说明：使用相对于 skill 根目录的路径，Claude Code 会自动解析为正确的绝对路径
  - 默认使用 `scripts/.env` 文件中的配置：
    - `JENKINS_URL`：Jenkins 服务器地址
    - `JENKINS_USERNAME`：用户名
    - `JENKINS_API_TOKEN`：API Token（在 Jenkins 用户设置中生成）
    - `JENKINS_COMM_JOB_NAME`：Job 名称
    - `JENKINS_BUILD_BRANCH`、`JENKINS_BUILD_ENV`：构建参数
  - 可通过 `-u` 参数覆盖 .env 中的用户名
  - 可通过 `-s` 参数启用 SonarQube 分析
- 如果推送失败，不执行构建，提示用户

**如果 `auto_mode = standard`（无参数）：**
执行交互确认流程：
- 显示：当前提交备注为：{生成的备注}
- 使用 AskUserQuestion 工具询问用户操作，提供以下选项：
	- 提交并推送 - 执行提交与推送
	- 修改备注后提交 - 用户输入新的提交备注后执行提交和推送
	- 提交并触发构建 - 执行提交与推送，成功后触发 Jenkins 构建
	- 修改备注后触发构建 - 用户输入新的提交备注后执行提交和推送，推送成功后触发 Jenkins 构建
- 处理用户选择：
	[提交并推送]：执行提交与推送。
	[修改备注后提交]：提示 请输入提交备注：，获取输入后更新备注并提交和推送。
	[提交并触发构建]：先执行提交与推送，推送成功后，再执行 Jenkins 构建（等同auto_submit + build_mode）
	[修改备注后触发构建]：提示 请输入提交备注：，获取输入后更新备注并提交和推送; 推送完再执行 Jenkins 构建

### 流程完成后的结果展示
	
	✅ 流程完成！
	#### 提交代码或推送代码成功后显示如下信息

	提交信息：
	  - 版本号: 
	  - 提交信息: 
	  - 分支: 
	  
	#### 触发 Jenkins 构建成功后显示如下信息
	Jenkins构建信息：
	  - Job: 
	  - 构建号: 
	  - 构建环境: 
	  - 构建url: 
	
	
