Use sequential-thinking mcp and all its tools that you will need about the problem and how to solve it. You must ultrathink for the solution and use reasoning.

You must consider edge cases and follow best coding practices for everything. Never do bandaid fixes.

## Configuration

STEP 1: You must use the investigator subagent and you must always pass to it the full path of the created claude-instance-{id} directory that was automatically created for this claude session.

STEP 2: You must use the code-flow-mapper subagent and you must always pass to it the full path of the created claude-instance-{id} directory that was automatically created for this claude session.

STEP 3: You must use the planner subagent and you must always pass to it the full path of the created claude-instance-{id} directory that was automatically created for this claude session.

STEP 4: After all three subagents finish, enter plan mode and read the "PLAN.md" file and present the plan to the user so that they can either accept or adjust it.

Problem: $ARGUMENTS
