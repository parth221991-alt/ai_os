# AI_OS MCP Configuration

MCP (Model Context Protocol) servers give Claude direct access to tools, filesystems, databases, and APIs without copy-pasting context.

## Active MCPs (configured in C:\Users\Dell\.claude\settings.json)

| Name | Package | Purpose | Auth |
|---|---|---|---|
| `filesystem` | `@modelcontextprotocol/server-filesystem` | Read/write files across all AI_OS projects | None |
| `github` | `@modelcontextprotocol/server-github` | PR review, issue tracking, CI status | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| `memory` | `@modelcontextprotocol/server-memory` | Persistent semantic memory across sessions | None |
| `sqlite` | `@modelcontextprotocol/server-sqlite` | Direct query access to tasks.db (Command Center) | None — local file |
| `fetch` | `@modelcontextprotocol/server-fetch` | Fetch URLs, API endpoints, web content | None |
| `obsidian-mcp` | `obsidian-mcp` | Read/write AI_OS vault at 01_memory/vault | None — local |

## Filesystem MCP — Allowed Paths

```
D:\AI_OS
D:\OptionHABot
D:\Trading_bot_a
D:\tradecopilot
D:\TradingBotwithAIAnalyzer
C:\Users\Dell\.claude
```

To add a path: edit `settings.json` → `mcpServers.filesystem.args` array.

## Planned MCPs (not yet configured)

| Name | Purpose | Blocker |
|---|---|---|
| `brave-search` | Web search for Research Director workflow | Need `BRAVE_API_KEY` |
| Custom Quantara MCP | Direct access to Quantara API / DB | Build after Quantara paper gate completes |

## Adding a New MCP

1. Install the package: `npm install -g @modelcontextprotocol/server-<name>`
2. Add the server block to `C:\Users\Dell\.claude\settings.json` under `mcpServers`
3. If auth needed: add to `env` block in the server config
4. Restart Claude Code to activate
5. Document it here

## Tokens Required

| Token | Location | Status |
|---|---|---|
| `GITHUB_PERSONAL_ACCESS_TOKEN` | settings.json env block | ✅ Configured |
| `BRAVE_API_KEY` | Not yet in settings.json | ⏳ Pending — get from brave.com/search/api |
