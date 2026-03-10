# Assignment 2 - Security Testing with GitHub Actions

This repository is used for:

- CodeQL code scanning
- Super-Linter multi-language linting
- Bandit Python security scanning

Languages included:
- Python
- JavaScript
- Java
 
## Reflection Questions

### 1. Do the scanner results match what you found in your previous peer review? Why or why not?

The automated scanner results were broadly consistent with the issues identified during the earlier peer review, especially around insecure coding patterns and general bad practices. However, the scanners also reported some additional findings (for example, style and configuration problems) that were not noticed in the peer review, while a few context-specific concerns raised by humans (such as how the code might be misused in the real application) were not flagged by the tools.

This shows that human reviewers are better at understanding business logic and misuse scenarios, while scanners are stronger at systematically checking for known patterns and rules across the whole codebase.

### 2. Do you think the scanners caught all vulnerabilities present in the code? Why or why not?

No. The scanners are good at catching many common and well-known vulnerability patterns (for example, dangerous functions, insecure configurations, or missing input validation in typical forms), but they are limited to what they are programmed to detect. If a vulnerability depends on specific business rules, complex data flows, or how the system is deployed in production, it may not be recognized by the tools.

Because of this, it is likely that some subtle or context-dependent vulnerabilities remain in the code, even if all the automated checks are passing.

### 3. Why is using multiple scanners better than relying on only one?

Each scanner has different strengths, coverage, and rule sets. For example:

- CodeQL focuses on data-flow and semantic analysis to find deeper security issues in the code.
- Super-Linter enforces style and best practices across multiple languages, which can indirectly prevent bugs and security problems.
- Bandit is specialized for Python security checks and looks for specific risky patterns in Python code.

Using multiple scanners in combination increases coverage: one tool may catch an issue that another misses, and together they provide more confidence that both obvious and less obvious problems are being checked. This layered approach is closer to real-world secure development practices, where you combine automated tools with human review and testing.


