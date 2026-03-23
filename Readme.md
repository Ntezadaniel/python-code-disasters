# Practical Assignment — Error Handling & Logging in Python

**Open-source project analyzed:** [sobolevn/python-code-disasters](https://github.com/sobolevn/python-code-disasters)  
**Language:** Python  
**Student:** Kirabo Daniel Nteza  
**Course:** Software Construction  
**Date:** March 2026



## 1. Project Selection

I selected **`sobolevn/python-code-disasters`** as my reference open-source project.

**Why this project?**
- It is a real, public GitHub repository with 161+ stars specifically created to collect and showcase **poorly written Python code** submitted by real developers
- It contains actual Flask and Django code examples with genuine error handling problems
- The patterns in this repo closely mirror what is commonly found in real-world open-source projects
- It is an ideal candidate for analyzing bad exception strategies and missing logging

**Repository structure analyzed:**
```
sobolevn/python-code-disasters/
├── python/       ← General Python scripts with bad practices
├── flask/        ← Flask-specific bad code
├── django/       ← Django-specific bad code
└── obfuscation/  ← Obfuscated/unreadable Python
```

The files `bad_error_handling.py` and `improved_error_handling.py` in this submission are directly modeled after real patterns found across the `python/` and `flask/` folders of this repository.



## 2. Error Handling Anti-Patterns Identified

The following problems were identified by analyzing code patterns in the repository:

| # | Pattern Found In Repo | Problem | Why It's Bad |
|---|----------------------|---------|--------------|
| 1 | `python/` scripts | Bare `except:` clause | Catches `SystemExit`, `KeyboardInterrupt`, hides all error detail |
| 2 | `flask/` handlers | `except Exception: pass` | Silently swallows errors; caller gets `None` with no explanation |
| 3 | Multiple files | Generic `raise Exception("msg")` | No distinction between input errors and processing errors |
| 4 | `flask/` views | Zero logging anywhere | Impossible to debug failures in production |
| 5 | Various files | `raise Exception(...)` without `from e` | Loses original traceback, root cause becomes invisible |

These are documented in `bad_error_handling.py` with inline comments explaining each problem.



## 3. Improvements Made

### 3a. Exception Strategy Fixes

- **Replaced bare `except`** with specific exceptions (`ConnectionError`, `Timeout`, `HTTPError`, `JSONDecodeError`)
- **Eliminated silent swallowing** — exceptions are now logged then re-raised so callers can handle them appropriately
- **Created custom exception classes** (`InvalidPaymentAmountError`, `PaymentProcessingError`) for semantic clarity
- **Used `raise ... from e`** to preserve the full exception chain and traceback
- **Added parameterized queries** to `delete_record` to prevent SQL injection (bonus fix)

### 3b. Meaningful Logging Added

Every function now logs at the appropriate level:

| Level | When Used |
|-------|-----------|
| `INFO` | Start of a significant operation |
| `DEBUG` | Successful completion with relevant details |
| `WARNING` | Bad inputs that are handled gracefully |
| `ERROR` | Exceptions caught, with all context variables |
| `logger.exception()` | Inside `except` blocks — auto-includes full stack trace |

Log output format:
```
2026-03-23 12:00:01 | INFO     | __main__ | Fetching user data for user_id=42
2026-03-23 12:00:02 | ERROR    | __main__ | Request timed out for user_id=42 (url=https://...)
```



## 4. AI-Generated vs Human Reasoning — Comparison

This section compares suggestions produced by an AI assistant (Claude by Anthropic) with what a human developer would typically reason through when fixing the same code.

### Function: `fetch_user_data`

| Aspect | AI Suggestion | Human Reasoning |
|--------|--------------|-----------------|
| Exception types | Immediately listed all `requests` sub-exceptions | Human might start with `RequestException` then refine after testing |
| Logging detail | Suggested logging the URL and user_id upfront | Human might only log user_id initially, add URL after a bug report |
| Timeout | Added `timeout=5` proactively | Human typically adds timeout only after experiencing a production hang |
| Overall quality | More complete from the start | Human reasoning is iterative and experience-driven |

### Function: `read_config`

| Aspect | AI Suggestion | Human Reasoning |
|--------|--------------|-----------------|
| Re-raising | Suggested `raise` immediately to preserve caller control | Human might return `None` first, then switch to raise after debugging |
| Encoding | Added `encoding="utf-8"` proactively | Often forgotten until a Unicode crash appears in production |
| Error messages | Detailed messages including filepath in every log | Human messages tend to be less consistent across functions |

### Function: `process_payment`

| Aspect | AI Suggestion | Human Reasoning |
|--------|--------------|-----------------|
| Custom exceptions | Immediately proposed custom exception classes | Human often starts with `ValueError`, promotes to custom class later |
| Type checking | Added `isinstance` check for amount type | Human might only add this after a TypeError crash from unexpected input |
| Logging levels | Used `WARNING` for bad input, `ERROR` for unexpected failure | Human might use `ERROR` for everything initially |

### Key Takeaways

1. **AI is better at consistency** — it applied the same logging format and exception strategy uniformly across all functions. Human developers often apply fixes inconsistently as they discover bugs one at a time.

2. **Human reasoning is more context-aware** — a human developer knows which errors are *actually* common in their specific codebase. An AI treats all possible errors as equally likely to occur.

3. **AI catches edge cases earlier** — encoding issues, timeouts, and type checks were added proactively by the AI. Humans typically add these only after experiencing the problem in production.

4. **Humans produce leaner code** — a human might deliberately omit some log lines to reduce noise in logs. AI tends to log at every possible point.

5. **Both agree on the fundamentals** — never swallow exceptions silently, always preserve traceback context with `raise ... from e`, and always use specific exception types instead of bare `except` or generic `Exception`.



## 5. Files in This Repository

| File | Description |
|------|-------------|
| `bad_error_handling.py` | Original poorly written code modeled on patterns from `sobolevn/python-code-disasters` |
| `improved_error_handling.py` | Fixed version with proper specific exceptions and structured logging |
| `README.md` | This document — project selection, analysis, fixes, and AI vs human comparison |

---

## 6. How to Run

```bash
# Install dependency
pip install requests

# Run the improved version
python improved_error_handling.py
```

Logs will appear in the console and be saved to `app.log` in the same directory.



## 7. References

- Repository analyzed: https://github.com/sobolevn/python-code-disasters
- Python logging docs: https://docs.python.org/3/library/logging.html
- Python exceptions docs: https://docs.python.org/3/library/exceptions.html
- Requests library exceptions: https://docs.python-requests.org/en/latest/api/#exceptions
