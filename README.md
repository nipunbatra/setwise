# Setwise: Professional LaTeX Quiz Generator

[![CI Status](https://img.shields.io/github/actions/workflow/status/nipunbatra/setwise/ci.yml?branch=main&label=CI)](https://github.com/nipunbatra/setwise/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/nipunbatra/setwise/branch/main/graph/badge.svg)](https://codecov.io/gh/nipunbatra/setwise)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Quality: Good](https://img.shields.io/badge/quality-good%20(85.7%25)-brightgreen)](docs/QUALITY.md)

A professional Python-based quiz generation system that creates beautiful, randomized PDF quizzes with comprehensive LaTeX support, multi-format question libraries, and intelligent validation.

## Quick Preview

| Default Template | Compact Template | Minimal Template |
|------------------|------------------|------------------|
| ![Default](assets/images/default_set1_page-1.png) | ![Compact](assets/images/compact_set1_page-1.png) | ![Minimal](assets/images/minimal_set1_page-1.png) |
| Professional layout | Space-efficient | Clean & minimal |

**[View all template samples →](docs/TEMPLATES.md)**

## Key Features

- **Professional Output** - Beautiful LaTeX PDFs with multiple templates
- **Multi-Format Support** - YAML, JSON, CSV, Markdown, Python question files
- **Smart Validation** - Enhanced LaTeX checking with auto-fix capabilities
- **Intelligent Guidance** - Interactive help system for all skill levels
- **Secure & Tested** - 86% test coverage, comprehensive security scanning
- **Cross-Platform** - Works on Windows, macOS, and Linux

## Quick Start

### Easy Installation (Recommended)

```bash
# Create virtual environment
python3 -m venv setwise-env
source setwise-env/bin/activate  # Windows: setwise-env\Scripts\activate

# Install Setwise
pip install git+https://github.com/nipunbatra/setwise.git

# Generate your first quiz (no LaTeX required)
setwise generate --seed 42 --no-pdf
```

### Alternative: Run from Source

If you prefer to clone the repository:

```bash
git clone https://github.com/nipunbatra/setwise.git
cd setwise
python3 -m venv setwise-env
source setwise-env/bin/activate
pip install -r requirements.txt

# Generate quiz without PDF to avoid LaTeX issues
python main.py --seed 42 --no-pdf
```

**Having issues?** See [QUICKSTART.md](QUICKSTART.md) for troubleshooting.

**[Complete installation guide →](docs/INSTALLATION.md)**

## Usage Examples

```bash
# Generate 3 quiz sets with specific counts
setwise generate --seed 123 --sets 3 --mcq 5 --subjective 2

# Use different template
setwise generate --template compact --sets 2

# Validate questions with smart suggestions
setwise questions validate my_questions.yaml --verbose

# Auto-fix common LaTeX issues
setwise questions fix-latex my_questions.yaml

# Convert between formats
setwise questions convert questions.py questions.yaml
```

**[Complete user guide →](docs/USER_GUIDE.md)**

## Multi-Format Question Support

Setwise supports five different formats to match your workflow:

| Format | Best For | Example Command |
|--------|----------|-----------------|
| **YAML** | Educators, readable format | `setwise questions create-examples --format yaml` |
| **JSON** | Developers, web apps | `setwise questions create-examples --format json` |
| **CSV** | Spreadsheet users | `setwise questions create-examples --format csv` |
| **Markdown** | Documentation | `setwise questions create-examples --format markdown` |
| **Python** | Advanced users | `setwise questions create-examples --format python` |

**[Format tutorial and best practices →](docs/FORMATS.md)**

## Documentation

### User Documentation
- **[Installation Guide](docs/INSTALLATION.md)** - Complete setup instructions
- **[User Guide](docs/USER_GUIDE.md)** - Comprehensive usage documentation
- **[Templates Guide](docs/TEMPLATES.md)** - Template showcase and customization
- **[Formats Tutorial](docs/FORMATS.md)** - Multi-format support and best practices
- **[Quality Assurance](docs/QUALITY.md)** - Testing results and quality metrics

### Developer Documentation
- **[API Reference](docs/API.md)** - Python API documentation
- **[Development Guide](docs/DEVELOPMENT.md)** - Contributing and development setup
- **[Architecture](docs/ARCHITECTURE.md)** - Technical design and components

### Advanced Topics
- **[LaTeX Best Practices](docs/LATEX.md)** - LaTeX syntax and validation
- **[Security](docs/SECURITY.md)** - Security features and considerations
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## Contributing

We welcome contributions! Please see our [Development Guide](docs/DEVELOPMENT.md) for details on:

- Setting up the development environment
- Running tests and quality checks
- Code style and conventions
- Submitting pull requests

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- **Issues**: [Report bugs and request features](https://github.com/nipunbatra/setwise/issues)
- **Discussions**: [Community Q&A](https://github.com/nipunbatra/setwise/discussions)
- **Documentation**: [Complete documentation](docs/)

---

**Made for educators and students worldwide**