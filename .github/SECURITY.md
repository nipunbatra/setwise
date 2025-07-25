# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | ✅ Yes              |
| < 1.0   | ❌ No               |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these guidelines:

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. **DO** send an email to the maintainers with details
3. **DO** include steps to reproduce the vulnerability if possible
4. **DO** include any proof-of-concept code (if applicable)

### What to Include

Please include the following information in your report:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact of the vulnerability
- Suggested mitigation or fix (if known)
- Your contact information for follow-up

### Response Timeline

- **Acknowledgment**: We will acknowledge receipt of your report within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 5 business days
- **Resolution**: We aim to resolve critical vulnerabilities within 30 days
- **Disclosure**: After a fix is deployed, we will coordinate responsible disclosure

### Security Measures

This project implements several security measures:

#### Automated Security Scanning
- **Bandit**: Static security analysis for Python code
- **Safety**: Vulnerability scanning for Python dependencies
- **CodeQL**: GitHub's semantic code analysis
- **pip-audit**: Dependency vulnerability scanning
- **Dependabot**: Automated dependency updates

#### Secure Development Practices
- All subprocess calls use secure argument parsing (no `shell=True`)
- Jinja2 templates use `autoescape=True` to prevent XSS
- Input validation and sanitization
- Comprehensive test coverage (85%+)
- Continuous integration with security checks

#### Recent Security Fixes

**2024-07**: Fixed HIGH severity vulnerabilities reported by Prof. Shouvick Mondal, IIT Gandhinagar:
- **B602/CWE-78**: Subprocess shell injection vulnerability
- **B701/CWE-94**: Jinja2 autoescape disabled vulnerability

View all security issues: [Security Issues](https://github.com/nipunbatra/setwise/issues?q=is%3Aissue+label%3Asecurity)

## Security Best Practices for Users

When using Setwise:

1. **Input Validation**: Always validate user inputs before processing
2. **LaTeX Security**: Be cautious with user-provided LaTeX content
3. **File Permissions**: Ensure proper file permissions in output directories
4. **Dependencies**: Keep Python dependencies updated
5. **Environment**: Use virtual environments for isolation

## Acknowledgments

We acknowledge and thank:

- **Prof. Shouvick Mondal, IIT Gandhinagar** for security vulnerability research and reporting
- The Python security community for continuous improvement of security tools
- GitHub for providing CodeQL and security features

## Contact

For security-related inquiries, please contact the project maintainers through the repository's issue tracker (for non-sensitive issues) or via email for sensitive security matters.