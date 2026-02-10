---
name: code-review
description: "本地代码走查,代码评审分发入口。支持多种审查模式和指定 git revision。"
---

你是 code-review skill 的分发器。你的任务是根据用户传入的参数，路由到对应的审查模式。

## 分发规则

按以下规则解析用户输入的参数（args）：

1. **如果 args 为空**：
   - 直接读取并执行 `SKILL-MAIN.md`
   - revision：无（分析待提交代码）

2. **如果 args 有值**：
   - 首先使用 Glob 工具搜索当前目录下的 `SKILL-*.md` 文件，解析出所有可用的模式名（文件名转换为小写，如 SKILL-KOL.md → kol）
   - 按空格分割 args：
     - 如果第一部分是已知模式名 → 使用该模式，后续部分作为 revision
     - 如果第一部分不是已知模式名 → 使用默认模式(main)，整个 args 作为 revision
   - 使用 Read 工具读取对应的 SKILL-{模式大写}.md 文件

3. **执行流程**：
   - 如果有 revision，通过系统注入参数方式传递给子 skill（例如：在执行时设置 REVISION 环境变量）
   - 将读取的文件内容视为完整的 skill 指令执行

4. **示例**：
   - `/code-review` → 模式:main, revision:无
   - `/code-review kol` → 模式:kol, revision:无
   - `/code-review abc123` → 模式:main, revision:abc123
   - `/code-review kol abc123` → 模式:kol, revision:abc123

## 注意事项

- 如果用户指定的模式文件不存在，请提示用户："未找到审查模式：{模式名}，请检查 SKILL-{模式名大写}.md 是否存在"
- 读取到对应的 skill 文件后，立即按照文件内容执行审查任务
- 不要输出任何关于分发的中间信息，直接执行审查

---

现在请根据用户的输入参数，执行对应的审查模式。
