import fs from"fs";
import path from"path";
import { fileURLToPath } from"url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const testsDir = path.join(__dirname, "..", "tests");

function scan(dir, relativePath = "") {
    const items = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const item of items) {
        const fullPath = path.join(dir, item.name);
        const relPath = path.join(relativePath, item.name);
        
        if (item.isDirectory()) {
            scan(fullPath, relPath);
        } elseif (item.name.endsWith(".md")) {
            try {
                const content = fs.readFileSync(fullPath, "utf-8");
                const firstLine = content.split("\n")[0].trim();
                const description = firstLine.startsWith(">") 
                    ? firstLine.replace(/^>\s*/, "").trim() 
                    : "无描述";
                const displayPath = path.join("./.claude/skills/apifox-tests/tests", relPath);
                console.log(`[${displayPath}] - ${description}`);
            } catch (err) {
                console.log(`[${relPath}] - (无法读取内容)`);
            }
        }
    }
}

console.log("🔍 可用的 Apifox 自动化测试列表：");
if (fs.existsSync(testsDir)) {
    scan(testsDir);
} else {
    console.log("❌ 未找到 tests 目录");
}