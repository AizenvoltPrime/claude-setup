#!/usr/bin/env python3
"""
UserPromptSubmit hook for task_medium directory preparation.
Automatically creates claude-instance-{id} directories when users type /task_medium.
"""
import json
import os
import sys
import re
from pathlib import Path


def get_next_instance_id(base_dir: Path) -> int:
    """Find the next available instance ID by checking existing directories."""
    if not base_dir.exists():
        return 1

    existing_dirs = [
        d for d in base_dir.iterdir()
        if d.is_dir() and d.name.startswith('claude-instance-')
    ]

    if not existing_dirs:
        return 1

    # Extract numbers from directory names
    numbers = []
    for dir_path in existing_dirs:
        match = re.search(r'claude-instance-(\d+)', dir_path.name)
        if match:
            numbers.append(int(match.group(1)))

    return max(numbers) + 1 if numbers else 1


def create_instance_directory(cwd: str, instance_id: int) -> tuple[bool, str]:
    """Create the claude-instance directory and return success status and path."""
    try:
        base_dir = Path(cwd) / "claude-code-storage"
        instance_dir = base_dir / f"claude-instance-{instance_id}"

        # Create directories with proper permissions
        base_dir.mkdir(exist_ok=True)
        instance_dir.mkdir(exist_ok=True)

        return True, str(instance_dir)
    except Exception as e:
        return False, str(e)


def validate_prompt(prompt: str) -> bool:
    """Check if prompt starts with /task_medium and requires directory setup."""
    # Strip whitespace and check for /task_medium at the start
    cleaned_prompt = prompt.strip()
    return cleaned_prompt.startswith('/task_medium')


def main():
    """Main hook execution logic."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        # Not a JSON input, exit silently
        sys.exit(0)

    # Extract required fields
    prompt = input_data.get("prompt", "")
    cwd = input_data.get("cwd", os.getcwd())

    # Check if this is a task_medium prompt
    if not validate_prompt(prompt):
        # Not a task_medium prompt, exit silently to allow normal processing
        sys.exit(0)

    # Get next instance ID
    base_dir = Path(cwd) / "claude-code-storage"
    instance_id = get_next_instance_id(base_dir)

    # Create instance directory
    success, result = create_instance_directory(cwd, instance_id)

    if success:
        # Extract the original problem from the prompt (after /task_medium)
        problem_text = prompt.replace('/task_medium', '').strip()

        # Output context message that will be added to the prompt
        context_msg = f"Directory claude-instance-{instance_id} has been automatically created for this claude session. The subagents will create the INVESTIGATION_REPORT.md, FLOW_REPORT.md and PLAN.md files inside {result}/ directory."
        if problem_text:
            context_msg += f" Problem to solve: {problem_text}"

        print(context_msg)
        sys.exit(0)
    else:
        # Output error but don't block processing
        print(f"Warning: Failed to create instance directory: {result}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()