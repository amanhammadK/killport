#!/usr/bin/env node
import { execSync } from "child_process";

function killPort(port: number): string {
  try {
    const cmd = process.platform === "win32"
      ? `netstat -ano | findstr :${port} | findstr LISTENING`
      : `lsof -ti :${port} | xargs kill -9`;
    const output = execSync(cmd, { encoding: "utf-8", timeout: 5000 });
    if (process.platform === "win32") {
      const lines = output.trim().split("\n");
      for (const line of lines) {
        const parts = line.trim().split(/\s+/);
        const pid = parts[parts.length - 1];
        if (pid) execSync(`taskkill /PID ${pid} /F`, { encoding: "utf-8", timeout: 3000 });
      }
    }
    return `Killed process(es) on port ${port}`;
  } catch { return `No process found on port ${port}`; }
}

const port = parseInt(process.argv[2] || "3000");
console.log(killPort(port));
