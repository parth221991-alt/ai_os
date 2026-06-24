# 3 Ways to Use Claude
## Your Complete Setup Guide

From **@ai_snipp** | Claude AI • Tools • Cheat Codes

---

> You're already using Claude — but most people only ever use one interface.
> This guide covers all three: Web → Desktop → CLI.
> 5 minutes to set up whichever one fits you.

---

## MODE 1 — Claude.ai (Web)
### The starting point. Works in any browser.

**What it is:**
The browser version of Claude. Free tier available. The interface most people already know.

**What makes it powerful:**
- **Projects** — persistent memory across conversations. Claude remembers your context.
- **Artifacts** — live code preview inside the chat. Ask Claude to build a chart, a React component, or a calculator — it runs right there in the browser.
- **File uploads** — PDFs, images, CSVs, code files. Claude reads and analyzes them.
- **Large context** — Claude Pro supports up to 200K tokens. Paste entire codebases.

**How to set it up:**

1. Go to **claude.ai**
2. Sign up free — or upgrade to **Claude Pro ($20/month)** for priority access, more messages, and Projects
3. Create your first Project:
   - Left sidebar → **New Project**
   - Add a custom instruction (example: *"I am an Indian developer building trading bots in Python. Always give me code-first answers."*)
   - Every conversation inside the Project shares this context
4. Try Artifacts — ask Claude: *"Build me a bar chart from this data"* — an interactive preview opens on the right

**Best for:**
Chatting, research, writing, code explanations, PDF analysis, brainstorming

---

## MODE 2 — Claude Desktop
### Same interface. Plus your local files and apps.

**What it is:**
A downloadable app for Mac and Windows. Identical to the web version — but with one major addition: **MCP servers**. MCP (Model Context Protocol) lets Claude connect to your local filesystem, browser, databases, and other tools.

**What makes it powerful:**
- Claude can **read and write your local files** — ask it to summarize a folder, find a file, or edit a document
- Claude can **control your browser** — navigate pages, extract data, fill forms
- Everything runs locally — your files never leave your machine unless you send them

**How to set it up:**

**Step 1 — Download**
- Go to **claude.ai** → scroll to the footer → click **Download Claude**
- Mac: Open the `.dmg` → drag Claude to your Applications folder
- Windows: Run the `.exe` installer → follow the prompts
- Sign in with your existing Claude account

**Step 2 — Connect the Filesystem MCP Server**
- Open Claude Desktop → click the **Settings** icon (top right) → **Developer**
- Click **Edit Config** — this opens a JSON config file
- Replace the contents with:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/YOUR_USERNAME/Documents"
      ]
    }
  }
}
```

- Replace `/Users/YOUR_USERNAME/Documents` with any folder path you want Claude to access
- **Save the file** → **Restart Claude Desktop**
- You should see a **hammer icon** (🔨) in the chat input bar — this confirms MCP is active

**Step 3 — Test it**
Ask Claude: *"What files are in my Documents folder?"*
Claude should list your actual files by name.

**Step 4 — Add the Browser MCP Server (optional)**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/YOUR_USERNAME/Documents"]
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```
This lets Claude control a headless browser — useful for scraping, automation, and research.

**Best for:**
Power users who want Claude to see their actual work — files, documents, projects, live apps

---

## MODE 3 — Claude Code (CLI)
### AI assistant that lives in your terminal.

**What it is:**
A command-line tool. You `cd` into any project folder, type `claude`, and Claude becomes your coding co-pilot — right in the terminal. It reads your files, writes code, runs commands, and explains bugs. No browser tab. No switching windows.

**What makes it powerful:**
- Claude has **full access to your project files** — it reads them automatically without you pasting anything
- It can **run shell commands** — execute tests, check git status, install packages
- It can **edit files directly** — write a function, save it, done
- Stays in your flow — you never leave the terminal

**How to set it up:**

**Step 1 — Check Node.js version**
```bash
node --version
```
You need Node.js 18 or higher. If not installed: **nodejs.org** → download and install.

**Step 2 — Install Claude Code**
```bash
npm install -g @anthropic-ai/claude-code
```

**Step 3 — Get your API key**
- Go to **console.anthropic.com/settings/keys**
- Click **Create Key** → give it a name → copy the key (`sk-ant-api03-...`)
- Keep this key private — treat it like a password

**Step 4 — Set your API key**

Mac / Linux:
```bash
export ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```
To make this permanent (so you don't set it every session):
```bash
echo 'export ANTHROPIC_API_KEY=sk-ant-api03-your-key-here' >> ~/.zshrc
source ~/.zshrc
```

Windows (PowerShell):
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-your-key-here"
```
To make permanent: set it in System → Environment Variables.

**Step 5 — Start Claude Code**
```bash
cd your-project-folder
claude
```

**Step 6 — Try these prompts**
```
> Review this project for security issues
> Write unit tests for the login() function
> What does the process_order() function do?
> Fix the bug on line 47 of auth.py
> Explain this error: [paste error message]
> Refactor this file to use async/await
```

**Useful commands inside Claude Code:**
| Command | What it does |
|---------|-------------|
| `/help` | See all available commands |
| `/clear` | Clear the current conversation |
| `/exit` | Quit Claude Code |
| `Ctrl+C` | Interrupt a running task |

**Note on cost:**
Claude Code uses your Anthropic API credits. Check current pricing at **console.anthropic.com**. For light daily use, typical cost is $5–15/month. Monitor your usage in the console dashboard.

**Best for:**
Developers who write code every day and want AI help without leaving the terminal

---

## Quick Decision Guide

| Your situation | Use this |
|----------------|----------|
| Just chatting, research, writing | **Claude.ai (Web)** |
| Want Claude to read your local files and apps | **Claude Desktop** |
| Writing code in a terminal every day | **Claude Code (CLI)** |
| Building a product or app using Claude | **Anthropic API** — console.anthropic.com |

> **You can use all three at once.** Most power users run Claude Desktop + Claude Code CLI as their daily setup, and keep the web version for quick chats on the go.

---

## Useful Links

| Resource | Link |
|----------|------|
| Claude Web | claude.ai |
| Claude Desktop Download | claude.ai (scroll to footer) |
| Claude Code Docs | docs.anthropic.com/claude-code |
| Anthropic API Console | console.anthropic.com |
| MCP Server Directory | modelcontextprotocol.io |

---

*Guide by @ai_snipp — follow for more AI cheat codes like this*
*Instagram · YouTube · Telegram: @ai_snipp*
