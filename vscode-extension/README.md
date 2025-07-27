# Setwise Quiz Generator - VSCode Extension

Professional LaTeX quiz generation with live preview and validation directly in VSCode.

## Features

### 📝 Smart Question Editing
- **Syntax highlighting** for questions.py files with LaTeX support
- **IntelliSense** and auto-completion for question structures
- **Quick templates** via snippets (mcq, subjective, template)
- **Real-time validation** with LaTeX syntax checking

### 🔍 Live Preview & Generation
- **One-click preview** of quiz PDFs
- **Live compilation** with error detection
- **Multiple templates** (default, compact, minimal)
- **Configurable parameters** (sets, questions, seed)

### 🔧 LaTeX Intelligence
- **Automatic error fixing** for common LaTeX mistakes
- **Smart validation** with user-friendly error messages
- **LaTeX help** and syntax reference
- **Chemical formula** and math expression support

### 📊 Question Management
- **File statistics** (question counts, marks, validation status)
- **Quick insertion** of question templates
- **Template variables** for dynamic questions
- **Answer key** generation and tracking

## Quick Start

1. **Install the extension** from VSCode marketplace
2. **Open or create** a `questions.py` file
3. **Use snippets** to quickly add questions:
   - Type `mcq` + Tab for MCQ template
   - Type `subjective` + Tab for subjective template
   - Type `template` + Tab for dynamic questions
4. **Preview quiz** with Ctrl+Shift+P (Cmd+Shift+P on Mac)
5. **Generate final quiz** with Ctrl+Shift+G

## Commands

### Main Commands
- **Setwise: Preview Quiz** (`Ctrl+Shift+P`) - Generate and open PDF preview
- **Setwise: Generate Quiz** (`Ctrl+Shift+G`) - Generate multiple quiz sets
- **Setwise: Validate Questions** (`Ctrl+Shift+V`) - Check syntax and structure

### LaTeX Tools
- **Setwise: Fix LaTeX Errors** - Automatically fix common LaTeX issues
- **Setwise: Show Statistics** - Display question counts and validation status

### Quick Insert
- **Setwise: Insert MCQ Template** - Add new MCQ question
- **Setwise: Insert Subjective Template** - Add new subjective question

## Configuration

```json
{
    "setwise.autoPreview": true,           // Auto-preview when opening questions files
    "setwise.autoValidate": true,          // Auto-validate on save
    "setwise.defaultTemplate": "default",  // Default quiz template
    "setwise.autoFixLatex": false,         // Auto-fix LaTeX on save
    "setwise.previewSets": 1               // Number of sets for preview
}
```

## File Structure

Create question files with this structure:

```python
# Multiple Choice Questions
mcq = [
    {
        "question": r"What is $2 + 2$?",
        "options": [
            r"3",
            r"4", 
            r"5",
            r"6"
        ],
        "answer": r"4",
        "marks": 1
    }
]

# Subjective Questions
subjective = [
    {
        "question": r"Derive the quadratic formula.",
        "answer": r"Starting from $ax^2 + bx + c = 0$...",
        "marks": 5
    }
]
```

## LaTeX Support

The extension provides comprehensive LaTeX support:

### Auto-fixes Applied
- Missing `$` delimiters: `x^2` → `$x^{2}$`
- Chemical formulas: `H2O` → `H$_2$O`
- Special characters: `%` → `\\%`
- Degree symbols: `45 degrees` → `45°`

### Syntax Highlighting
- **Math expressions** in `$...$` are highlighted
- **LaTeX commands** like `\frac`, `\sqrt` are recognized
- **Chemical formulas** and **subscripts** are styled
- **Question structure** keywords are emphasized

## Templates and Snippets

### Available Snippets
- `mcq` - Multiple choice question
- `subjective` - Subjective question  
- `template` - Dynamic question with variables
- `physics` - Physics equation template
- `chemequation` - Chemistry equation template
- `math` - Math expression
- `frac` - LaTeX fraction
- `chem` - Chemical formula

### Template Variables
Create dynamic questions:

```python
{
    "template": r"Calculate kinetic energy with mass {{ mass }} kg and velocity {{ velocity }} m/s",
    "variables": [
        {"mass": 10, "velocity": 5, "answer": "KE = 125 J"},
        {"mass": 2, "velocity": 10, "answer": "KE = 100 J"}
    ],
    "marks": 3
}
```

## Keybindings

| Command | Windows/Linux | Mac |
|---------|---------------|-----|
| Preview Quiz | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Generate Quiz | `Ctrl+Shift+G` | `Cmd+Shift+G` |
| Validate Questions | `Ctrl+Shift+V` | `Cmd+Shift+V` |

## Requirements

- **Setwise CLI** installed: `pip install git+https://github.com/nipunbatra/setwise.git`
- **LaTeX distribution** (TeXLive, MiKTeX, or TinyTeX)
- **Python 3.8+** for running Setwise commands

## Extension Settings

This extension contributes the following settings:

- `setwise.autoPreview`: Automatically preview quiz when questions file is opened
- `setwise.autoValidate`: Automatically validate questions on file save  
- `setwise.defaultTemplate`: Default template for quiz generation
- `setwise.autoFixLatex`: Automatically fix common LaTeX errors on save
- `setwise.previewSets`: Number of quiz sets to generate for preview

## Known Issues

- Large question files (>1000 questions) may take longer to validate
- LaTeX compilation requires proper LaTeX installation
- Preview may not work if Setwise CLI is not in PATH

## Release Notes

### 1.0.0
- Initial release
- Basic question editing with syntax highlighting
- Live preview and validation
- LaTeX auto-fixing and help
- Comprehensive snippet library
- Multi-template support

## Support

For issues and feature requests, visit the [Setwise GitHub repository](https://github.com/nipunbatra/setwise).

## License

MIT License - see the main Setwise repository for details.