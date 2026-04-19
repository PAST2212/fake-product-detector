---
name: review
description: Performs a focused review of code changes or specific files.
tools: Task, Read, Bash, Grep, Glob
---

# Code Review

Performs a focused review of code changes or specific files.

## Usage

```
/review [files...]
```

## Workflow

1. Identify changed/new files using git diff or specified paths
2. For each file:
   - Check for security issues (secrets, hardcoded credentials, injection risks)
   - Verify code style consistency
   - Check error handling
   - Review test coverage
3. Summarize findings with severity (critical/warning/suggestion)
4. Recommend specific fixes if issues found

## Focus Areas

- Security: exposed secrets, SQL/injection vulnerabilities, unsafe inputs
- Correctness: logic errors, edge cases, exception handling
- Maintainability: code duplication, complexity, unclear naming
