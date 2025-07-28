# Setwise Quick Start Guide

**For users experiencing installation or execution issues**

## Method 1: Recommended (Pip Installation)

This is the simplest and most reliable method:

```bash
# Create virtual environment
python3 -m venv setwise-env
source setwise-env/bin/activate  # On Windows: setwise-env\Scripts\activate

# Install Setwise directly
pip install git+https://github.com/nipunbatra/setwise.git

# Test installation
setwise welcome

# Generate your first quiz (without PDF to avoid LaTeX issues)
setwise generate --seed 42 --sets 2 --no-pdf

# Check output
ls output/
```

## Method 2: Direct Script (If Method 1 Fails)

If you prefer to run from source:

```bash
# Clone and setup
git clone https://github.com/nipunbatra/setwise.git
cd setwise

# Create virtual environment
python3 -m venv setwise-env
source setwise-env/bin/activate  # On Windows: setwise-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate figures first
python generate_figures.py

# Generate quiz WITHOUT PDF (avoids LaTeX issues)
python main.py --seed 42 --sets 2 --no-pdf

# Check output
ls output/
```

## Common Issues and Solutions

### Issue: Script hangs or doesn't exit

**Solution**: Use `--no-pdf` flag to skip LaTeX compilation:
```bash
# Instead of: python main.py --seed 42
# Use:
python main.py --seed 42 --no-pdf
```

### Issue: LaTeX compilation fails

**Cause**: Missing LaTeX installation or packages

**Quick Solution**: Skip PDF generation initially:
```bash
# Generate LaTeX files only
setwise generate --seed 42 --no-pdf
# or
python main.py --seed 42 --no-pdf
```

**Complete Solution**: Install LaTeX
```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-extra texlive-fonts-recommended

# macOS (with Homebrew)
brew install --cask mactex

# Or use TinyTeX (lighter)
wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh
```

### Issue: Import errors or missing modules

**Solution**: Ensure you're in the correct directory and environment:
```bash
# Make sure you're in the setwise directory
cd setwise

# Activate your virtual environment
source setwise-env/bin/activate

# Install/reinstall dependencies
pip install -r requirements.txt
```

## What You Should See

### Successful Generation (without PDF):
```
Using random seed: 42
Setwise Quiz Generator
========================================
Generating 2 quiz sets
Random seed: 42
MCQ questions per set: all
Subjective questions per set: all
PDF compilation: disabled
Output directory: output
========================================
Generating Quiz Set 1...
  ✓ LaTeX file saved: output/quiz_set_1.tex
  ✓ Answer key saved: output/answer_key_1.txt

Generating Quiz Set 2...
  ✓ LaTeX file saved: output/quiz_set_2.tex
  ✓ Answer key saved: output/answer_key_2.txt

Generated 2 quiz sets successfully!
Files saved in: /Users/your-username/setwise/output
```

### Expected Output Files:
```
output/
├── quiz_set_1.tex
├── quiz_set_2.tex
├── answer_key_1.txt
├── answer_key_2.txt
└── figures/
```

## Next Steps

Once you have LaTeX files generating successfully:

1. **View LaTeX files**: Open `.tex` files in any text editor
2. **Install LaTeX**: Follow the LaTeX installation guide above
3. **Generate PDFs**: Remove `--no-pdf` flag once LaTeX is working
4. **Explore features**: Try different templates, question counts, etc.

## Get Help

If you're still having issues:

1. **Check our documentation**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
2. **Report issues**: [GitHub Issues](https://github.com/nipunbatra/setwise/issues)
3. **Join discussions**: [GitHub Discussions](https://github.com/nipunbatra/setwise/discussions)

---

**TL;DR**: Use `--no-pdf` flag to avoid LaTeX issues: `python main.py --seed 42 --no-pdf`