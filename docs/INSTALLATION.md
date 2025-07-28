# Installation Guide

This guide covers all installation methods and requirements for Setwise.

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Installation Options](#installation-options)
- [LaTeX Setup](#latex-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Supported Platforms
- **Windows** 10/11
- **macOS** 10.15+
- **Linux** (Ubuntu 18.04+, CentOS 7+, Debian 10+)

### Python Requirements
- **Python** 3.8 or higher
- **pip** (latest version recommended)

### Optional Dependencies
- **LaTeX** distribution (for PDF generation)
- **poppler-utils** (for PDF preview generation)
- **Git** (for development installation)

## Quick Installation

### For Regular Users

```bash
# Install latest stable version
pip install git+https://github.com/nipunbatra/setwise.git

# Test installation
setwise welcome
```

### For Web Interface Users

```bash
# Install with web interface support
pip install git+https://github.com/nipunbatra/setwise.git[web]

# Launch web interface
streamlit run setwise_web.py
```

### For Developers

```bash
# Clone repository
git clone https://github.com/nipunbatra/setwise.git
cd setwise

# Install in development mode
pip install -e .[dev,security]

# Run tests
python -m pytest
```

## Installation Options

### Standard Installation

Installs core Setwise functionality:

```bash
pip install git+https://github.com/nipunbatra/setwise.git
```

**Includes:**
- Core quiz generation engine
- Command-line interface
- All question formats (YAML, JSON, CSV, Markdown, Python)
- LaTeX validation and auto-fix
- Basic templates

### Web Interface Installation

Adds Streamlit-based web interface:

```bash
pip install git+https://github.com/nipunbatra/setwise.git[web]
```

**Additional features:**
- Interactive web interface
- Live question editor
- Visual validation feedback
- Point-and-click generation

### Development Installation

For contributors and advanced users:

```bash
pip install git+https://github.com/nipunbatra/setwise.git[dev,security]
```

**Additional tools:**
- Testing frameworks (pytest, coverage)
- Code formatting (black, flake8)
- Security scanning (bandit, safety)
- Documentation tools

### Virtual Environment (Recommended)

Using a virtual environment isolates Setwise from other Python packages:

```bash
# Create virtual environment
python -m venv setwise-env

# Activate (Linux/macOS)
source setwise-env/bin/activate

# Activate (Windows)
setwise-env\Scripts\activate

# Install Setwise
pip install git+https://github.com/nipunbatra/setwise.git

# Deactivate when done
deactivate
```

## LaTeX Setup

LaTeX is required for PDF generation. Choose one option:

### Option 1: TinyTeX (Recommended)

Lightweight, automatically manages packages:

**Linux/macOS:**
```bash
wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh
```

**Windows:**
1. Download installer from https://yihui.org/tinytex/
2. Run installer as administrator
3. Restart command prompt

### Option 2: TeX Live (Full)

Complete LaTeX distribution:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install texlive-full
```

**CentOS/RHEL:**
```bash
sudo yum install texlive-collection-*
```

**macOS (Homebrew):**
```bash
brew install --cask mactex
```

**Windows:**
Download from https://tug.org/texlive/

### Option 3: MiKTeX

User-friendly LaTeX distribution:

**Windows:**
Download from https://miktex.org/download

**Linux:**
Follow instructions at https://miktex.org/howto/install-miktex-unx

### LaTeX Package Requirements

Setwise automatically installs required packages on first use:

- `geometry` - Page layout
- `xcolor` - Color support  
- `tikz` - Diagram generation
- `amsmath, amssymb` - Mathematical symbols
- `fancyhdr` - Headers and footers
- `multicol` - Multi-column layout

## Verification

### Test Basic Installation

```bash
# Check Setwise is installed
setwise --help

# Test welcome command
setwise welcome

# Create example questions
setwise questions create-examples --output-dir test

# Validate examples
setwise questions validate test/sample_questions.yaml
```

### Test LaTeX Generation

```bash
# Generate LaTeX files only (no PDF)
setwise generate --no-pdf --sets 1 --output-dir test-output

# Generate with PDF (requires LaTeX)
setwise generate --sets 1 --output-dir test-output-pdf
```

### Test All Features

```bash
# Run comprehensive tests
python test_quality.py
```

## Troubleshooting

### Common Issues

#### "setwise: command not found"

**Cause:** Setwise not in PATH or virtual environment not activated

**Solutions:**
```bash
# Check if installed
pip list | grep setwise

# Reinstall if missing
pip install git+https://github.com/nipunbatra/setwise.git

# Use full path if needed
python -m setwise.cli --help
```

#### "pdflatex: command not found"

**Cause:** LaTeX not installed or not in PATH

**Solutions:**
```bash
# Check LaTeX installation
pdflatex --version

# Add to PATH (Linux/macOS)
echo 'export PATH="/usr/local/texlive/2023/bin/x86_64-linux:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Reinstall LaTeX if needed
```

#### "Permission denied" errors

**Cause:** Insufficient permissions

**Solutions:**
```bash
# Install for current user only
pip install --user git+https://github.com/nipunbatra/setwise.git

# Or use virtual environment
python -m venv setwise-env
source setwise-env/bin/activate
pip install git+https://github.com/nipunbatra/setwise.git
```

#### Import errors with development installation

**Cause:** Missing development dependencies

**Solutions:**
```bash
# Install all development dependencies
pip install -e .[dev,security,web]

# Or install missing packages individually
pip install pytest black flake8 bandit safety streamlit
```

### Platform-Specific Issues

#### Windows

**PowerShell execution policy:**
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Long path support:**
Enable long path support in Windows settings or registry.

#### macOS

**Homebrew permissions:**
```bash
# Fix Homebrew permissions
sudo chown -R $(whoami) $(brew --prefix)/*
```

**Command Line Tools:**
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

#### Linux

**Missing system dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3-devel python3-pip
```

### Getting Help

If you encounter issues not covered here:

1. **Check existing issues:** [GitHub Issues](https://github.com/nipunbatra/setwise/issues)
2. **Search discussions:** [GitHub Discussions](https://github.com/nipunbatra/setwise/discussions)
3. **Create new issue:** Include installation method, OS, Python version, and full error message
4. **Review logs:** Use `setwise --verbose` for detailed output

### Advanced Troubleshooting

#### Enable debug logging

```bash
# Set environment variable for detailed logging
export SETWISE_DEBUG=1
setwise generate --sets 1
```

#### Test specific components

```bash
# Test LaTeX validation
setwise questions latex-help

# Test format conversion
setwise questions convert test/sample_questions.py test_output.yaml

# Test templates
setwise list-templates
```

#### Clean installation

```bash
# Uninstall completely
pip uninstall setwise

# Clear pip cache
pip cache purge

# Reinstall fresh
pip install git+https://github.com/nipunbatra/setwise.git
```

## Next Steps

After successful installation:

1. **Read the [User Guide](USER_GUIDE.md)** for comprehensive usage instructions
2. **Explore [Templates](TEMPLATES.md)** to understand output options
3. **Learn [Formats](FORMATS.md)** to choose the right question format
4. **Check [Examples](../examples/)** for sample question libraries

---

**Need help?** Join our [community discussions](https://github.com/nipunbatra/setwise/discussions) or [report an issue](https://github.com/nipunbatra/setwise/issues).