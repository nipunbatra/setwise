# 🚀 Setwise Enhanced Features Guide

This document outlines all the new enhancements to the Setwise quiz generator, making it more powerful and user-friendly.

## 📋 Summary of Enhancements

1. **✅ Python-only format (.py)** - Simplified from multiple formats  
2. **✅ Templated MCQ questions** - Now supported (previously blocked)
3. **✅ Easy quiz metadata specification** - Clean YAML-like syntax in Python
4. **✅ Multi-part questions** - Enhanced support with individual marks
5. **✅ Comprehensive examples** - Demonstrating all features

## 🔧 1. Python-Only Format (.py)

**Before:** Supported .py, .yaml, .json, .csv, .md files  
**After:** Only .py files for simplicity and reliability

### Benefits:
- **Simpler codebase** - No format conversion complexity
- **Better validation** - Direct Python syntax checking  
- **Faster loading** - No parsing overhead
- **IDE support** - Full syntax highlighting and error checking

### Usage:
```bash
# Only .py files accepted
setwise generate --questions-file my_questions.py --template default --sets 3
```

## 🎯 2. Templated MCQ Questions (NEW!)

**Before:** Only subjective questions could use templates  
**After:** Both MCQ and subjective questions support templates

### MCQ Template Syntax:
```python
mcq = [
    {
        "template": r"What is {{ a }} + {{ b }}?",
        "options": [
            r"{{ a + b - 1 }}", 
            r"{{ a + b }}", 
            r"{{ a + b + 1 }}", 
            r"{{ a * b }}"
        ],
        "answer": r"{{ a + b }}",
        "variables": [
            {"a": 3, "b": 4},
            {"a": 5, "b": 7},
            {"a": 8, "b": 2}
        ],
        "marks": 2
    }
]
```

### Template Features:
- **Jinja2 expressions** - Full Python expression support
- **Random selection** - One variable set chosen per question
- **Option rendering** - Templates in both questions and options
- **Answer validation** - Rendered answers verified against options

## 📊 3. Easy Quiz Metadata Specification

**Before:** No standardized way to specify quiz information  
**After:** Clean `quiz_metadata` dictionary

### Metadata Syntax:
```python
quiz_metadata = {
    "title": "Machine Learning Fundamentals Quiz",
    "subject": "Computer Science",
    "course_code": "CS 4780", 
    "instructor": "Prof. Smith",
    "semester": "Fall 2024",
    "duration": "90 minutes",
    "total_marks": 50,
    "instructions": [
        "Answer all questions clearly and concisely",
        "Show your work for partial credit",
        "Use proper mathematical notation where applicable"
    ],
    "exam_date": "December 15, 2024",
    "institution": "Cornell University"
}
```

### Supported Fields:
| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Quiz title |
| `subject` | string | Subject name |
| `course_code` | string | Course identifier |
| `instructor` | string | Instructor name |
| `semester` | string | Academic term |
| `duration` | string | Time limit |
| `total_marks` | int | Maximum score |
| `instructions` | list | List of instructions |
| `exam_date` | string | Exam date |
| `institution` | string | School/university name |

## 📝 4. Multi-Part Questions

Enhanced support for questions with multiple sub-parts, each with individual marks.

### Multi-Part Syntax:
```python
subjective = [
    {
        "question": r"Analyze the performance of a logistic regression model:",
        "parts": [
            {
                "question": r"Given training accuracy 95% and validation 60%, what problem exists?",
                "answer": r"This indicates overfitting...",
                "marks": 3
            },
            {
                "question": r"Suggest three techniques to address this problem.",
                "answer": r"1) Regularization 2) Cross-validation 3) Feature selection...",
                "marks": 6
            },
            {
                "question": r"Evaluate the outcome after applying your suggestions.",
                "answer": r"The improvement shows better generalization...",
                "marks": 4
            }
        ],
        "marks": 13  # Total marks for all parts
    }
]
```

### Templated Multi-Part Questions:
```python
subjective = [
    {
        "template": r"Consider a dataset with {{ n_samples }} samples:",
        "parts": [
            {
                "question": r"Calculate the class imbalance ratio with {{ pos_samples }} positive examples.",
                "answer": r"Ratio = {{ pos_samples }}/{{ neg_samples }} = {{ pos_samples/neg_samples:.1f }}",
                "marks": 3
            },
            {
                "question": r"Suggest appropriate evaluation metrics.",
                "answer": r"Use precision, recall, F1-score instead of accuracy...",
                "marks": 4
            }
        ],
        "variables": [
            {"n_samples": 1000, "pos_samples": 200, "neg_samples": 800},
            {"n_samples": 500, "pos_samples": 50, "neg_samples": 450}
        ],
        "marks": 7
    }
]
```

## 📚 5. Complete Example Structure

Here's a comprehensive example showing all features:

```python
#!/usr/bin/env python3
"""Complete Setwise Enhanced Example"""

# Quiz metadata
quiz_metadata = {
    "title": "Advanced Topics Quiz",
    "subject": "Computer Science",
    "duration": "120 minutes",
    "total_marks": 100
}

# MCQ questions (regular + templated)
mcq = [
    # Regular MCQ
    {
        "question": r"What is machine learning?",
        "options": [
            r"Programming computers explicitly",
            r"Learning from data without explicit programming", 
            r"Using only statistical methods",
            r"Manual data analysis"
        ],
        "answer": r"Learning from data without explicit programming",
        "marks": 2
    },
    
    # Templated MCQ
    {
        "template": r"A dataset has {{ n }} samples. Using {{ ratio }}% for training, how many training samples?",
        "options": [
            r"{{ int(n * ratio / 100) }}",
            r"{{ int(n * (100-ratio) / 100) }}",
            r"{{ n }}",
            r"{{ ratio }}"
        ],
        "answer": r"{{ int(n * ratio / 100) }}",
        "variables": [
            {"n": 1000, "ratio": 80},
            {"n": 500, "ratio": 70}
        ],
        "marks": 3
    }
]

# Subjective questions (regular + templated + multi-part)
subjective = [
    # Regular subjective
    {
        "question": r"Compare supervised and unsupervised learning.",
        "answer": r"Supervised uses labeled data, unsupervised finds patterns in unlabeled data.",
        "marks": 8
    },
    
    # Templated subjective
    {
        "template": r"Calculate parameters in a {{ layers }}-layer neural network with {{ neurons }} neurons per layer.",
        "variables": [
            {"layers": 3, "neurons": 64, "answer": "Detailed parameter calculation..."},
            {"layers": 2, "neurons": 128, "answer": "Alternative calculation..."}
        ],
        "marks": 10
    },
    
    # Multi-part question
    {
        "question": r"Analyze model performance:",
        "parts": [
            {
                "question": r"Interpret training=95%, validation=60%.",
                "answer": r"Indicates overfitting.",
                "marks": 3
            },
            {
                "question": r"Suggest solutions.",
                "answer": r"Regularization, more data, simpler model.",
                "marks": 5
            }
        ],
        "marks": 8
    }
]
```

## 🚀 Usage Examples

### Basic Usage:
```bash
# Generate quiz with enhanced features
setwise generate --questions-file enhanced_questions.py --template default --sets 5
```

### Python API:
```python
from setwise.quiz_generator import QuizGenerator

# Create generator with enhanced questions
gen = QuizGenerator(questions_file='enhanced_questions.py', output_dir='output/')

# Access metadata
print(f"Quiz: {gen.quiz_metadata['title']}")
print(f"Duration: {gen.quiz_metadata['duration']}")

# Generate quiz sets
success = gen.generate_quizzes(num_sets=3, template_name='default', compile_pdf=True)
```

## 🔍 Validation

The enhanced setwise includes comprehensive validation:

- **Python syntax** - File must be valid Python
- **Required fields** - `mcq` and `subjective` arrays required
- **Question structure** - Each question needs either `question` or `template` field
- **Template validation** - Templated questions must have `variables` array
- **LaTeX validation** - Math expressions checked for syntax
- **Answer validation** - MCQ answers must match options (after template rendering)

## 🆕 Migration Guide

### From Old Setwise:
1. **Convert files to .py** - Only Python format supported
2. **Add quiz metadata** - Optional but recommended
3. **Update MCQ templates** - Now supported with same syntax as subjective
4. **Test generation** - Verify all questions render correctly

### Backward Compatibility:
- ✅ **Existing .py files** work without changes
- ✅ **Regular questions** unchanged syntax
- ✅ **Subjective templates** work as before
- ✅ **All templates** same syntax

## 🎯 Best Practices

1. **Start simple** - Begin with regular questions, add templates gradually
2. **Test templates** - Verify all variable combinations work
3. **Use metadata** - Makes quizzes more professional
4. **Validate syntax** - Use IDE with Python syntax checking
5. **Test compilation** - Ensure LaTeX renders correctly
6. **Document variables** - Comment complex template expressions

## 🐛 Troubleshooting

### Common Issues:

**Template rendering errors:**
- Check Jinja2 syntax in `{{ expressions }}`
- Verify all variables defined in `variables` array
- Test mathematical expressions with simple values

**LaTeX compilation errors:**
- Escape special characters: `\`, `{`, `}`, `%`
- Use raw strings: `r"LaTeX content"`
- Test complex math expressions separately

**MCQ answer validation:**
- Ensure rendered answer matches one of the rendered options
- Check template expressions in both question and options

**Metadata not showing:**
- Verify `quiz_metadata` dictionary syntax
- Check for typos in metadata field names

## 🎉 Conclusion

The enhanced Setwise is now significantly more powerful and user-friendly:

- **✅ Simplified format** - Python-only for reliability
- **✅ MCQ templates** - Full template support for all question types  
- **✅ Easy metadata** - Professional quiz information
- **✅ Multi-part questions** - Complex question structures
- **✅ Better validation** - Comprehensive error checking

These enhancements make Setwise suitable for professional educational use while maintaining simplicity for basic quiz generation.