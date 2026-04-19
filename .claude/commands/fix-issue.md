---
name: fix-issue
description: Analyzes and fixes a specific code issue or bug.
tools: Task, Read, Write, Bash, Grep, Glob
---

# Fix Issue

Analyzes and fixes a specific code issue or bug.

## Usage

```
/fix-issue [description]
```

## Workflow

1. Understand the issue from description or error message
2. Locate relevant code using grep/glob
3. Analyze root cause
4. Apply fix following code-style rules
5. Verify fix doesn't introduce new issues
6. Report what was changed and why

## Guidelines

- Prefer minimal changes over refactoring
- Preserve existing behavior unless explicitly asked
- Add no comments unless requested
- Test the fix if possible
