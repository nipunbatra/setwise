# 🎯 Setwise: Professional LaTeX Quiz Generator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![LaTeX](https://img.shields.io/badge/LaTeX-Required-green.svg)](https://www.latex-project.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](#testing)

> **Transform your question banks into beautiful, randomized LaTeX quiz sets with professional formatting and advanced templating capabilities.**

## 🌟 **Why Setwise?**

- **🎲 Smart Randomization** - Questions and MCQ options automatically shuffled
- **📝 Template Magic** - Create variants using Jinja2 templates (MCQ + Subjective!)
- **🎨 Professional Output** - Beautiful LaTeX formatting with multiple themes
- **⚡ Lightning Fast** - Generate hundreds of unique quiz variations instantly
- **🔧 Simple Setup** - Python-only format, no complex configurations
- **📊 Comprehensive** - MCQ, subjective, multi-part questions with individual scoring

## 🚀 **Quick Start**

### Installation
```bash
pip install setwise
# or for development
git clone https://github.com/nipunbatra/setwise.git
cd setwise && pip install -e .
```

### 30-Second Example
```python
# Create questions.py
quiz_metadata = {
    "title": "My First Quiz",
    "duration": "60 minutes",
    "total_marks": 20
}

mcq = [
    {
        "question": r"What is machine learning?",
        "options": [
            r"Programming with explicit rules",
            r"Learning patterns from data",
            r"Statistical analysis only",
            r"Database management"
        ],
        "answer": r"Learning patterns from data",
        "marks": 2
    }
]

subjective = [
    {
        "question": r"Explain supervised vs unsupervised learning.",
        "answer": r"Supervised uses labeled data, unsupervised finds hidden patterns.",
        "marks": 8
    }
]
```

```bash
# Generate 5 unique quiz sets
setwise generate --questions-file questions.py --sets 5 --template default
```

**Output:** 5 beautifully formatted PDF quiz sets with randomized question order! 🎉

## ⭐ **Key Features**

### 🎲 **Smart Randomization**
- Question order randomized across quiz sets
- MCQ options shuffled automatically  
- Answer keys updated with correct positions
- Seed-based reproducible randomization

### 📝 **Advanced Templates** ⭐ NEW!
```python
# Templates work for BOTH MCQ and subjective questions!
mcq = [
    {
        "template": r"What is {{ a }} + {{ b }}?",
        "options": [r"{{ a+b-1 }}", r"{{ a+b }}", r"{{ a+b+1 }}", r"{{ a*b }}"],
        "answer": r"{{ a+b }}",
        "variables": [
            {"a": 3, "b": 4},
            {"a": 7, "b": 2}, 
            {"a": 5, "b": 6}
        ],
        "marks": 2
    }
]
```

### 🎨 **Professional Themes**
| Theme | Description | Best For |
|-------|-------------|----------|
| `default` | Clean, professional single-column | Formal exams |
| `compact` | Space-efficient two-column | Quick assessments |
| `academic` | Traditional academic format | University exams |
| `minimal` | Clean black & white | Print-friendly |

### 📊 **Easy Quiz Metadata**
```python
quiz_metadata = {
    "title": "Advanced Machine Learning Quiz",
    "subject": "Computer Science",
    "course_code": "CS 4780",
    "instructor": "Prof. Smith", 
    "semester": "Fall 2024",
    "duration": "120 minutes",
    "total_marks": 100,
    "instructions": ["Show all work", "Use proper notation"],
    "exam_date": "December 15, 2024",
    "institution": "Cornell University"
}
```

## 📖 **Documentation**

- **🚀 [Quick Start Guide](docs/quickstart.md)** - Get up and running in minutes
- **📝 [Writing Questions](docs/questions.md)** - Complete question format reference
- **🎨 [Templates & Themes](docs/templates.md)** - Customization and styling
- **⚡ [Advanced Features](docs/advanced.md)** - Templating, randomization, and more
- **🛠️ [CLI Reference](docs/cli.md)** - All command-line options
- **🐍 [Python API](docs/api.md)** - Programmatic usage
- **🎓 [Examples Gallery](examples/)** - Real-world question banks

## 🎯 **Enhanced Features** ⭐ **NEW in v2.0!**

### ✅ **What's New:**
1. **Python-only format** - Simplified from 5 formats to just `.py`
2. **MCQ templates** - Now fully supported (was blocked before!)
3. **Easy metadata** - Clean `quiz_metadata` dictionary
4. **Multi-part questions** - Enhanced with individual marks
5. **Comprehensive docs** - Complete guides and examples

### 📝 **Template Examples**

#### MCQ with Variables
```python
{
    "template": r"Calculate: {{ base }}^{{ exponent }} = ?",
    "options": [
        r"{{ base ** exponent }}",      # Correct
        r"{{ base * exponent }}",       # Common mistake
        r"{{ base + exponent }}",       # Wrong operation  
        r"{{ (base + 1) ** exponent }}" # Close but wrong
    ],
    "answer": r"{{ base ** exponent }}",
    "variables": [
        {"base": 2, "exponent": 3},  # 2³ = 8
        {"base": 3, "exponent": 4},  # 3⁴ = 81
        {"base": 5, "exponent": 2}   # 5² = 25
    ],
    "marks": 3
}
```

#### Multi-Part Questions
```python
{
    "question": r"Analyze the dataset performance:",
    "parts": [
        {
            "question": r"Calculate the accuracy with TP=85, TN=90, FP=10, FN=15.",
            "answer": r"Accuracy = (TP+TN)/(TP+TN+FP+FN) = (85+90)/(85+90+10+15) = 175/200 = 87.5%",
            "marks": 3
        },
        {
            "question": r"What does this accuracy tell us about model performance?",
            "answer": r"87.5% accuracy indicates good but not excellent performance. Need to examine precision/recall for class-specific performance.",
            "marks": 4
        }
    ],
    "marks": 7
}
```

## 🛠️ **CLI Usage**

```bash
# Basic generation
setwise generate --questions-file questions.py --sets 3

# With custom template and output
setwise generate --questions-file quiz.py --template compact --sets 5 --output-dir exams/

# Reproducible generation with seed
setwise generate --questions-file quiz.py --seed 42 --sets 3

# List available templates
setwise list-templates

# Validate questions before generation
setwise questions validate questions.py
```

## 🐍 **Python API**

```python
from setwise import QuizGenerator

# Create generator
gen = QuizGenerator(
    questions_file="questions.py",
    output_dir="output/"
)

# Access metadata and questions
print(f"Quiz: {gen.quiz_metadata['title']}")
print(f"MCQ: {len(gen.mcq)}, Subjective: {len(gen.subjective)}")

# Generate quiz sets
success = gen.generate_quizzes(
    num_sets=5,
    template_name="default",
    compile_pdf=True,
    seed=42
)
```

## 🎓 **Examples**

### Mathematics
```python
quiz_metadata = {"title": "Calculus I - Derivatives"}

mcq = [
    {
        "template": r"Find $\frac{d}{dx}[{{ function }}]$",
        "options": [r"${{ derivative }}$", r"${{ wrong1 }}$", r"${{ wrong2 }}$", r"${{ wrong3 }}$"],
        "answer": r"${{ derivative }}$",
        "variables": [
            {"function": "x^3", "derivative": "3x^2", "wrong1": "x^4", "wrong2": "3x", "wrong3": "x^2"},
            {"function": r"\sin(x)", "derivative": r"\cos(x)", "wrong1": r"-\cos(x)", "wrong2": r"\sin(x)", "wrong3": r"\tan(x)"}
        ],
        "marks": 3
    }
]
```

### Computer Science
```python
mcq = [
    {
        "template": r"A binary tree with {{ n }} nodes has maximum height of:",
        "options": [r"{{ n-1 }}", r"{{ n }}", r"$\log_2({{ n }})$", r"${{ n }}^2$"],
        "answer": r"{{ n-1 }}",
        "variables": [{"n": 7}, {"n": 15}, {"n": 31}],
        "marks": 2
    }
]
```

### Physics
```python
mcq = [
    {
        "template": r"A ball dropped from {{ height }}m hits ground with velocity:",
        "options": [
            r"$\sqrt{2g \times {{ height }}}$ ≈ {{ velocity:.1f }} m/s",
            r"$g \times {{ height }}$ = {{ height * 9.8 }} m/s", 
            r"${{ height }} \times 2$ = {{ height * 2 }} m/s",
            r"$\sqrt{{{ height }}}$ = {{ height**0.5:.1f }} m/s"
        ],
        "answer": r"$\sqrt{2g \times {{ height }}}$ ≈ {{ velocity:.1f }} m/s",
        "variables": [
            {"height": 20, "velocity": 19.8},
            {"height": 45, "velocity": 29.7}
        ],
        "marks": 3
    }
]
```

## 📊 **Before vs After Comparison**

| Feature | Before v2.0 | After v2.0 ✨ |
|---------|-------------|---------------|
| **Input Formats** | 5 formats (.py, .yaml, .json, .csv, .md) | **1 format (.py only)** |
| **MCQ Templates** | ❌ Blocked by validation | **✅ Fully supported** |
| **Quiz Metadata** | ❌ No standard way | **✅ Easy dict format** |
| **Multi-part Questions** | ⚠️ Basic support | **✅ Enhanced with marks** |
| **Documentation** | ⚠️ Basic README | **✅ Comprehensive guides** |
| **Complexity** | 🔴 High learning curve | **🟢 Simple and intuitive** |

## 🔍 **Migration from v1.x**

Existing `.py` files work without changes! New features are opt-in:

```python
# v1.x (still works)
mcq = [{"question": "...", "options": [...], "answer": "...", "marks": 2}]

# v2.0 enhancements (optional)
quiz_metadata = {"title": "My Quiz"}  # Add metadata
mcq = [{"template": "...", "variables": [...]}]  # Use templates
```

## 🚨 **Requirements**

- **Python 3.8+**
- **LaTeX distribution** (TeX Live, MiKTeX, or MacTeX)
- **Git** (for development)

## 🤝 **Contributing**

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 **License**

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 **Acknowledgments**

- LaTeX community for beautiful typesetting
- Jinja2 for powerful templating
- Contributors and users for feedback and improvements

---

<div align="center">

**Made with ❤️ by the Setwise Community**

[⭐ Star us on GitHub](https://github.com/nipunbatra/setwise) • [📖 Documentation](docs/) • [🐛 Report Issues](https://github.com/nipunbatra/setwise/issues) • [💬 Discussions](https://github.com/nipunbatra/setwise/discussions)

</div>