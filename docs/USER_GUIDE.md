# User Guide

Complete guide to using Setwise for creating professional LaTeX quizzes.

## Table of Contents

- [Getting Started](#getting-started)
- [Command Line Interface](#command-line-interface)
- [Question Management](#question-management)
- [Quiz Generation](#quiz-generation)
- [Multi-Format Support](#multi-format-support)
- [Validation and Quality](#validation-and-quality)
- [Advanced Features](#advanced-features)
- [Best Practices](#best-practices)

## Getting Started

### First-Time User Workflow

If you're new to Setwise, follow this step-by-step guide:

```bash
# 1. Get welcomed and oriented
setwise welcome

# 2. Get format recommendation
setwise questions recommend-format

# 3. Create example questions in your preferred format
setwise questions create-examples --output-dir my-questions

# 4. Examine the example files
ls my-questions/
cat my-questions/sample_questions.yaml

# 5. Validate the examples with detailed feedback
setwise questions validate my-questions/sample_questions.yaml --verbose

# 6. Generate your first quiz
setwise generate --questions-file my-questions/sample_questions.yaml --sets 2

# 7. Check the output
ls output/
```

### Understanding the Output

After generation, you'll find:

```
output/
├── quiz_set_1.tex          # LaTeX source for set 1
├── quiz_set_1.pdf          # Compiled PDF for set 1
├── quiz_set_2.tex          # LaTeX source for set 2  
├── quiz_set_2.pdf          # Compiled PDF for set 2
├── answer_key_1.txt        # Answer key for set 1
├── answer_key_2.txt        # Answer key for set 2
└── figures/                # Generated figures (if any)
    ├── decision_tree.pdf
    └── neural_network.pdf
```

## Command Line Interface

### Core Commands

#### Generate Quizzes

```bash
# Basic generation
setwise generate

# With specific parameters
setwise generate --seed 123 --sets 3 --mcq 5 --subjective 2

# Use custom questions
setwise generate --questions-file my_questions.yaml --template compact

# Skip PDF compilation (LaTeX only)
setwise generate --no-pdf --sets 1

# Custom output directory
setwise generate --output-dir exam_2024 --sets 5
```

#### Question Management

```bash
# List available question libraries
setwise questions list

# Create sample questions
setwise questions create-sample physics_questions.py

# Get question statistics
setwise questions stats my_questions.yaml

# Search for questions in specific directories
setwise questions list --search-dirs ./subjects ./archives
```

#### Validation and Quality

```bash
# Basic validation
setwise questions validate questions.yaml

# Detailed validation with suggestions
setwise questions validate questions.yaml --verbose

# Show auto-fix suggestions
setwise questions validate questions.yaml --auto-suggest

# Preview LaTeX fixes
setwise questions fix-latex questions.yaml --dry-run

# Apply LaTeX fixes
setwise questions fix-latex questions.yaml
```

#### Format Operations

```bash
# Convert between formats
setwise questions convert input.py output.yaml
setwise questions convert data.csv questions.json

# Create examples in all formats
setwise questions create-examples --output-dir examples

# Get format recommendations
setwise questions recommend-format

# Compare format features
setwise questions format-comparison
```

#### Help and Information

```bash
# Welcome guide
setwise welcome

# List available templates
setwise list-templates

# LaTeX syntax help
setwise questions latex-help

# Workflow guidance
setwise questions workflow first-time
setwise questions workflow collaboration
setwise questions workflow bulk-editing
setwise questions workflow latex-heavy
```

### Command Options Reference

#### Generate Command Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--seed` | Random seed for reproducibility | Random | `--seed 42` |
| `--sets` | Number of quiz sets to generate | 3 | `--sets 5` |
| `--mcq` | Number of MCQ questions per set | All available | `--mcq 10` |
| `--subjective` | Number of subjective questions | All available | `--subjective 3` |
| `--template` | Template to use | default | `--template compact` |
| `--output-dir` | Output directory | ./output | `--output-dir exams` |
| `--no-pdf` | Skip PDF compilation | False | `--no-pdf` |
| `--questions-file` | Custom questions file | Built-in | `--questions-file my.yaml` |

#### Validation Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `--verbose` | Show detailed statistics and suggestions | `--verbose` |
| `--auto-suggest` | Show available auto-fix commands | `--auto-suggest` |

#### Fix-LaTeX Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `--dry-run` | Preview fixes without applying | `--dry-run` |
| `--output` | Output to different file | `--output fixed.yaml` |

## Question Management

### Creating Questions

#### Using Examples as Templates

```bash
# Create examples to use as templates
setwise questions create-examples --output-dir templates

# Copy and modify for your subject
cp templates/sample_questions.yaml physics_101.yaml
# Edit physics_101.yaml with your content
```

#### Starting from Scratch

```bash
# Create a basic template
setwise questions create-sample my_questions.py

# Validate as you build
setwise questions validate my_questions.py --verbose
```

### Question File Structure

All question formats follow the same logical structure with two main sections:

#### MCQ Questions
Each MCQ question requires:
- `question`: The question text
- `options`: List of answer choices  
- `answer`: The correct answer
- `marks`: Point value

#### Subjective Questions
Each subjective question requires:
- `question`: The question text
- `answer`: Sample or expected answer
- `marks`: Point value

**Template Support:**
- Use `template` instead of `question` for dynamic questions
- Provide `variables` array with different values
- Use `{{ variable_name }}` syntax in templates

### Question Quality Guidelines

#### Content Guidelines

**MCQ Questions:**
- Write clear, unambiguous questions
- Provide 3-5 realistic options
- Ensure only one clearly correct answer
- Avoid "all of the above" or "none of the above"
- Make distractors plausible but clearly wrong

**Subjective Questions:**
- Start with action verbs (Explain, Calculate, Derive, Compare)
- Specify the expected depth of answer
- Include point allocation hints in complex questions
- Provide comprehensive sample answers

#### Technical Guidelines

**LaTeX Usage:**
- Use `$...$` for inline math: `$x^2 + y^2 = z^2$`
- Use `$$...$$` for display math: `$$\int_0^1 f(x) dx$$`
- Escape special characters: `\%`, `\$`, `\&`
- Use proper chemical formulas: `H$_2$O`, `CO$_2$`

**Formatting:**
- Keep questions concise but complete
- Use consistent mark allocation
- Include units in numerical problems
- Use proper mathematical notation

### Validation Workflow

#### Step-by-Step Validation

```bash
# 1. Basic syntax validation
setwise questions validate my_questions.yaml

# 2. Get improvement suggestions
setwise questions validate my_questions.yaml --verbose

# 3. Preview automatic fixes
setwise questions fix-latex my_questions.yaml --dry-run

# 4. Apply fixes if appropriate
setwise questions fix-latex my_questions.yaml

# 5. Re-validate after fixes
setwise questions validate my_questions.yaml --verbose

# 6. Check statistics
setwise questions stats my_questions.yaml
```

#### Understanding Validation Output

**Valid Files:**
```
✅ Valid: Valid questions file with 5 MCQ and 3 subjective questions

💡 Suggestions for improvement (2 found):
   1. 💡 Chemistry formula 'H2O' should use subscripts: H$_2$O
   2. 💡 Consider adding more answer options for MCQ diversity

📊 Quick Stats:
   📝 Total questions: 8
   🔢 MCQ: 5 (15 marks)
   📖 Subjective: 3 (25 marks)
   🏆 Total marks: 40
```

**Invalid Files:**
```
❌ Invalid: MCQ question 2 LaTeX errors: Math expression 'x^2' should be in math mode: $x^2$

🔍 Troubleshooting tips:
   • Check file format and syntax
   • Ensure all required fields are present
   • Validate LaTeX expressions
   • Run: setwise questions latex-help for LaTeX syntax help
```

## Quiz Generation

### Basic Generation

#### Simple Generation
```bash
# Generate with defaults (3 sets, all questions)
setwise generate

# Specify number of sets
setwise generate --sets 5

# Use specific random seed for reproducibility
setwise generate --seed 42 --sets 3
```

#### Controlling Question Selection
```bash
# Generate specific numbers of questions
setwise generate --mcq 5 --subjective 2 --sets 3

# Generate only MCQ questions
setwise generate --mcq 10 --subjective 0

# Generate only subjective questions  
setwise generate --mcq 0 --subjective 5
```

### Template Selection

#### Available Templates

```bash
# List all templates with descriptions
setwise list-templates
```

**Default Template:**
- Professional single-column layout
- Color-coded sections
- Suitable for formal exams
- 3-4 pages typical

**Compact Template:**
- Two-column space-efficient layout
- Multi-column MCQ options
- Ideal for printing and paper saving
- 1-2 pages typical

**Minimal Template:**
- Clean black and white design
- High contrast for readability
- Perfect for simple assessments
- 1-2 pages typical

#### Using Templates

```bash
# Use specific template
setwise generate --template compact --sets 2

# Compare templates
setwise generate --template default --sets 1 --output-dir default_output
setwise generate --template compact --sets 1 --output-dir compact_output
setwise generate --template minimal --sets 1 --output-dir minimal_output
```

### Custom Questions

#### Using Your Own Questions

```bash
# Create your questions file
setwise questions create-sample chemistry_quiz.py

# Edit the file with your content
# ... add your questions ...

# Validate before generation
setwise questions validate chemistry_quiz.py --verbose

# Generate quiz with your questions
setwise generate --questions-file chemistry_quiz.py --sets 3
```

#### Subject-Specific Examples

Download and use subject examples:

```bash
# Physics examples
curl -o physics.py https://raw.githubusercontent.com/nipunbatra/setwise/main/examples/physics_questions.py
setwise generate --questions-file physics.py --template compact

# Chemistry examples  
curl -o chemistry.py https://raw.githubusercontent.com/nipunbatra/setwise/main/examples/chemistry_questions.py
setwise generate --questions-file chemistry.py --template default

# Mathematics examples
curl -o math.py https://raw.githubusercontent.com/nipunbatra/setwise/main/examples/mathematics_questions.py
setwise generate --questions-file math.py --template minimal
```

### Output Management

#### Organizing Output

```bash
# Use descriptive output directories
setwise generate --output-dir midterm_exam_2024 --sets 5
setwise generate --output-dir quiz_week_3 --sets 2 --mcq 5

# Date-based organization
setwise generate --output-dir "exam_$(date +%Y%m%d)" --sets 3
```

#### Batch Generation

```bash
# Generate multiple versions for different classes
for class in cs101 cs102 cs201; do
    setwise generate --seed $RANDOM --sets 3 --output-dir "${class}_midterm"
done

# Generate with different templates
for template in default compact minimal; do
    setwise generate --template $template --sets 1 --output-dir "sample_${template}"
done
```

## Multi-Format Support

### Format Selection Guide

#### Choose Your Format

**YAML (.yaml)** - Recommended for most users
```yaml
mcq:
  - question: "What is the speed of light?"
    options: ["3×10^8 m/s", "3×10^6 m/s", "3×10^10 m/s"]
    answer: "3×10^8 m/s"
    marks: 2
```

**JSON (.json)** - For developers and web integration
```json
{
  "mcq": [
    {
      "question": "What is the speed of light?",
      "options": ["3×10^8 m/s", "3×10^6 m/s", "3×10^10 m/s"],
      "answer": "3×10^8 m/s",
      "marks": 2
    }
  ]
}
```

**CSV (.csv)** - For spreadsheet users
```csv
type,question,option1,option2,option3,answer,marks
mcq,"What is the speed of light?","3×10^8 m/s","3×10^6 m/s","3×10^10 m/s","3×10^8 m/s",2
```

**Python (.py)** - For advanced users
```python
mcq = [
    {
        "question": "What is the speed of light?",
        "options": ["3×10^8 m/s", "3×10^6 m/s", "3×10^10 m/s"],
        "answer": "3×10^8 m/s",
        "marks": 2
    }
]
```

### Format Conversion

#### Converting Between Formats

```bash
# Python to YAML (most common)
setwise questions convert questions.py questions.yaml

# YAML to JSON (for web apps)
setwise questions convert questions.yaml questions.json

# CSV to Python (for advanced features)
setwise questions convert questions.csv questions.py

# Any format to any format
setwise questions convert input.FORMAT output.FORMAT
```

#### Batch Conversion

```bash
# Convert all Python files to YAML
for file in *.py; do
    setwise questions convert "$file" "${file%.py}.yaml"
done

# Create all formats from master file
setwise questions convert master.py master.yaml
setwise questions convert master.py master.json
setwise questions convert master.py master.csv
```

### Format-Specific Tips

#### YAML Best Practices
- Use consistent indentation (2 spaces recommended)
- Quote strings containing special characters
- Use literal style (`|`) for multi-line text
- Validate with `setwise questions validate file.yaml --verbose`

#### JSON Best Practices  
- Use double quotes for all strings
- Validate JSON syntax with online tools
- Use proper escaping for LaTeX: `"x^{2}"`
- Pretty-print for readability: `python -m json.tool file.json`

#### CSV Best Practices
- Quote fields containing commas or quotes
- Use consistent column ordering
- Escape quotes by doubling: `"She said ""Hello"""`
- Open in spreadsheet software for bulk editing

#### Python Best Practices
- Use raw strings for LaTeX: `r"$x^2 + y^2 = z^2$"`
- Leverage template variables for dynamic questions
- Add comments for documentation
- Use proper Python formatting: `black questions.py`

## Validation and Quality

### Enhanced Validation Features

#### Smart Suggestions

Setwise provides intelligent suggestions for common issues:

```bash
setwise questions validate questions.yaml --verbose
```

**Common suggestions:**
- Chemistry formulas needing subscripts
- Math expressions missing dollar signs
- Physics units that can be improved
- Overly long questions that should be split
- Missing question marks
- Formatting inconsistencies

#### Auto-Fix Capabilities

```bash
# Preview what would be fixed
setwise questions fix-latex questions.yaml --dry-run

# Apply automatic fixes
setwise questions fix-latex questions.yaml
```

**Automatic fixes include:**
- `H2O` → `H$_2$O`
- `x^2` → `$x^{2}$`
- `45 degrees` → `45°`
- `%` → `\%`
- Unescaped special characters

### Quality Metrics

#### Statistical Analysis

```bash
setwise questions stats questions.yaml
```

**Output includes:**
- Total questions and marks
- MCQ vs subjective distribution
- File size and complexity
- Template variable usage
- Mark allocation analysis

#### Comprehensive Quality Testing

```bash
# Run full quality test suite
python test_quality.py
```

**Tests include:**
- Format validation across all types
- Conversion integrity testing
- Performance benchmarking
- LaTeX compilation testing
- Error handling verification

## Advanced Features

### Template Variables

#### Dynamic Questions with Variables

```python
subjective = [
    {
        "template": "Calculate the kinetic energy of a {{ mass }} kg object moving at {{ velocity }} m/s.",
        "variables": [
            {"mass": 10, "velocity": 5, "answer": "KE = ½mv² = ½(10)(25) = 125 J"},
            {"mass": 2, "velocity": 10, "answer": "KE = ½mv² = ½(2)(100) = 100 J"},
            {"mass": 5, "velocity": 8, "answer": "KE = ½mv² = ½(5)(64) = 160 J"}
        ],
        "marks": 5
    }
]
```

#### Benefits of Templates
- Generate multiple variants from one question
- Ensure consistent difficulty across sets
- Reduce question writing workload
- Maintain parallel forms for fair assessment

### Figure Generation

#### TikZ Diagrams

```bash
# Generate figures before quiz creation
setwise generate-figures
```

**Automatically generates:**
- Decision tree diagrams
- Neural network architectures
- Support vector machine illustrations
- Mathematical plots and graphs

#### Custom Figures

Add your own figures to the `figures/` directory:
- `.tikz` files for TikZ diagrams
- `.pdf` files for external graphics
- Reference in questions as `\includegraphics{figures/my_diagram.pdf}`

### API Integration

#### Python API Usage

```python
from setwise import QuizGenerator, TemplateManager

# Create generator with custom settings
generator = QuizGenerator(
    output_dir="api_output",
    questions_file="my_questions.yaml"
)

# Generate quizzes programmatically
success = generator.generate_quizzes(
    num_sets=5,
    num_mcq=10,
    num_subjective=3,
    template_name="compact",
    seed=12345,
    compile_pdf=True
)

# Check available templates
tm = TemplateManager()
templates = tm.list_templates()
print(templates)
```

#### Batch Processing

```python
import os
from pathlib import Path

# Process multiple question files
question_files = Path("questions/").glob("*.yaml")

for qfile in question_files:
    output_dir = f"output/{qfile.stem}"
    generator = QuizGenerator(
        output_dir=output_dir,
        questions_file=str(qfile)
    )
    generator.generate_quizzes(num_sets=3, seed=42)
```

## Best Practices

### Content Development

#### Question Writing
1. **Start with learning objectives** - What should students demonstrate?
2. **Use action verbs** - Calculate, explain, compare, analyze
3. **Provide clear context** - Include necessary background information
4. **Test your questions** - Try solving them yourself
5. **Get feedback** - Have colleagues review before use

#### LaTeX Usage
1. **Be consistent** - Use the same notation throughout
2. **Test compilation** - Always generate PDFs to check formatting
3. **Use raw strings** - Especially in Python format
4. **Follow conventions** - Mathematical typesetting standards
5. **Validate early** - Check LaTeX syntax as you write

### Workflow Organization

#### File Organization
```
my_course/
├── questions/
│   ├── midterm_1.yaml
│   ├── midterm_2.yaml
│   └── final_exam.yaml
├── output/
│   ├── midterm_1_2024/
│   ├── midterm_2_2024/
│   └── final_2024/
└── templates/
    └── custom_template.tex.jinja
```

#### Version Control
```bash
# Initialize git repository
git init
git add questions/ templates/
git commit -m "Initial question bank"

# Track changes
git add questions/midterm_1.yaml
git commit -m "Add thermodynamics questions"

# Tag releases
git tag -a v1.0 -m "Midterm 1 questions finalized"
```

#### Collaborative Workflow
1. **Use YAML format** - Most readable for team collaboration
2. **Establish conventions** - Naming, marking, style guides
3. **Regular validation** - Check quality before merging
4. **Peer review** - Have others validate content
5. **Backup frequently** - Use cloud storage or git

### Performance Optimization

#### Large Question Banks
```bash
# Use specific question counts to reduce generation time
setwise generate --mcq 20 --subjective 5 --sets 10

# Generate LaTeX only for faster iteration
setwise generate --no-pdf --sets 5

# Use consistent seeds for reproducible testing
setwise generate --seed 42 --sets 1
```

#### Resource Management
- Keep question files under 1000 questions for best performance
- Use template variables to create variation without bloat
- Generate figures once and reuse
- Clean up old output directories regularly

### Quality Assurance

#### Testing Workflow
1. **Validate questions** - Use verbose validation
2. **Test generation** - Generate small test sets
3. **Review output** - Check PDFs for formatting
4. **Verify answers** - Ensure answer keys are correct
5. **Get feedback** - Use with students and collect input

#### Continuous Improvement
```bash
# Regular quality checks
setwise questions validate questions.yaml --verbose --auto-suggest

# Performance monitoring
python test_quality.py

# Security updates
pip install --upgrade git+https://github.com/nipunbatra/setwise.git
```

---

**Next Steps:**
- Explore [Templates Guide](TEMPLATES.md) for customization options
- Learn [Format Details](FORMATS.md) for advanced format features
- Check [LaTeX Guide](LATEX.md) for mathematical typesetting
- Review [Troubleshooting](TROUBLESHOOTING.md) for common issues