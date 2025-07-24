# Setwise: Randomized LaTeX Quiz Generator

## Overview
Setwise is a Python-based quiz generation system that creates randomized PDF quizzes using LaTeX. It supports multiple question types, randomization features, and automatic answer key generation.

## Features

### Question Types Supported
- **Multiple Choice Questions (MCQs)**: With randomizable option order
- **Subjective Questions**: With templated variants using variables
- **LaTeX Mathematical Content**: Inline math ($x^2$) and display math (\[...\])
- **Tables**: Raw LaTeX table support
- **Figures**: PDF image inclusion from figures/ directory

### Randomization Capabilities
- MCQ option shuffling for each quiz set
- Subjective question variant selection
- Different quiz sets with same content pool

### Output Generation
- LaTeX source files (.tex)
- PDF compilation (via pdflatex)
- Answer keys (plaintext format)

## Architecture

### Directory Structure
```
setwise/
├── data/
│   └── questions.py          # Question definitions in Python
├── templates/
│   └── quiz_template.tex.jinja  # Jinja2 LaTeX template
├── figures/
│   └── *.pdf                 # Image assets for questions
├── output/
│   ├── quiz_set_N.tex
│   ├── quiz_set_N.pdf
│   └── answer_key_N.txt
├── main.py                   # Main quiz generation script
├── requirements.txt          # Python dependencies
└── SPECIFICATION.md          # This document
```

### Core Components

#### 1. Question Definition System (`data/questions.py`)
Questions are defined as Python data structures with the following formats:

**MCQ Format:**
```python
mcq = [
    {
        "question": r"What is the derivative of $f(x) = x^2$?",
        "options": [r"$x$", r"$2x$", r"$x^2$", r"$\frac{1}{x}$"],
        "answer": r"$2x$"
    }
]
```

**Subjective Format:**
```python
subjective = [
    {
        "template": r'''Calculate the mean of the values:
        \begin{center}
        \begin{tabular}{|c|c|c|}
        \hline
        A & B & C \\
        \hline
        {{ a }} & {{ b }} & {{ c }} \\
        \hline
        \end{tabular}
        \end{center}
        ''',
        "variables": [
            {"a": 10, "b": 20, "c": 30},
            {"a": 5, "b": 15, "c": 25}
        ]
    }
]
```

#### 2. Template System (`templates/quiz_template.tex.jinja`)
Uses Jinja2 templating to generate LaTeX documents with:
- Dynamic question insertion
- Loop-based question numbering
- Conditional content rendering
- Variable substitution for subjective questions

#### 3. Quiz Generation Engine (`main.py`)
Core functionality includes:
- Question loading and parsing
- Randomization algorithms
- Template rendering
- LaTeX compilation
- Answer key generation

## Technical Specifications

### Dependencies
- **Python 3.8+**
- **Jinja2**: Template rendering
- **Random**: Built-in randomization
- **LaTeX Distribution**: pdflatex for PDF generation

### Input Requirements
- Questions must use raw Python strings (`r'''...'''`) for LaTeX content
- LaTeX math can be inline (`$...$`) or display (`\[...\]`)
- Subjective questions use Jinja2 syntax (`{{ variable }}`)
- Images must be PDF format in `figures/` directory

### Output Specifications

**LaTeX Files:**
- Article document class
- Standard math and graphics packages
- 1-inch margins
- Enumerated lists for MCQ options

**Answer Keys:**
```
MCQ 1: Option B
MCQ 2: Option A  
Subjective 1: Answer = 20.0
```

## Usage Workflow

1. **Question Definition**: Add questions to `data/questions.py`
2. **Asset Management**: Place images in `figures/` as PDF files
3. **Generation**: Run `python main.py` to create quiz sets
4. **Compilation**: Automatic pdflatex compilation (optional)
5. **Distribution**: Use generated PDFs and answer keys

## Randomization Algorithm

### MCQ Randomization
- Options are shuffled using Fisher-Yates algorithm
- Answer tracking maintains correctness across shuffles
- Each quiz set has independent randomization

### Subjective Randomization
- One variant randomly selected per question per quiz set
- Variables substituted using Jinja2 rendering
- Deterministic selection for reproducible answer keys

## Extensibility Features

### Planned Enhancements
- **Image Support**: Enhanced figure handling and formats
- **Advanced Tables**: Dynamic table generation
- **Markdown Integration**: Markdown-to-LaTeX conversion
- **CLI Interface**: Command-line argument parsing
- **GUI Wrapper**: Graphical user interface
- **Export Formats**: Multiple output format support

### Configuration Options
- Number of quiz sets to generate
- Question pool selection
- Randomization seed control
- LaTeX compilation settings

## Quality Assurance

### Validation Features
- LaTeX syntax checking
- Answer key verification
- Template rendering validation
- File structure integrity checks

### Error Handling
- Missing figure detection
- LaTeX compilation error reporting
- Template variable validation
- Question format verification

## Performance Considerations
- Efficient randomization algorithms
- Lazy loading of large question pools
- Parallel PDF generation (future)
- Memory-efficient template rendering

## Security & Best Practices
- Input sanitization for LaTeX injection prevention
- File path validation
- Safe template rendering
- Secure random number generation