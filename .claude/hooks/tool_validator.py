#!/usr/bin/env python3
"""
Claude Code Hook: Tool Validator
Enforces preferred tool usage and blocks prohibited commands.
"""

import json
import sys
import re
import shlex

# Tool mappings: prohibited -> preferred
TOOL_MAPPINGS = {
    'grep': {
        'tool': 'rg (ripgrep)',
        'tips': 'Common flags: -i (ignore case), -n (line numbers), -A/-B/-C (context lines), -l (files only), -t (file types)'
    },
    'cat': {
        'tool': 'bat',
        'tips': 'Common flags: -n (line numbers), -p (plain), -A (show all), -r (line range), --color=always|never'
    },
    'find': {
        'tool': 'fd',
        'tips': 'Common flags: -t f|d|l (file type), -e ext (extension), -H (hidden), -d num (max depth), -x cmd (execute)'
    },
    'awk': {
        'tool': 'sed or sd (for text manipulation) or jq (for JSON)',
        'tips': 'sed: -i (in-place), -e (expression), -r (extended regex) | sd: \'pattern\' \'replacement\' files (-p preview, -F fixed strings) | jq: -r (raw), -c (compact), .key syntax'
    },
    'perl': {
        'tool': 'sed or sd',
        'tips': 'sed: -i (in-place), -e (expression), -n (quiet), -r (extended regex) | sd: \'pattern\' \'replacement\' files (-p preview, -f flags)'
    },
    'cut': {
        'tool': 'xsv (for CSV data)',
        'tips': 'Common commands: xsv select, xsv search, xsv headers, xsv count, xsv stats'
    },
}

# Native tools that should be replaced with Bash equivalents
NATIVE_TOOL_REPLACEMENTS = {
    'Read': {
        'tool': 'Bash tool with bat command',
        'tips': 'Use: bat filename [-n line numbers] [-p plain] [-r start:end range]'
    },
    'Edit': {
        'tool': 'Bash tool with rg, bat, and sed/sd commands',
        'tips': 'Use: rg pattern + bat file + sed -i "s/old/new/g" file OR sd "old" "new" file'
    },
    'Write': {
        'tool': 'Bash tool with appropriate text manipulation commands',
        'tips': 'Use: echo content > file, or sed "s/old/new/g" file OR sd "old" "new" file for modifications'
    },
    'MultiEdit': {
        'tool': 'Bash tool with rg and sed/sd for multiple file edits',
        'tips': 'Use: rg -l pattern | xargs sed -i "s/old/new/g" OR rg -l pattern | xargs -I {} sd "old" "new" {}'
    },
}

def extract_command_from_bash_input(tool_input):
    """Extract the command string from Bash tool input."""
    if isinstance(tool_input, dict):
        return tool_input.get('command', '')
    return str(tool_input)

def extract_commands(command):
    """Extract actual command names from a shell command string."""
    # Split on shell operators (pipes, semicolons, &&, ||, etc.)
    # This separates compound commands
    segments = re.split(r'[|;&]+|\s+&&\s+|\s+\|\|\s+', command)

    commands = []
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        try:
            # Use shlex to properly tokenize while respecting quotes
            tokens = shlex.split(segment)
            if tokens:
                # First token is the command name
                cmd = tokens[0].lower()
                # Remove path components (e.g., /usr/bin/grep -> grep)
                cmd = cmd.split('/')[-1]
                commands.append(cmd)
        except ValueError:
            # If shlex fails (unmatched quotes, etc.), fall back to simple split
            # This handles edge cases with incomplete commands
            first_word = segment.split()[0] if segment.split() else ''
            if first_word:
                cmd = first_word.lower().strip('`"\'')
                cmd = cmd.split('/')[-1]
                commands.append(cmd)

    return commands

def check_prohibited_commands(command):
    """Check if command contains prohibited tools."""
    commands = extract_commands(command)

    for cmd in commands:
        if cmd in TOOL_MAPPINGS:
            return cmd, TOOL_MAPPINGS[cmd]

    return None, None

def check_markdown_manipulation_patterns(command):
    """Detect specific patterns where markdown content should be manipulated with mdq."""
    # Simple patterns to detect markdown-specific operations
    if not any(ext in command.lower() for ext in [".md", ".markdown", ".mdown"]):
        return None, None

    # Check for header extraction with rg
    if "rg" in command.lower() and "#" in command:
        return "header extraction", "mdq \"h1,h2,h3\" file.md"

    # Check for code block extraction
    if "rg" in command.lower() and ("```" in command or "~~~" in command):
        return "code block extraction", "mdq \"pre,code\" file.md"

    # Check for list extraction
    if "rg" in command.lower() and ("\\*" in command or "\\-" in command):
        return "list extraction", "mdq \"ul,ol,li\" file.md"

    # Check for sed modifications of markdown structure
    if ("sed" in command.lower() or "sd" in command.lower()) and "-i" in command and "#" in command:
        return "header modification", "Use mdq to extract, then redirect output for safe editing"

    return None, None

def check_contextual_requirements(command):
    """Check for file types that benefit from specialized tools."""
    # CSV/TSV operations
    if any(ext in command.lower() for ext in [".csv", ".tsv"]):
        return "csv", {
            'tool': 'xsv',
            'tips': 'xsv select (columns), xsv search (filter), xsv stats (analysis), xsv headers (list columns)'
        }

    # JSON operations
    if ".json" in command.lower() and ("sed" in command.lower() or "awk" in command.lower()):
        return "json", {
            'tool': 'jq',
            'tips': 'jq "." (pretty print), jq ".key" (extract), jq -r (raw output), jq -c (compact)'
        }

    # YAML operations
    if any(ext in command.lower() for ext in [".yaml", ".yml"]):
        return "yaml", {
            'tool': 'yq',
            'tips': 'yq ".key" (extract), yq -i (in-place edit), yq eval-all (multiple files)'
        }

    return None, None

def main():
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Handle both camelCase and snake_case formats
        tool_name = hook_input.get('tool_name', hook_input.get('toolName', ''))
        tool_input = hook_input.get('tool_input', hook_input.get('toolInput', {}))

        # Allow modern native tools (Grep and Glob are already modern equivalents)
        if tool_name in ['Grep', 'Glob']:
            # These are Claude Code's native modern tools - allow them
            sys.exit(0)

        # Check for native tool usage (Read, Edit, Write, MultiEdit)
        if tool_name in NATIVE_TOOL_REPLACEMENTS:
            replacement = NATIVE_TOOL_REPLACEMENTS[tool_name]
            print(f"ℹ️  Consider using {replacement['tool']} for better performance.", file=sys.stderr)
            print(f"💡 {replacement['tips']}", file=sys.stderr)
            # Don't block - this is just a suggestion

        # Handle Bash commands
        if tool_name == 'Bash':
            command = extract_command_from_bash_input(tool_input)

            # Check for prohibited commands
            prohibited_tool, preferred_tool = check_prohibited_commands(command)
            if prohibited_tool:
                print(f"❌ Prohibited tool '{prohibited_tool}' detected in command.", file=sys.stderr)
                print(f"✅ Use {preferred_tool['tool']} instead.", file=sys.stderr)
                print(f"💡 {preferred_tool['tips']}", file=sys.stderr)
                print("💡 This follows your CLAUDE.md tool preferences.", file=sys.stderr)
                sys.exit(2)

            # Check contextual requirements
            file_type, required_tool = check_contextual_requirements(command)
            if file_type and required_tool:
                print(f"ℹ️  Consider using {required_tool['tool']} for {file_type.upper()} files.", file=sys.stderr)
                print(f"💡 {required_tool['tips']}", file=sys.stderr)
                print("💡 This follows your CLAUDE.md preference for specialized tools.", file=sys.stderr)
                # Don't exit - this is just a suggestion

            # Check markdown-specific manipulation patterns
            markdown_operation, mdq_suggestion = check_markdown_manipulation_patterns(command)
            if markdown_operation and mdq_suggestion:
                print(f"ℹ️  Detected {markdown_operation} on Markdown file.", file=sys.stderr)
                print(f"✅ Consider using: {mdq_suggestion}", file=sys.stderr)
                print("💡 mdq is optimized for structured Markdown content extraction.", file=sys.stderr)

        # Allow the tool to execute
        sys.exit(0)

    except json.JSONDecodeError:
        print("❌ Invalid JSON input to hook", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"❌ Hook error: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == '__main__':
    main()
