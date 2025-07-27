# Setwise Question File Formats

Setwise supports multiple question file formats to accommodate different user preferences and workflows. Choose the format that works best for your needs!

## 📋 Supported Formats

| Format | Extension | Best For | Pros | Cons |
|--------|-----------|----------|------|------|
| **YAML** | `.yaml`, `.yml` | Educators, readable config | Human-readable, clean syntax, version control friendly | Indentation sensitive |
| **JSON** | `.json` | Web integration, APIs | Standard format, tool support | Less readable for humans |
| **CSV** | `.csv` | Spreadsheet users | Excel/Sheets compatibility, bulk editing | Limited formatting options |
| **Markdown** | `.md` | Documentation, GitHub | Great for documentation, preview-friendly | Basic structure only |
| **Python** | `.py` | Programmers, advanced users | Full programming power, templating | Requires Python knowledge |

## 🎯 Quick Start Examples

### YAML Format (Recommended for Educators)
```yaml
metadata:
  title: Physics Quiz Questions
  format: setwise-yaml
  version: '1.0'

mcq:
  - question: "What is the speed of light in vacuum?"
    options:
      - "299,792,458 m/s"
      - "300,000,000 m/s"
      - "3.00 × 10^8 m/s"
    answer: "299,792,458 m/s"
    marks: 2

subjective:
  - question: "Explain Newton's first law of motion."
    answer: "An object at rest stays at rest unless acted upon by an external force."
    marks: 5
```

### JSON Format (Web-Friendly)
```json
{
  "metadata": {
    "title": "Quiz Questions",
    "format": "setwise-json"
  },
  "mcq": [
    {
      "question": "What is 2 + 2?",
      "options": ["3", "4", "5", "6"],
      "answer": "4",
      "marks": 1
    }
  ],
  "subjective": [
    {
      "question": "Explain gravity.",
      "answer": "Gravity is a fundamental force of attraction.",
      "marks": 5
    }
  ]
}
```

### CSV Format (Spreadsheet-Friendly)
```csv
type,question,option1,option2,option3,option4,option5,answer,marks
MCQ,What is the capital of France?,London,Berlin,Paris,Madrid,,Paris,1
Subjective,Explain photosynthesis.,,,,,,The process by which plants convert sunlight into energy.,5
```

### Markdown Format (Documentation-Friendly)
```markdown
# Quiz Questions

## MCQ Questions

**1. What is the capital of France?**

- London
- Berlin  
- Paris
- Madrid

*Answer:* Paris
*Marks:* 1

## Subjective Questions

**1. Explain photosynthesis.**

The process by which plants convert sunlight into energy using chlorophyll.

*Marks:* 5
```

### Python Format (Advanced Users)
```python
"""
Advanced Python format with templating support
"""

mcq = [
    {
        "question": r"What is $E = mc^2$?",
        "options": [
            r"Einstein's mass-energy equivalence",
            r"Newton's second law",
            r"Conservation of energy",
            r"Relativity principle"
        ],
        "answer": r"Einstein's mass-energy equivalence",
        "marks": 2
    }
]

subjective = [
    {
        "template": r"Calculate kinetic energy with mass {{ mass }} kg and velocity {{ velocity }} m/s",
        "variables": [
            {"mass": 10, "velocity": 5, "answer": "KE = ½mv² = 125 J"},
            {"mass": 2, "velocity": 10, "answer": "KE = ½mv² = 100 J"}
        ],
        "marks": 3
    }
]
```

## 🔄 Format Conversion

Convert between any supported formats:

```bash
# Convert Python to YAML (most readable)
setwise questions convert physics_questions.py physics_questions.yaml

# Convert YAML to CSV (for spreadsheet editing)
setwise questions convert physics_questions.yaml physics_questions.csv

# Convert CSV to JSON (for web integration)
setwise questions convert physics_questions.csv physics_questions.json

# Convert JSON to Markdown (for documentation)
setwise questions convert physics_questions.json physics_questions.md
```

## 📚 Command Reference

### Create Example Files
```bash
# Create sample files in all formats
setwise questions create-examples --output-dir my_examples

# This creates:
# my_examples/sample_questions.py
# my_examples/sample_questions.yaml
# my_examples/sample_questions.json
# my_examples/sample_questions.csv
# my_examples/sample_questions.md
```

### Validation
```bash
# Validate any format
setwise questions validate questions.yaml
setwise questions validate questions.json
setwise questions validate questions.csv
setwise questions validate questions.md
setwise questions validate questions.py
```

### Quiz Generation
```bash
# Generate quiz from any format
setwise generate --questions-file questions.yaml --sets 3
setwise generate --questions-file questions.json --sets 2
setwise generate --questions-file questions.csv --sets 1
```

## 🎨 Best Practices by Format

### YAML (.yaml) - **Recommended for Most Users**
✅ **Pros:**
- Most human-readable format
- Great for version control (Git)
- Supports comments and documentation
- Clean, indented structure

📝 **Tips:**
- Use consistent indentation (2 spaces recommended)
- Quote strings with special characters
- Use `|` for multi-line text
- Add metadata section for documentation

### JSON (.json) - **Best for Web Integration**
✅ **Pros:**
- Standard web format
- Excellent tool support
- Easy to parse programmatically
- No indentation sensitivity

📝 **Tips:**
- Use proper escaping for LaTeX (`\\` becomes `\\\\`)
- Validate JSON syntax with tools
- Consider pretty-printing for readability

### CSV (.csv) - **Best for Bulk Editing**
✅ **Pros:**
- Excel/Google Sheets compatibility
- Great for bulk question creation
- Easy collaboration with non-technical users
- Simple tabular format

📝 **Tips:**
- Keep LaTeX simple in CSV
- Use type column to distinguish MCQ/Subjective
- Empty cells for unused option columns
- Quote fields containing commas

### Markdown (.md) - **Best for Documentation**
✅ **Pros:**
- GitHub-friendly
- Great for documentation
- Human-readable
- Easy to write and edit

📝 **Tips:**
- Follow the exact format structure
- Use consistent heading levels
- Include answer and marks sections
- Great for README files

### Python (.py) - **Best for Advanced Users**
✅ **Pros:**
- Full programming capabilities
- Template variables for dynamic questions
- Complex LaTeX expressions
- Conditional logic support

📝 **Tips:**
- Use raw strings (r"") for LaTeX
- Leverage template variables for variants
- Add documentation strings
- Follow Python naming conventions

## 🚨 Common Issues and Solutions

### YAML Issues
```yaml
# ❌ Wrong: Unquoted special characters
question: What is x^2 + y^2?

# ✅ Correct: Quote LaTeX expressions
question: "What is $x^2 + y^2$?"
```

### JSON Issues
```json
// ❌ Wrong: Single quotes and comments not allowed
{
  'question': 'What is x^2?' // This is wrong
}

// ✅ Correct: Double quotes, no comments
{
  "question": "What is $x^2$?"
}
```

### CSV Issues
```csv
# ❌ Wrong: Commas in unquoted fields
question,options,answer
What is Paris, France?,London;Paris;Rome,Paris

# ✅ Correct: Quote fields with commas
question,option1,option2,option3,answer
"What is Paris, France?",London,Paris,Rome,Paris
```

## 🎯 Format Selection Guide

**Choose YAML if:**
- You're an educator or non-programmer
- You want human-readable files
- You use version control (Git)
- You need to add comments/documentation

**Choose JSON if:**
- You're building web applications
- You need API integration
- You use automated tools
- You prefer strict syntax

**Choose CSV if:**
- You work with spreadsheets (Excel/Sheets)
- You need bulk question creation
- You collaborate with non-technical users
- You prefer tabular data format

**Choose Markdown if:**
- You're documenting questions
- You use GitHub/GitLab
- You want readable documentation
- You need simple, clean format

**Choose Python if:**
- You're a programmer
- You need template variables
- You want complex LaTeX expressions
- You need conditional logic

## 🔗 Integration Examples

### GitHub Workflow
```bash
# Store questions in YAML for readability
git add physics_questions.yaml
git commit -m "Add physics questions"

# Convert to other formats as needed
setwise questions convert physics_questions.yaml physics_questions.json
```

### Spreadsheet Workflow
```bash
# Export to CSV for Excel editing
setwise questions convert questions.yaml questions.csv

# Edit in Excel/Google Sheets
# Import back after editing
setwise questions convert questions.csv questions.yaml
```

### Documentation Workflow
```bash
# Convert to Markdown for documentation
setwise questions convert questions.yaml README_questions.md

# Include in your project README or wiki
```

## 📖 LaTeX Support Across Formats

All formats support LaTeX mathematical expressions:

```
# Mathematical expressions
$x^2 + y^2 = z^2$
$\frac{a}{b} + \sqrt{c}$

# Chemical formulas  
H$_2$O + CO$_2$

# Physics equations
$F = ma$, $E = mc^2$

# Complex expressions
$\lim_{x \to 0} \frac{\sin x}{x} = 1$
```

## 🎓 Getting Started Workflow

1. **Create sample files**: `setwise questions create-examples`
2. **Choose your format**: Start with YAML if unsure
3. **Edit questions**: Use your preferred editor
4. **Validate**: `setwise questions validate your_questions.yaml`
5. **Generate quiz**: `setwise generate --questions-file your_questions.yaml`
6. **Convert as needed**: Use `setwise questions convert` for other formats

For more help: `setwise questions --help` or `setwise questions latex-help`