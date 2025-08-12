# Claude Code Setup

> A comprehensive configuration setup for Claude Code with Model Context Protocol (MCP) servers, custom commands, and automated workflows.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blue.svg)](https://claude.ai/code) [![MCP](https://img.shields.io/badge/MCP-Enabled-green.svg)](https://modelcontextprotocol.io/) [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Features](#features)
- [Commands](#commands)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project provides a pre-configured environment for Claude Code with enhanced capabilities through:

- **MCP Servers**: Context7, Puppeteer, Sequential Thinking, DeepWiki
- **Custom Commands**: Intelligent workflows for commits, tasks, and problem-solving
- **Hook System**: Automated directory management and workflow triggers
- **Structured Workflows**: Organized task management with reporting and planning

## Quick Start

```bash
# 1. Install dependencies
pip install uv

# 2. Clone this configuration
git clone <your-repo> claude-setup
cd claude-setup

# 3. Start using commands
/task_hard implement user authentication
```

## Prerequisites

Before using this setup, ensure you have:

- **Claude Code**: Installed and configured
- **Python 3.8+**: For hook script execution
- **uv**: Package manager for Python script execution
- **Node.js**: For MCP server functionality (npx)

### Installation

#### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# After installation, open a new terminal and verify:
uv --version
```

#### 2. Setup Configuration

```bash
# Copy configuration files to your project
cp -r .claude/ /your/project/
cp .mcp.json /your/project/

# Ensure hook permissions
chmod +x .claude/hooks/task_hard_prep_hook.py
```

## Features

### 🎯 Custom Commands

- **`/commit`**: Intelligent commit workflow with conventional standards
- **`/code-review`**: Reviews uncommitted changes before committing
- **`/task_hard`**: Advanced problem-solving with automated directory management
- **`/task_easy`**: Simplified task workflow for lighter needs

### 🤖 Custom Agents

- **`investigator`**: Expert code investigator that tracks down related code to problems
  - Uses sequential thinking and advanced search tools
  - Generates comprehensive INVESTIGATION_REPORT.md files
  - Integrated with task_hard workflow
- **`code-flow-mapper`**: Expert code flow mapper that traces execution paths and file interconnections
  - Maps code flow and analyzes file relationships
  - Generates FLOW_REPORT.md files
- **`planner`**: Expert planner that takes into account investigation and flow analysis reports
  - Creates detailed plans that solve all problems
  - Generates comprehensive PLAN.md files
- **`code-reviewer`**: Senior code review specialist for quality assurance
  - Reviews changes for quality, security, and maintainability
  - Provides prioritized feedback (critical, warnings, suggestions)
  - Checks for best practices and potential issues

### 🔌 MCP Servers

- **Context7**: Library documentation and code context
- **Puppeteer**: Browser automation and web scraping
- **Sequential Thinking**: Advanced reasoning and problem-solving
- **DeepWiki**: Repository documentation fetching

### ⚡ Hook System

- **UserPromptSubmit**: Automatic directory creation for task workflows
- **Extensible**: Easy to add custom hooks for workflow automation
- **Documentation**: [Hooks Reference](https://docs.anthropic.com/en/docs/claude-code/hooks) | [Hooks Guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)

## Commands

### `/task_hard` - Advanced Problem Solving

Automated workflow for complex problem-solving with structured investigation and planning.

**Usage:**

```bash
/task_hard [problem description]
```

**Features:**

- ✅ Automatic `claude-instance-{id}` directory creation
- ✅ Sequential thinking for complex reasoning
- ✅ Multi-agent workflow with specialized subagents
- ✅ Codebase investigation with INVESTIGATION_REPORT.md generation
- ✅ Code flow mapping with FLOW_REPORT.md analysis
- ✅ Structured planning with PLAN.md output
- ✅ Incremental instance numbering
- ✅ Edge case handling and best practices focus

**Example:**

```bash
/task_hard implement user authentication system
```

**Workflow:**

1. 🔧 Hook detects `/task_hard` prompt
2. 📁 Creates `claude-code-storage/claude-instance-{id}/` directory
3. 🔍 Investigator agent analyzes codebase using sequential thinking
4. 📄 Generates comprehensive INVESTIGATION_REPORT.md with related files
5. 🗺️ Code-flow-mapper agent traces execution paths and file interconnections
6. 📊 Generates detailed FLOW_REPORT.md with code relationships
7. 📋 Planner agent reads both reports and creates comprehensive PLAN.md
8. 👤 User reviews and approves plan

### `/code-review` - Automated Code Review

Initiates code-reviewer agent to analyze uncommitted changes only.

**Usage:**

```bash
/code-review
```

**Features:**

- Focuses exclusively on uncommitted changes
- Reviews modified files for quality, security, and maintainability
- Provides prioritized feedback:
  - 🚨 Critical issues (must fix)
  - ⚠️ Warnings (should fix)
  - 💡 Suggestions (consider improving)
- Includes specific fix examples

**Example:**

```bash
# After making changes
/code-review
# Fix any critical issues
/commit
```

### `/commit` - Intelligent Commits

Streamlined commit workflow following conventional commit standards.

**Features:**

- Diff analysis and change summarization
- Conventional commit message formatting
- Clean, focused commits

**Important:** Run `/code-review` before committing to ensure code quality.

**Example:**

```bash
# Review changes first
/code-review
# After fixing issues
/commit
```

### `/task_easy` - Simplified Tasks

Lightweight task workflow for simpler problem-solving needs.

## Configuration

### Directory Structure

```
claude-setup/
├── .claude/
│   ├── settings.json          # Permissions and hook configuration
│   ├── agents/
│   │   ├── investigator.md    # Code investigation agent
│   │   ├── code-flow-mapper.md # Code flow mapping agent
│   │   ├── planner.md         # Planning agent
│   │   └── code-reviewer.md   # Code review specialist
│   ├── hooks/
│   │   └── task_hard_prep_hook.py  # Auto directory creation
│   └── commands/
│       ├── task_hard.md     # Advanced task workflow
│       ├── task_easy.md       # Simple task workflow
│       ├── code-review.md     # Code review workflow
│       └── commit.md          # Commit workflow
├── .mcp.json                  # MCP server configuration
├── claude-code-storage/       # Auto-generated task directories
└── README.md
```

### Settings Configuration

The `.claude/settings.json` file contains:

```json
{
  "permissions": {
    "allow": ["WebFetch(domain:docs.anthropic.com)", ...],
    "deny": [...]
  },
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/task_hard_prep_hook.py"
          }
        ]
      }
    ]
  },
  "enabledMcpjsonServers": ["context7", "puppeteer", "sequential-thinking", ...]
}
```

### MCP Configuration

The `.mcp.json` file defines server configurations:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["@context7/claude-dev", "--minTokens", "1000"]
    },
    "puppeteer": {
      "command": "npx",
      "args": ["@puppeteer/claude-dev"]
    }
  }
}
```

## Troubleshooting

### Common Issues

**Hook not triggering:**

- Ensure `uv` is installed and in PATH
- Check script permissions: `chmod +x .claude/hooks/task_hard_prep_hook.py`
- Verify hook configuration in `.claude/settings.json`

**Directory creation fails:**

- Check file system permissions
- Ensure `claude-code-storage/` parent directory exists
- Review hook script logs for error details

**MCP servers not loading:**

- Verify Node.js and npx are installed
- Check `.mcp.json` configuration syntax
- Ensure MCP packages are available via npx

### Debug Mode

Enable debug mode for detailed logging:

```bash
claude --debug
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

### Adding Custom Hooks

1. Create script in `.claude/hooks/`
2. Make executable: `chmod +x .claude/hooks/your_hook.py`
3. Add configuration to `.claude/settings.json`
4. Test with sample inputs

**Resources:**

- [Hooks Reference Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Hooks Implementation Guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AizenvoltPrime/claude-setup&type=Date)](https://star-history.com/#AizenvoltPrime/claude-setup&Date)

## License

This configuration setup is provided as-is for Claude Code enhancement.

---

**Need help?** Check the documentation:

- [Claude Code Main Docs](https://docs.anthropic.com/claude-code)
- [Hooks Reference](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Hooks Implementation Guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)

Or open an issue for project-specific questions.
