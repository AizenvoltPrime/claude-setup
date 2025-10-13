Use sequential-thinking mcp and all its tools that you will need about the problem and how to solve it. You must ultrathink for the solution and use reasoning.

You must consider edge cases and follow best coding practices for everything. Never do bandaid fixes. Never implement fallbacks. Never implement backwards compatibility. Never use inline comments. Always write self-documenting code with clear naming and structure. Use concise documentation comments for methods, classes, and properties to describe their purpose.

## Configuration

**IMPORTANT: Execute these steps SEQUENTIALLY - wait for each subagent to complete before starting the next one. NEVER run subagents in parallel.**

STEP 1: You must use the investigator subagent and you must always pass to it the full path of the created claude-instance-{id} directory that was automatically created for this claude session. If the user's problem statement includes "Keywords:" followed by comma-separated keywords, make sure to pass these keywords to the investigator subagent with special instructions to prioritize files containing these keywords during investigation. If no explicit "Keywords:" are provided, analyze the Problem statement to extract the most relevant keywords and pass these automatically identified keywords to the investigator subagent for prioritization. Wait for this subagent to complete before proceeding to step 2.

STEP 2: After the investigator completes, use the code-flow-mapper subagent and you must always pass to it the full path of the created claude-instance-{id} directory that was automatically created for this claude session. Wait for this subagent to complete before proceeding to step 3.

STEP 3: After the code-flow-mapper completes, use the planner subagent and you must always pass to it the full path of the created claude-instance-{id} directory that was automatically created for this claude session. Wait for this subagent to complete before proceeding to step 4.

STEP 4: After all three subagents finish sequentially, enter plan mode and read the "PLAN.md" file and present the plan to the user so that they can either accept or adjust it.

Problem: $ARGUMENTS
