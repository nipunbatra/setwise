# Setwise Testing Scripts

This directory contains scripts for testing and quality assurance.

## security_test.sh

Comprehensive local security testing script that runs:
- **Bandit**: Static security analysis for Python code
- **Safety**: Known vulnerability database checks
- **pip-audit**: Dependency vulnerability scanning
- **pytest**: Test suite with coverage reporting

### Usage

```bash
# Make executable (first time only)
chmod +x scripts/security_test.sh

# Run comprehensive security tests
./scripts/security_test.sh
```

### What it checks

- ✅ Fixes for B602/CWE-78 (subprocess shell injection)
- ✅ Fixes for B701/CWE-94 (Jinja2 autoescape)
- ✅ Dependency vulnerabilities
- ✅ Test coverage (target: 85%+)
- ✅ Code quality metrics

### Output

- Console output with security scan results
- `htmlcov/index.html` - Detailed coverage report
- Security issues filtered to show only relevant findings

Use this script before committing changes to ensure security standards are maintained.