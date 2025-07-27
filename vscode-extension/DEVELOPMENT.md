# Setwise VSCode Extension - Development Guide

## Overview

The Setwise VSCode Extension provides a professional development environment for creating LaTeX quiz questions with live preview, validation, and generation capabilities. It transforms VSCode into a powerful quiz authoring tool similar to Overleaf but specifically designed for educational content creation.

## Architecture

### Core Components

1. **Extension Host** (`src/extension.ts`)
   - Main extension activation and command registration
   - Integration with Setwise CLI commands
   - Webview provider for live preview panel
   - Auto-validation and preview triggers

2. **Language Support**
   - Custom language definition for `*questions.py` files
   - Syntax highlighting with LaTeX awareness
   - Auto-completion and bracket matching
   - Folding and indentation rules

3. **Snippet System** (`snippets/setwise-snippets.json`)
   - Rich template library for common question types
   - LaTeX-aware snippets with placeholders
   - Subject-specific templates (physics, chemistry, math)
   - Dynamic question templates with variables

4. **Command Integration**
   - Direct integration with Setwise CLI commands
   - Progress indicators and error handling
   - File validation and LaTeX fixing
   - Quiz generation with download support

## Key Features

### Smart Question Editing
- **Syntax Highlighting**: Custom grammar for questions.py files with LaTeX support
- **IntelliSense**: Auto-completion for question structure keywords
- **Error Detection**: Real-time validation with user-friendly messages
- **Auto-fixing**: Automatic correction of common LaTeX errors

### Live Preview System
- **One-click Preview**: Generate and open PDF preview with single command
- **Real-time Validation**: Instant feedback on file changes
- **Multiple Templates**: Support for default, compact, and minimal layouts
- **Configurable Parameters**: Customizable generation settings

### LaTeX Intelligence
- **Smart Validation**: Context-aware LaTeX syntax checking
- **Auto-correction**: Fixes common issues like missing $, unescaped characters
- **Help Integration**: Contextual LaTeX syntax help and examples
- **Chemical Formula Support**: Automatic H2O → H₂O conversion

### Workflow Integration
- **Command Palette**: All features accessible via Ctrl+Shift+P
- **Keyboard Shortcuts**: Quick access to common operations
- **File Management**: Integrated with VSCode file explorer
- **Output Handling**: Proper error reporting and success feedback

## File Structure

```
vscode-extension/
├── package.json              # Extension manifest and configuration
├── src/
│   └── extension.ts          # Main extension logic
├── syntaxes/
│   └── setwise-questions.tmLanguage.json  # Syntax highlighting grammar
├── snippets/
│   └── setwise-snippets.json # Code snippets and templates
├── language-configuration.json  # Language behavior configuration
├── tsconfig.json            # TypeScript configuration
├── .eslintrc.json          # Linting rules
├── README.md               # User documentation
├── DEVELOPMENT.md          # This file
└── install.sh              # Automated installation script
```

## Command Reference

### Main Commands
- `setwise.previewQuiz` - Generate single quiz set for preview
- `setwise.generateQuiz` - Generate multiple quiz sets with options
- `setwise.validateQuestions` - Validate questions file structure and LaTeX
- `setwise.fixLatex` - Automatically fix common LaTeX errors
- `setwise.showStats` - Display question statistics and validation status

### Template Commands
- `setwise.insertMCQ` - Insert MCQ question template
- `setwise.insertSubjective` - Insert subjective question template

### Keyboard Shortcuts
- `Ctrl+Shift+P` / `Cmd+Shift+P` - Preview Quiz
- `Ctrl+Shift+G` / `Cmd+Shift+G` - Generate Quiz
- `Ctrl+Shift+V` / `Cmd+Shift+V` - Validate Questions

## Configuration Options

```json
{
  "setwise.autoPreview": true,           // Auto-preview when opening questions files
  "setwise.autoValidate": true,          // Auto-validate on file save
  "setwise.defaultTemplate": "default",  // Default quiz template
  "setwise.autoFixLatex": false,         // Auto-fix LaTeX on save
  "setwise.previewSets": 1               // Number of sets for preview
}
```

## Development Setup

### Prerequisites
- Node.js 16+ and npm
- VSCode 1.74+
- TypeScript compiler
- Setwise CLI installed and in PATH

### Build Process
```bash
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch for changes during development
npm run watch

# Package extension
vsce package

# Install locally
code --install-extension setwise-quiz-generator-1.0.0.vsix
```

### Testing
- Test with various questions.py files
- Verify all commands work correctly
- Check syntax highlighting and snippets
- Validate LaTeX error detection and fixing
- Test preview and generation workflows

## Integration Points

### Setwise CLI Integration
The extension integrates with the Setwise CLI through:
- `setwise generate` - Quiz generation
- `setwise questions validate` - File validation
- `setwise questions fix-latex` - LaTeX error fixing
- `setwise questions stats` - Statistics display

### VSCode API Usage
- `vscode.commands` - Command registration and execution
- `vscode.window` - UI components (progress, messages, input)
- `vscode.workspace` - File operations and configuration
- `vscode.languages` - Language features and providers
- Webview API for live preview panel

## User Workflows

### Basic Question Creation
1. Create new `questions.py` file
2. Use `mcq` snippet to add multiple choice questions
3. Use `subjective` snippet for open-ended questions
4. Preview with `Ctrl+Shift+P`
5. Generate final quiz with `Ctrl+Shift+G`

### Advanced Template Usage
1. Use `template` snippet for dynamic questions
2. Add variable placeholders with `{{ variable }}`
3. Define multiple variable sets for randomization
4. Validate with `Ctrl+Shift+V`
5. Generate multiple sets with different values

### LaTeX Error Handling
1. Extension highlights LaTeX syntax errors
2. Auto-fix suggestions appear in problems panel
3. Use "Fix LaTeX Errors" command for batch fixing
4. Real-time validation prevents compilation errors

## Future Enhancements

### Planned Features
- **PDF Preview Panel**: Embedded PDF viewer within VSCode
- **Live Compilation**: Real-time LaTeX compilation as you type
- **Enhanced IntelliSense**: Smart completion for LaTeX commands
- **Template Manager**: GUI for creating and managing question templates
- **Collaboration Features**: Share question libraries and collaborate
- **Export Options**: Direct export to various quiz platforms

### Technical Improvements
- **Performance**: Optimize large file handling
- **Error Recovery**: Better handling of LaTeX compilation failures
- **Customization**: More granular configuration options
- **Accessibility**: Screen reader support and keyboard navigation
- **Testing**: Comprehensive test suite for all features

## Troubleshooting

### Common Issues
- **Command not found**: Ensure Setwise CLI is installed and in PATH
- **LaTeX compilation fails**: Check LaTeX installation and packages
- **Preview not working**: Verify PDF viewer configuration
- **Syntax highlighting missing**: Check file association with questions.py

### Debug Information
- Use "Developer: Toggle Developer Tools" for console logs
- Check Output panel for Setwise extension logs
- Verify extension activation in Extensions view
- Test CLI commands in integrated terminal

## Contributing

### Code Style
- Follow TypeScript best practices
- Use ESLint configuration provided
- Add comments for complex logic
- Update tests for new features

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request with description

## License

MIT License - see main Setwise repository for details.