# Multi-Format Question Support

Comprehensive guide to Setwise's five question formats and how to choose the right one for your workflow.

## Table of Contents

- [Format Overview](#format-overview)
- [Format Comparison](#format-comparison)
- [YAML Format](#yaml-format)
- [JSON Format](#json-format)
- [CSV Format](#csv-format)
- [Markdown Format](#markdown-format)
- [Python Format](#python-format)
- [Format Conversion](#format-conversion)
- [Best Practices](#best-practices)

## Format Overview

Setwise supports five different question formats to accommodate different user preferences, workflows, and technical requirements:

| Format | Extension | Primary Users | Strengths |
|--------|-----------|---------------|-----------|
| **YAML** | `.yaml`, `.yml` | Educators, content creators | Human-readable, version control friendly |
| **JSON** | `.json` | Developers, web applications | Standard format, excellent tool support |
| **CSV** | `.csv` | Spreadsheet users, bulk editors | Excel compatibility, familiar interface |
| **Markdown** | `.md` | Documentation writers | GitHub integration, readable |
| **Python** | `.py` | Programmers, advanced users | Full programming capabilities |

### Choosing Your Format

**Quick Decision Tree:**

1. **Are you comfortable with programming?**
   - Yes → Consider **Python** for maximum flexibility
   - No → Continue to question 2

2. **Do you primarily use spreadsheets (Excel/Sheets)?**
   - Yes → **CSV** is perfect for you
   - No → Continue to question 3

3. **Do you need web/API integration?**
   - Yes → **JSON** for standard compatibility
   - No → Continue to question 4

4. **Do you work with GitHub or version control?**
   - Yes → **YAML** or **Markdown** for best experience
   - No → **YAML** for general use

**Get personalized recommendation:**
```bash
setwise questions recommend-format
```

## Format Comparison

### Feature Matrix

| Feature | YAML | JSON | CSV | Markdown | Python |
|---------|------|------|-----|----------|--------|
| **Readability** | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★★★★ | ★★★☆☆ |
| **Tool Support** | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★★ |
| **Learning Curve** | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★☆☆☆ |
| **Version Control** | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ★★★★★ | ★★★★★ |
| **Bulk Editing** | ★★★☆☆ | ★★☆☆☆ | ★★★★★ | ★★☆☆☆ | ★★★☆☆ |
| **Advanced Features** | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★☆☆☆ | ★★★★★ |
| **Web Integration** | ★★★☆☆ | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ |

### Comparison Commands

```bash
# See detailed comparison table
setwise questions format-comparison

# Create examples in all formats to compare
setwise questions create-examples --output-dir format_comparison

# Compare file sizes and readability
ls -la format_comparison/sample_questions.*
```

## YAML Format

**Best for:** Educators, content creators, team collaboration

YAML (YAML Ain't Markup Language) provides the best balance of readability and functionality for most users.

### Basic Structure

```yaml
mcq:
  - question: "What is the capital of France?"
    options:
      - "London"
      - "Berlin" 
      - "Paris"
      - "Madrid"
    answer: "Paris"
    marks: 1

  - question: "Calculate the area of a circle with radius $r = 5$ cm."
    options:
      - "$25\\pi$ cm²"
      - "$10\\pi$ cm²" 
      - "$5\\pi$ cm²"
      - "$\\pi$ cm²"
    answer: "$25\\pi$ cm²"
    marks: 2

subjective:
  - question: "Explain Newton's first law of motion."
    answer: "An object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force."
    marks: 5

  - question: "Derive the quadratic formula from $ax^2 + bx + c = 0$."
    answer: |
      Starting with $ax^2 + bx + c = 0$:
      
      1. Divide by $a$: $x^2 + \frac{b}{a}x + \frac{c}{a} = 0$
      2. Complete the square: $x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = \left(\frac{b}{2a}\right)^2 - \frac{c}{a}$
      3. Simplify: $\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}$
      4. Take square root: $x + \frac{b}{2a} = \pm\frac{\sqrt{b^2-4ac}}{2a}$
      5. Solve for $x$: $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$
    marks: 8
```

### YAML Best Practices

#### Indentation
```yaml
# Use 2 spaces for indentation (consistent)
mcq:
  - question: "Question text"
    options:
      - "Option 1"
      - "Option 2"
    answer: "Option 1"
    marks: 1
```

#### String Handling
```yaml
# Quote strings with special characters
question: "What is 50% of 100?"

# Use literal style for multi-line text
answer: |
  This is a multi-line answer.
  
  It preserves line breaks and formatting.
  Perfect for detailed explanations.

# Use folded style for wrapped text
question: >
  This is a very long question that would normally
  wrap across multiple lines but will be folded
  into a single line.
```

#### LaTeX in YAML
```yaml
# Use quotes for LaTeX expressions
question: "Calculate $\\int_0^1 x^2 dx$"

# Raw strings work well for complex LaTeX
answer: |
  $$\int_0^1 x^2 dx = \left[\frac{x^3}{3}\right]_0^1 = \frac{1}{3}$$
```

### YAML Validation

```bash
# Validate YAML syntax and content
setwise questions validate questions.yaml --verbose

# Common YAML issues and fixes
# 1. Indentation errors
# 2. Missing quotes for special characters
# 3. Inconsistent list formatting
```

## JSON Format

**Best for:** Developers, web applications, API integration

JSON provides excellent tool support and is the standard for web applications.

### Basic Structure

```json
{
  "mcq": [
    {
      "question": "What is the capital of France?",
      "options": ["London", "Berlin", "Paris", "Madrid"],
      "answer": "Paris",
      "marks": 1
    },
    {
      "question": "Calculate the area of a circle with radius $r = 5$ cm.",
      "options": ["$25\\pi$ cm²", "$10\\pi$ cm²", "$5\\pi$ cm²", "$\\pi$ cm²"],
      "answer": "$25\\pi$ cm²",
      "marks": 2
    }
  ],
  "subjective": [
    {
      "question": "Explain Newton's first law of motion.",
      "answer": "An object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.",
      "marks": 5
    },
    {
      "question": "Derive the quadratic formula from $ax^2 + bx + c = 0$.",
      "answer": "Starting with $ax^2 + bx + c = 0$:\\n\\n1. Divide by $a$: $x^2 + \\frac{b}{a}x + \\frac{c}{a} = 0$\\n2. Complete the square...\\n5. Solve for $x$: $x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$",
      "marks": 8
    }
  ]
}
```

### JSON Best Practices

#### Formatting
```bash
# Pretty-print JSON for readability
python -m json.tool questions.json > formatted_questions.json

# Validate JSON syntax
python -c "import json; json.load(open('questions.json'))"
```

#### String Escaping
```json
{
  "question": "What is the derivative of $f(x) = x^2$?",
  "answer": "The derivative is $f'(x) = 2x$ using the power rule.",
  "note": "Use double quotes for all strings and escape internal quotes with \\\"
}
```

#### LaTeX in JSON
```json
{
  "question": "Solve the equation $ax^2 + bx + c = 0$",
  "answer": "Using the quadratic formula: $x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$",
  "explanation": "Note the double backslashes for LaTeX commands in JSON"
}
```

### JSON Tools and Integration

#### Command Line Tools
```bash
# Validate JSON
jq . questions.json > /dev/null

# Extract specific data
jq '.mcq | length' questions.json  # Count MCQ questions
jq '.mcq[0].question' questions.json  # Get first question

# Transform data
jq '.mcq | map(select(.marks > 1))' questions.json  # Filter by marks
```

#### Web Integration
```javascript
// Load questions in web application
fetch('questions.json')
  .then(response => response.json())
  .then(data => {
    console.log(`Loaded ${data.mcq.length} MCQ questions`);
    console.log(`Loaded ${data.subjective.length} subjective questions`);
  });
```

## CSV Format

**Best for:** Spreadsheet users, bulk editing, data analysis

CSV format excels at bulk operations and familiar spreadsheet interfaces.

### Basic Structure

```csv
type,question,option1,option2,option3,option4,answer,marks,explanation
mcq,"What is the capital of France?","London","Berlin","Paris","Madrid","Paris",1,"Basic geography question"
mcq,"Calculate the area of a circle with radius $r = 5$ cm.","$25\pi$ cm²","$10\pi$ cm²","$5\pi$ cm²","$\pi$ cm²","$25\pi$ cm²",2,"Area formula: $A = \pi r^2$"
subjective,"Explain Newton's first law of motion.",,,,,An object at rest stays at rest...,5,"Fundamental physics concept"
subjective,"Derive the quadratic formula.",,,,,Starting with $ax^2 + bx + c = 0$...,8,"Mathematical derivation"
```

### CSV Best Practices

#### Field Handling
```csv
# Quote fields containing commas
question,"In the equation F = ma, what does 'a' represent?","acceleration","mass","force","velocity","acceleration",1

# Escape quotes by doubling them
question,"Einstein said ""Imagination is more important than knowledge""","True","False",,,True,2

# Handle multi-line content with proper quoting
subjective,"Explain photosynthesis","Plants convert CO2 and H2O into glucose using sunlight:
6CO2 + 6H2O + light → C6H12O6 + 6O2",5
```

#### LaTeX in CSV
```csv
type,question,answer,marks
mcq,"What is $\frac{d}{dx}(x^2)$?","$2x$",2
subjective,"Derive $\int x^2 dx$","$\int x^2 dx = \frac{x^3}{3} + C$",3
```

### Spreadsheet Workflow

#### Excel/Google Sheets Tips
1. **Use Data Validation** - Create dropdown lists for answer options
2. **Conditional Formatting** - Highlight incomplete questions
3. **Formulas** - Calculate total marks automatically
4. **Templates** - Create question templates for consistency
5. **Collaboration** - Share sheets for team editing

#### Bulk Operations
```bash
# Count questions by type
cut -d',' -f1 questions.csv | sort | uniq -c

# Extract only MCQ questions
grep "^mcq," questions.csv > mcq_only.csv

# Calculate total marks (assuming marks in column 7)
awk -F',' '{sum += $7} END {print "Total marks:", sum}' questions.csv
```

### CSV Validation and Conversion

```bash
# Validate CSV format
setwise questions validate questions.csv --verbose

# Convert to other formats for advanced features
setwise questions convert questions.csv questions.yaml
setwise questions convert questions.csv questions.py
```

## Markdown Format

**Best for:** Documentation, GitHub integration, content sharing

Markdown format provides excellent readability and integrates well with documentation workflows.

### Basic Structure

```markdown
# Quiz Questions

## Multiple Choice Questions

### Question 1 (1 mark)
**Question:** What is the capital of France?

**Options:**
- A) London
- B) Berlin
- C) Paris
- D) Madrid

**Answer:** C) Paris

### Question 2 (2 marks)
**Question:** Calculate the area of a circle with radius $r = 5$ cm.

**Options:**
- A) $25\pi$ cm²
- B) $10\pi$ cm²
- C) $5\pi$ cm²
- D) $\pi$ cm²

**Answer:** A) $25\pi$ cm²

## Subjective Questions

### Question 1 (5 marks)
**Question:** Explain Newton's first law of motion.

**Answer:** An object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.

### Question 2 (8 marks)
**Question:** Derive the quadratic formula from $ax^2 + bx + c = 0$.

**Answer:**
Starting with $ax^2 + bx + c = 0$:

1. Divide by $a$: $x^2 + \frac{b}{a}x + \frac{c}{a} = 0$
2. Complete the square: $x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = \left(\frac{b}{2a}\right)^2 - \frac{c}{a}$
3. Simplify: $\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}$
4. Take square root: $x + \frac{b}{2a} = \pm\frac{\sqrt{b^2-4ac}}{2a}$
5. Solve for $x$: $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$
```

### Markdown Best Practices

#### GitHub Integration
- Use proper heading hierarchy for navigation
- Include table of contents for long documents
- Use code blocks for LaTeX formatting examples
- Add metadata in YAML front matter

#### LaTeX in Markdown
```markdown
# LaTeX expressions work naturally
Inline math: The formula $E = mc^2$ is famous.

Display math:
$$\int_0^1 x^2 dx = \frac{1}{3}$$

# Use code blocks for complex LaTeX
```latex
\begin{align}
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \epsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{align}
```

#### Documentation Workflow
```bash
# Preview Markdown files
grip questions.md  # GitHub-flavored markdown preview

# Convert to other formats
pandoc questions.md -o questions.pdf
pandoc questions.md -o questions.html
```

## Python Format

**Best for:** Programmers, advanced users, dynamic content

Python format provides maximum flexibility and programming capabilities.

### Basic Structure

```python
# Multiple Choice Questions
mcq = [
    {
        "question": r"What is the capital of France?",
        "options": [r"London", r"Berlin", r"Paris", r"Madrid"],
        "answer": r"Paris",
        "marks": 1
    },
    {
        "question": r"Calculate the area of a circle with radius $r = 5$ cm.",
        "options": [r"$25\pi$ cm²", r"$10\pi$ cm²", r"$5\pi$ cm²", r"$\pi$ cm²"],
        "answer": r"$25\pi$ cm²",
        "marks": 2
    }
]

# Subjective Questions
subjective = [
    {
        "question": r"Explain Newton's first law of motion.",
        "answer": r"An object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.",
        "marks": 5
    },
    {
        "template": r"Calculate the kinetic energy of a {{ mass }} kg object moving at {{ velocity }} m/s.",
        "variables": [
            {"mass": 10, "velocity": 5, "answer": r"KE = ½mv² = ½(10)(25) = 125 J"},
            {"mass": 2, "velocity": 10, "answer": r"KE = ½mv² = ½(2)(100) = 100 J"},
            {"mass": 5, "velocity": 8, "answer": r"KE = ½mv² = ½(5)(64) = 160 J"}
        ],
        "marks": 3
    }
]
```

### Advanced Python Features

#### Template Variables
```python
# Dynamic questions with multiple variants
subjective = [
    {
        "template": r"A projectile is launched at {{ angle }}° with initial velocity {{ velocity }} m/s. Calculate the maximum height.",
        "variables": [
            {
                "angle": 30,
                "velocity": 20,
                "answer": r"$h_{max} = \frac{v_0^2 \sin^2\theta}{2g} = \frac{20^2 \sin^2(30°)}{2 \times 9.8} = 5.1$ m"
            },
            {
                "angle": 45,
                "velocity": 15,
                "answer": r"$h_{max} = \frac{v_0^2 \sin^2\theta}{2g} = \frac{15^2 \sin^2(45°)}{2 \times 9.8} = 5.7$ m"
            }
        ],
        "marks": 4
    }
]
```

#### Programmatic Generation
```python
import math

# Generate questions programmatically
def generate_circle_questions():
    questions = []
    for radius in [2, 3, 5, 7, 10]:
        area = math.pi * radius ** 2
        questions.append({
            "question": f"What is the area of a circle with radius {radius} cm?",
            "options": [
                f"${radius**2}\\pi$ cm²",
                f"${2*radius}\\pi$ cm²", 
                f"${radius}\\pi$ cm²",
                f"${radius**2//2}\\pi$ cm²"
            ],
            "answer": f"${radius**2}\\pi$ cm²",
            "marks": 2
        })
    return questions

# Add generated questions
mcq.extend(generate_circle_questions())
```

#### Comments and Documentation
```python
# Physics Questions - Mechanics Unit
# Created: 2024-01-15
# Last Modified: 2024-01-20
# Total Questions: 15 MCQ + 8 Subjective
# Estimated Time: 90 minutes

# Constants used in calculations
G = 9.8  # acceleration due to gravity (m/s²)
C = 3e8  # speed of light (m/s)

mcq = [
    # Kinematics questions (Questions 1-5)
    {
        "question": f"What is the acceleration due to gravity?",
        "options": [f"{G} m/s²", "10 m/s²", "9.0 m/s²", "8.8 m/s²"],
        "answer": f"{G} m/s²",
        "marks": 1,
        "topic": "kinematics",
        "difficulty": "easy"
    }
]
```

### Python Best Practices

#### Raw Strings for LaTeX
```python
# Use raw strings to avoid escaping issues
question = r"Solve $\int_0^1 \frac{1}{1+x^2} dx$"

# Instead of escaped strings
question = "Solve $\\int_0^1 \\frac{1}{1+x^2} dx$"
```

#### Code Organization
```python
# Organize questions by topic
kinematics_mcq = [...]
dynamics_mcq = [...]
energy_mcq = [...]

# Combine sections
mcq = kinematics_mcq + dynamics_mcq + energy_mcq

# Add metadata
metadata = {
    "course": "Physics 101",
    "unit": "Mechanics", 
    "created": "2024-01-15",
    "total_marks": sum(q["marks"] for q in mcq + subjective)
}
```

#### Validation and Testing
```python
# Validate question structure
def validate_questions():
    required_fields = ["question", "answer", "marks"]
    mcq_fields = required_fields + ["options"]
    
    for i, q in enumerate(mcq):
        for field in mcq_fields:
            assert field in q, f"MCQ {i+1} missing field: {field}"
        assert len(q["options"]) >= 2, f"MCQ {i+1} needs at least 2 options"
        assert q["answer"] in q["options"], f"MCQ {i+1} answer not in options"
    
    for i, q in enumerate(subjective):
        for field in required_fields:
            assert field in q, f"Subjective {i+1} missing field: {field}"

# Run validation
if __name__ == "__main__":
    validate_questions()
    print(f"✅ Validation passed: {len(mcq)} MCQ, {len(subjective)} subjective")
```

## Format Conversion

### Conversion Commands

```bash
# Convert between any formats
setwise questions convert input.py output.yaml
setwise questions convert input.yaml output.json
setwise questions convert input.json output.csv
setwise questions convert input.csv output.md
setwise questions convert input.md output.py

# Batch conversion
for file in *.py; do
    setwise questions convert "$file" "${file%.py}.yaml"
done
```

### Conversion Best Practices

#### Data Integrity
```bash
# Verify conversion integrity
setwise questions convert original.py converted.yaml
setwise questions stats original.py > original_stats.txt
setwise questions stats converted.yaml > converted_stats.txt
diff original_stats.txt converted_stats.txt
```

#### Format-Specific Considerations

**Python → YAML:**
- Template variables preserved
- Comments lost
- Programmatic logic lost

**CSV → Python:**
- Gains template capabilities
- Better LaTeX handling
- Programmatic features available

**YAML → JSON:**
- Maintains structure
- Better web integration
- Loses readability

### Lossy vs Lossless Conversions

#### Lossless Conversions
- YAML ↔ JSON
- Python → YAML (without logic)
- CSV → YAML/JSON

#### Lossy Conversions
- Python → CSV (loses templates)
- Any format → Markdown (structural info lost)
- Markdown → Any format (formatting lost)

## Best Practices

### Format Selection Strategy

#### By Team Size
- **Individual use:** Any format based on preference
- **Small team (2-5):** YAML for readability
- **Large team (5+):** JSON for tooling or CSV for spreadsheets
- **Mixed skill levels:** YAML with conversion to others as needed

#### By Project Phase
- **Development:** Python for flexibility
- **Review:** YAML or Markdown for readability  
- **Production:** JSON for web apps, CSV for data analysis
- **Archive:** YAML for long-term storage

#### By Integration Needs
- **Web applications:** JSON primary, others as source
- **Documentation:** Markdown with conversion from YAML
- **Data analysis:** CSV with conversion from other formats
- **Version control:** YAML or Python for best diff visibility

### Migration Strategies

#### Gradual Migration
```bash
# Start with examples in target format
setwise questions create-examples --format yaml

# Convert high-priority content first
setwise questions convert critical_questions.py critical_questions.yaml

# Test thoroughly before full migration
setwise generate --questions-file critical_questions.yaml --sets 1 --no-pdf

# Migrate in batches
find . -name "*.py" -exec setwise questions convert {} {}.yaml \;
```

#### Parallel Formats
```bash
# Maintain multiple formats during transition
setwise questions convert master.py master.yaml
setwise questions convert master.py master.json
setwise questions convert master.py master.csv

# Keep all in sync with master
./sync_formats.sh master.py
```

### Quality Assurance

#### Cross-Format Validation
```bash
# Validate across all formats
for format in py yaml json csv md; do
    echo "Validating $format format..."
    setwise questions validate "questions.$format" --verbose
done
```

#### Automated Testing
```bash
# Test conversion roundtrips where possible
setwise questions convert test.yaml test.json
setwise questions convert test.json test_roundtrip.yaml
diff test.yaml test_roundtrip.yaml
```

---

**Next Steps:**
- Choose your format using `setwise questions recommend-format`
- Create examples with `setwise questions create-examples --output-dir examples`
- Read the [User Guide](USER_GUIDE.md) for detailed usage instructions
- Check [LaTeX Guide](LATEX.md) for mathematical typesetting