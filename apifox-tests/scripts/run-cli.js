import fs from"fs";
import path from"path";
import { execSync } from"child_process";
import dotenv from"dotenv";
import { fileURLToPath } from"url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// args
const mdPath = process.argv[2];
const envName = process.argv[3] || "local";

if (!mdPath) {
    console.error("❌ 缺少测试 md 文件路径");
    process.exit(1);
}

// env 路径：始终相对 skills 本身
const envPath = path.join(__dirname, "..", "env", `${envName}.env`);

if (!fs.existsSync(envPath)) {
    console.error(`❌ 未找到环境配置：${envPath}`);
    process.exit(1);
}

dotenv.config({ path: envPath });

// 读取 md
const content = fs.readFileSync(mdPath, "utf-8");
const match = content.match(/```bash([\s\S]*?)```/);

if (!match) {
    console.error("❌ 未找到 bash 命令块");
    process.exit(1);
}

let command = match[1].trim();

// 变量替换
command = command
    .replaceAll("$APIFOX_ACCESS_TOKEN", process.env.APIFOX_ACCESS_TOKEN)
    .replaceAll("$APIFOX_ENV_ID", process.env.APIFOX_ENV_ID);

console.log(`▶ Running (${envName})`);
console.log(command);

// 执行
try {
    execSync(command, { stdio: "inherit" });
} catch (e) {
    // Apifox CLI 在测试失败时会返回退出码 1
    process.exit(1);
}