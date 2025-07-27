# Setwise User Testing Guide

This guide provides comprehensive testing scenarios to ensure Setwise works perfectly for different types of users.

## 🎯 User Personas & Testing Scenarios

### 1. Educator (Non-Technical) - Dr. Sarah
**Background**: High school physics teacher, not comfortable with code
**Preferred Format**: YAML or Markdown
**Goals**: Create physics quizzes easily, collaborate with colleagues

#### Testing Scenario A: First-Time Setup
```bash
# 1. Install Setwise
pip install git+https://github.com/nipunbatra/setwise.git[web]

# 2. Create example files to learn from
setwise questions create-examples --output-dir my_questions

# 3. Open the most readable format
# User opens my_questions/sample_questions.yaml

# 4. Edit questions in YAML format
# User modifies questions using text editor

# 5. Validate questions
setwise questions validate my_questions/sample_questions.yaml

# 6. Generate quiz
setwise generate --questions-file my_questions/sample_questions.yaml --sets 2
```

**Expected Results**:
- ✅ Clean, readable YAML format
- ✅ Clear error messages if validation fails
- ✅ Beautiful PDF quiz output
- ✅ No technical jargon in interface

#### Testing Scenario B: Web Interface Usage
```bash
# 1. Launch web interface
streamlit run setwise_web.py

# 2. Use "Live Question Editor"
# - Edit questions on left panel
# - See real-time validation on right
# - Use quick insert buttons for templates

# 3. Generate quiz from web interface
# - Click "Generate Quiz" 
# - Download results

# 4. Use "Question Library Manager"
# - Upload existing files
# - Convert between formats
# - Fix LaTeX errors automatically
```

**Expected Results**:
- ✅ Intuitive web interface
- ✅ Real-time feedback and validation
- ✅ No need for command line
- ✅ Easy file management

### 2. Programmer/Developer - Alex
**Background**: Software developer, comfortable with code
**Preferred Format**: Python or JSON
**Goals**: Integrate with existing systems, automate quiz generation

#### Testing Scenario A: API Integration
```python
# 1. Programmatic usage
from setwise import QuizGenerator
from setwise.formats import QuestionFormatConverter

# 2. Load questions from JSON (API-friendly)
mcq, subjective = QuestionFormatConverter.load_questions("api_questions.json")

# 3. Generate quiz programmatically  
generator = QuizGenerator(questions_file="api_questions.json")
success = generator.generate_quizzes(num_sets=5, seed=42)

# 4. Convert formats programmatically
QuestionFormatConverter.save_questions(mcq, subjective, "output.yaml", "yaml")
```

**Expected Results**:
- ✅ Clean Python API
- ✅ Multiple format support
- ✅ Reliable error handling
- ✅ Consistent results with seeds

#### Testing Scenario B: VSCode Extension
```bash
# 1. Install VSCode extension
cd vscode-extension
./install.sh

# 2. Open questions.py file in VSCode
# - Syntax highlighting works
# - Snippets available (mcq + Tab)
# - Commands in Command Palette

# 3. Use VSCode features
# - Ctrl+Shift+P for preview
# - Ctrl+Shift+G for generation
# - Ctrl+Shift+V for validation
```

**Expected Results**:
- ✅ Professional IDE integration
- ✅ Rich editing experience
- ✅ Live validation and preview
- ✅ Efficient keyboard shortcuts

### 3. Spreadsheet User - Maria
**Background**: Office administrator, Excel power user
**Preferred Format**: CSV
**Goals**: Bulk question creation, collaboration via spreadsheets

#### Testing Scenario A: Excel Workflow
```bash
# 1. Create sample CSV
setwise questions create-examples --output-dir excel_work

# 2. Open sample_questions.csv in Excel
# User sees clear tabular format:
# type | question | option1 | option2 | option3 | option4 | answer | marks

# 3. Add many questions using Excel features
# - Copy/paste rows
# - Use Excel formulas
# - Collaborate with colleagues

# 4. Import back to Setwise
setwise questions validate excel_work/sample_questions.csv
setwise generate --questions-file excel_work/sample_questions.csv --sets 3
```

**Expected Results**:
- ✅ Excel-compatible CSV format
- ✅ Clear column structure
- ✅ Handles Excel quirks (quotes, commas)
- ✅ Bulk editing capabilities

#### Testing Scenario B: Format Conversion
```bash
# 1. Convert Excel CSV to other formats
setwise questions convert questions.csv questions.yaml

# 2. Share YAML with technical colleagues
# 3. Convert YAML back to CSV for editing
setwise questions convert questions.yaml questions_v2.csv

# 4. Round-trip validation
# Original questions should be preserved
```

**Expected Results**:
- ✅ Lossless format conversion
- ✅ Preserved question content
- ✅ Handle special characters correctly
- ✅ Clear conversion messages

### 4. Academic Researcher - Dr. James
**Background**: University professor, uses GitHub/LaTeX
**Preferred Format**: Markdown or Python
**Goals**: Version control, documentation, complex LaTeX

#### Testing Scenario A: GitHub Integration
```bash
# 1. Store questions in Markdown for documentation
# questions.md is readable on GitHub

# 2. Use version control
git add questions.md
git commit -m "Add thermodynamics questions"

# 3. Collaborate via pull requests
# Colleagues can review questions in readable format

# 4. Generate quizzes from Markdown
setwise generate --questions-file questions.md --sets 2
```

**Expected Results**:
- ✅ GitHub-friendly Markdown format
- ✅ Readable diffs in version control
- ✅ Proper LaTeX rendering in PDFs
- ✅ Documentation-friendly structure

#### Testing Scenario B: Advanced LaTeX
```python
# 1. Complex mathematical expressions
subjective = [
    {
        "question": r"Derive $\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$",
        "answer": r"Starting from Faraday's law...",
        "marks": 10
    }
]

# 2. Template variables for variants
{
    "template": r"Calculate $\int_0^{{{ upper }}} x^{{ power }} dx$",
    "variables": [
        {"upper": 2, "power": 2, "answer": r"$\frac{8}{3}$"},
        {"upper": 3, "power": 3, "answer": r"$\frac{81}{4}$"}
    ]
}
```

**Expected Results**:
- ✅ Complex LaTeX expressions work
- ✅ Template variables generate correctly
- ✅ Professional mathematical typesetting
- ✅ Consistent formatting across question sets

## 🧪 Comprehensive Feature Testing

### Format Validation Testing
```bash
# Test each format validates correctly
setwise questions validate test.py     # ✅ Should work
setwise questions validate test.yaml   # ✅ Should work  
setwise questions validate test.json   # ✅ Should work
setwise questions validate test.csv    # ✅ Should work
setwise questions validate test.md     # ✅ Should work
setwise questions validate test.txt    # ❌ Should fail gracefully
```

### Error Handling Testing
```bash
# Test various error conditions
setwise questions validate nonexistent.yaml          # File not found
setwise questions validate malformed.json            # Invalid JSON
setwise questions validate empty.csv                 # Empty file
setwise generate --questions-file broken.yaml        # Generation errors
```

### LaTeX Error Testing
```bash
# Test LaTeX validation and fixing
# Create file with common LaTeX errors:
# - Missing $ delimiters
# - Unescaped % characters  
# - Chemical formulas without subscripts

setwise questions validate broken_latex.yaml         # Should show errors
setwise questions fix-latex broken_latex.yaml        # Should fix errors
setwise questions validate broken_latex.yaml         # Should pass now
```

### Performance Testing
```bash
# Test with large files
# Create 1000 questions
setwise questions create-examples --output-dir large_test
# Edit to have 1000 questions
setwise questions validate large_questions.yaml      # Should handle large files
setwise generate --questions-file large_questions.yaml --sets 10  # Performance test
```

### Integration Testing
```bash
# Test full workflow
setwise questions create-examples --output-dir workflow_test
setwise questions convert workflow_test/sample_questions.py workflow_test/test.yaml
setwise questions validate workflow_test/test.yaml
setwise generate --questions-file workflow_test/test.yaml --sets 3
setwise questions stats workflow_test/test.yaml
```

## 🎯 Success Criteria

### For Educators
- [ ] Can create questions without touching code
- [ ] Error messages are helpful, not technical
- [ ] Web interface is intuitive
- [ ] Can collaborate easily with colleagues
- [ ] LaTeX errors are auto-fixed when possible

### For Developers  
- [ ] Clean Python API
- [ ] VSCode extension works smoothly
- [ ] Good error handling and debugging
- [ ] Format conversion is reliable
- [ ] Can integrate with existing systems

### For Spreadsheet Users
- [ ] CSV format works in Excel/Sheets
- [ ] Bulk editing is efficient
- [ ] Round-trip conversion preserves data
- [ ] Column structure is clear

### For Researchers
- [ ] Markdown is GitHub-friendly
- [ ] Complex LaTeX expressions work
- [ ] Version control diffs are readable
- [ ] Template variables enable variants

## 🐛 Common Issues & Solutions

### Issue: YAML indentation errors
**Solution**: Clear error messages point to line numbers
```bash
setwise questions validate broken.yaml
# ❌ YAML syntax error at line 5: expected <block end>, but found '<scalar>'
# 💡 Check indentation - YAML requires consistent spacing
```

### Issue: LaTeX compilation failures  
**Solution**: Auto-fix common errors
```bash
setwise questions fix-latex questions.yaml --dry-run  # Preview fixes
setwise questions fix-latex questions.yaml            # Apply fixes
```

### Issue: CSV special characters
**Solution**: Proper escaping and quoting
```bash
# CSV handles commas, quotes automatically
"What is Paris, France?","London","Paris","Rome","Paris"
```

### Issue: Large file performance
**Solution**: Streaming validation and progress indicators
```bash
setwise questions validate large_file.yaml
# Validating 1000 questions... ████████████████ 100%
```

## 📊 Testing Checklist

### Installation Testing
- [ ] `pip install` works on Windows/Mac/Linux
- [ ] Dependencies install correctly
- [ ] VSCode extension installs without errors
- [ ] Web interface launches successfully

### Core Functionality
- [ ] Question validation works for all formats
- [ ] Quiz generation produces PDFs
- [ ] Format conversion preserves content
- [ ] LaTeX expressions render correctly
- [ ] Answer keys match questions

### User Experience
- [ ] Help messages are clear and helpful
- [ ] Error messages suggest solutions
- [ ] Examples are provided for all features
- [ ] Documentation is comprehensive
- [ ] Workflows are intuitive

### Edge Cases
- [ ] Empty files handled gracefully
- [ ] Large files (1000+ questions) work
- [ ] Special characters don't break parsing
- [ ] Network issues don't crash web interface
- [ ] Invalid LaTeX provides helpful errors

### Platform Testing
- [ ] Works on Windows 10/11
- [ ] Works on macOS (Intel/Apple Silicon)
- [ ] Works on Linux (Ubuntu/CentOS)
- [ ] Python 3.8+ compatibility
- [ ] VSCode extension cross-platform

## 🎉 Success Metrics

**Adoption Success**:
- Educators can create their first quiz in < 10 minutes
- Error rate < 5% for valid question files
- User satisfaction > 90% in feedback surveys
- Support requests decrease over time

**Technical Success**:
- Test coverage > 85%
- No critical security vulnerabilities
- Performance: < 2 seconds for typical quiz generation
- Format conversion accuracy > 99%

**Community Success**:
- Multiple user personas adopt different formats
- Active GitHub discussions and contributions
- Educational institutions deploy successfully
- Integration with existing educational tools

This testing guide ensures Setwise works excellently for all user types and provides a robust, user-friendly quiz generation experience!