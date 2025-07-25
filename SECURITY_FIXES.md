# Security Fixes Documentation

This document tracks the security vulnerabilities that have been addressed in the Setwise project.

## Fixed Vulnerabilities

### 1. Subprocess shell=True Vulnerability (Issue #1)
- **Severity**: HIGH
- **CWE**: CWE-78 (OS Command Injection)
- **Bandit ID**: B602
- **File**: generate_template_previews.py:19
- **Fix**: Replaced `shell=True` with secure `shlex.split()` argument parsing
- **Status**: ✅ Fixed in commit d624b24

### 2. Jinja2 autoescape Vulnerability (Issue #2)  
- **Severity**: HIGH
- **CWE**: CWE-94 (Code Injection)
- **Bandit ID**: B701
- **File**: main.py:126
- **Fix**: Enabled `autoescape=True` in Jinja2 Environment configuration
- **Status**: ✅ Fixed in commit d624b24

### 3. Test Coverage Improvements (Issue #3)
- **Coverage**: Improved from 56% to ~85% (+29% improvement)
- **New Test Files**: 
  - test_generate_figures.py (99% coverage)
  - test_generate_template_previews.py (95% coverage)  
  - test_template_config.py (100% coverage)
- **Status**: ✅ Fixed in commit c4b40e9

## Verification

Run local security scan to verify fixes:
```bash
# Install security tools
pip install bandit safety pip-audit

# Run security scan
bandit -r . -f txt

# Check for known vulnerabilities
safety check
```

## Security Attribution

Security vulnerabilities reported by **Prof. Shouvick Mondal, IIT Gandhinagar**.