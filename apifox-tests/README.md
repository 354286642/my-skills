# apifox-tests

Apifox 自动化测试执行技能，用于验证 API 接口的可用性和正确性。

## 功能描述

自动执行 Apifox 中配置的 API 测试用例，并解读测试结果。支持多种测试场景和环境的切换。

## 目录结构

```
apifox-tests/
├── scripts/
│   ├── list-tests.js      # 列出可用的测试场景
│   └── run-cli.js         # 执行测试的核心脚本
├── env/
│   ├── dev.env            # 开发环境配置
│   └── dev.env.example    # 环境配置模板
├── tests/
│   └── 全案项目场景流程.md # 测试场景文档
└── SKILL.md               # 技能配置文件
```

## 触发场景

- 修改代码后需要验证接口可用性
- git commit/push 前的接口检查
- 发布版本前的回归测试
- 用户明确要求运行 Apifox 测试
- 合并到 main 分支前的自动化检查

## 使用方法

### 基本用法

```
/apifox-tests
```

该命令会列出所有可用的测试场景，供用户选择执行。

### 指定环境

```
/apifox-tests dev          # 在开发环境执行
/apifox-tests test         # 在测试环境执行
/apifox-tests prod         # 在生产环境执行
```

## 环境配置

复制 `env/dev.env.example` 为 `dev.env` 并配置以下参数：

```env
APIFOX_TOKEN=your_token_here
APIFOX_BASE_URL=https://api.apifox.com
```

## 支持的测试类型

1. **接口功能测试** - 验证接口返回数据的正确性
2. **接口性能测试** - 检查接口响应时间
3. **接口安全测试** - 检测认证、授权等安全问题
4. **场景流程测试** - 多接口组合的业务流程测试

## 输出结果

技能执行后会输出：
- 测试用例总数和通过数
- 失败用例的详细信息
- 响应时间统计
- 错误堆栈（如有）

## 依赖项

- Node.js >= 14
- dotenv (环境变量管理)
- Apifox CLI
