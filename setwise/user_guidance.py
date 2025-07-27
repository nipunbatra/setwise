#!/usr/bin/env python3
"""
User Guidance and Help System for Setwise

Provides contextual help, error explanations, and workflow guidance
to improve the user experience for all skill levels.
"""

import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class UserGuidance:
    """Provides contextual help and guidance for users."""
    
    # Error message improvements
    ERROR_SOLUTIONS = {
        "File not found": {
            "solution": "💡 The file doesn't exist. Try creating example files first.",
            "commands": [
                "setwise questions create-examples --output-dir examples",
                "setwise questions create-sample my_questions.py"
            ]
        },
        "Invalid YAML": {
            "solution": "💡 YAML syntax error. Check indentation and structure.",
            "commands": [
                "# YAML is sensitive to spaces - use consistent indentation",
                "# Example of correct YAML structure:",
                "mcq:",
                "  - question: 'Your question?'",
                "    options: ['A', 'B', 'C']"
            ]
        },
        "Invalid JSON": {
            "solution": "💡 JSON syntax error. Check for missing quotes or commas.",
            "commands": [
                "# JSON requires double quotes for strings",
                '{"question": "Your question?", "options": ["A", "B"]}',
                "# Validate JSON at: https://jsonlint.com/"
            ]
        },
        "Missing required field": {
            "solution": "💡 Required fields missing. Check the question structure.",
            "commands": [
                "# MCQ questions need: question, options, answer, marks",
                "# Subjective questions need: question, answer, marks",
                "setwise questions validate my_questions.yaml --verbose"
            ]
        },
        "LaTeX compilation failed": {
            "solution": "💡 LaTeX syntax error. Use the auto-fix feature.",
            "commands": [
                "setwise questions fix-latex my_questions.yaml --dry-run",
                "setwise questions fix-latex my_questions.yaml",
                "setwise questions latex-help"
            ]
        }
    }
    
    # Format recommendations based on user profile
    FORMAT_RECOMMENDATIONS = {
        "educator": {
            "primary": "yaml",
            "reason": "Human-readable, easy to learn, version control friendly",
            "example": "Perfect for creating and sharing question banks"
        },
        "developer": {
            "primary": "json",
            "reason": "Standard format, excellent tool support, API integration",
            "example": "Great for web applications and automated systems"
        },
        "spreadsheet_user": {
            "primary": "csv", 
            "reason": "Excel/Sheets compatibility, bulk editing capabilities",
            "example": "Edit hundreds of questions in familiar spreadsheet interface"
        },
        "researcher": {
            "primary": "markdown",
            "reason": "Documentation-friendly, GitHub integration, readable",
            "example": "Combine questions with documentation and version control"
        },
        "programmer": {
            "primary": "python",
            "reason": "Full programming power, template variables, complex logic",
            "example": "Create dynamic questions with conditional logic"
        }
    }
    
    @staticmethod
    def get_format_recommendation(user_type: str = None) -> Dict:
        """Get format recommendation based on user type."""
        if user_type and user_type.lower() in UserGuidance.FORMAT_RECOMMENDATIONS:
            return UserGuidance.FORMAT_RECOMMENDATIONS[user_type.lower()]
        
        # Interactive recommendation
        return UserGuidance._interactive_format_recommendation()
    
    @staticmethod
    def _interactive_format_recommendation() -> Dict:
        """Interactive format recommendation based on user answers."""
        print("🎯 Let's find the best format for you!")
        print("Answer a few quick questions:")
        
        # Simple scoring system
        scores = {"yaml": 0, "json": 0, "csv": 0, "markdown": 0, "python": 0}
        
        try:
            # Question 1: Technical comfort
            tech_comfort = input("Are you comfortable with code/programming? (y/n): ").lower()
            if tech_comfort.startswith('y'):
                scores["python"] += 2
                scores["json"] += 1
            else:
                scores["yaml"] += 2
                scores["csv"] += 1
            
            # Question 2: Tool preference
            spreadsheet = input("Do you regularly use Excel or Google Sheets? (y/n): ").lower()
            if spreadsheet.startswith('y'):
                scores["csv"] += 3
            
            # Question 3: GitHub usage
            github = input("Do you use GitHub or version control? (y/n): ").lower()
            if github.startswith('y'):
                scores["yaml"] += 2
                scores["markdown"] += 2
                scores["python"] += 1
            
            # Question 4: Team collaboration
            team = input("Do you work with a team on questions? (y/n): ").lower()
            if team.startswith('y'):
                scores["yaml"] += 1
                scores["csv"] += 1
                scores["markdown"] += 1
            
            # Question 5: Web integration
            web = input("Do you need web/API integration? (y/n): ").lower()
            if web.startswith('y'):
                scores["json"] += 3
                scores["python"] += 1
            
        except (KeyboardInterrupt, EOFError):
            # Default to YAML if interrupted
            return UserGuidance.FORMAT_RECOMMENDATIONS["educator"]
        
        # Find highest scoring format
        recommended_format = max(scores, key=scores.get)
        
        # Map to user type for consistent response
        format_map = {
            "yaml": "educator",
            "json": "developer", 
            "csv": "spreadsheet_user",
            "markdown": "researcher",
            "python": "programmer"
        }
        
        user_type = format_map.get(recommended_format, "educator")
        return UserGuidance.FORMAT_RECOMMENDATIONS[user_type]
    
    @staticmethod
    def enhance_error_message(error_msg: str) -> str:
        """Enhance error message with helpful suggestions."""
        enhanced_msg = error_msg
        
        # Look for matching error patterns
        for error_pattern, solution_info in UserGuidance.ERROR_SOLUTIONS.items():
            if error_pattern.lower() in error_msg.lower():
                enhanced_msg += f"\n\n{solution_info['solution']}\n"
                enhanced_msg += "Try these commands:\n"
                for cmd in solution_info['commands']:
                    if cmd.startswith('#'):
                        enhanced_msg += f"  {cmd}\n"
                    else:
                        enhanced_msg += f"  $ {cmd}\n"
                break
        
        return enhanced_msg
    
    @staticmethod
    def detect_common_issues(file_path: str, content: str = None) -> List[str]:
        """Detect common issues and provide suggestions."""
        suggestions = []
        path = Path(file_path)
        
        # Read content if not provided
        if content is None and path.exists():
            try:
                content = path.read_text(encoding='utf-8')
            except Exception:
                return ["❌ Unable to read file - check file permissions"]
        
        if not content:
            return ["❌ File is empty - use 'setwise questions create-examples' to get started"]
        
        # Detect potential math expressions without $ delimiters
        math_patterns = [
            (r'\b[a-zA-Z]\^[\w+]', "x^2"),
            (r'\b[a-zA-Z]_[\w+]', "H_2"),
            (r'\\frac\{[^}]*\}\{[^}]*\}', "\\frac{a}{b}"),
            (r'\\sqrt\{[^}]*\}', "\\sqrt{x}"),
        ]
        
        for pattern, example in math_patterns:
            matches = re.findall(pattern, content)
            if matches and not UserGuidance._is_in_math_mode(content, matches[0]):
                suggestions.append(
                    f"💡 Found math expression '{matches[0]}' - consider wrapping in $: ${matches[0]}$"
                )
        
        # Check for common chemistry formulas without subscripts
        chem_patterns = [
            (r'\bH2O\b', "H$_2$O"),
            (r'\bCO2\b', "CO$_2$"),
            (r'\bNH3\b', "NH$_3$"),
            (r'\bSO4\b', "SO$_4$"),
        ]
        
        for pattern, suggestion in chem_patterns:
            if re.search(pattern, content):
                match = re.search(pattern, content).group()
                if not UserGuidance._is_in_math_mode(content, match):
                    suggestions.append(f"💡 Chemistry formula '{match}' should use subscripts: {suggestion}")
        
        # Check for common physics units and expressions
        physics_patterns = [
            (r'\b(\d+)\s*degrees?\b', r"\1°"),
            (r'\b(\d+)\s*kg\s*m/s\b', r"$\1$ kg⋅m/s"),
            (r'\b(\d+)\s*m/s2\b', r"$\1$ m/s²"),
        ]
        
        for pattern, suggestion in physics_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                suggestions.append(f"💡 Physics unit '{match}' can be improved: {suggestion}")
        
        # Check for missing marks field
        if 'marks' not in content.lower():
            suggestions.append("💡 Consider adding 'marks' field to specify question points")
        
        # Check for very long questions (might need breaking up)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if len(line) > 200 and 'question' in line.lower():
                suggestions.append(f"💡 Line {i+1}: Very long question - consider breaking into multiple parts")
        
        # Check for common CSV issues
        if path.suffix.lower() == '.csv':
            if ',' in content and content.count('"') % 2 != 0:
                suggestions.append("💡 CSV: Unmatched quotes detected - ensure proper quoting of fields with commas")
            
            if '\t' in content:
                suggestions.append("💡 CSV: Tab characters detected - use commas as separators")
        
        # Check for YAML issues
        if path.suffix.lower() in ['.yaml', '.yml']:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('-') and line.count(' ') != line.count(' ', 0, line.find('-') + 2):
                    suggestions.append(f"💡 YAML line {i+1}: Inconsistent indentation for list item")
        
        # Check for JSON issues
        if path.suffix.lower() == '.json':
            if "'" in content and '"' not in content:
                suggestions.append("💡 JSON: Use double quotes instead of single quotes for strings")
            
            if content.count('{') != content.count('}'):
                suggestions.append("💡 JSON: Unmatched braces - check for missing { or }")
        
        # Check for accessibility and readability
        if content.count('?') < content.count('question'):
            suggestions.append("💡 Some questions might be missing question marks")
        
        return suggestions
    
    @staticmethod
    def _is_in_math_mode(text: str, expression: str) -> bool:
        """Check if expression is already in math mode (between $ delimiters)."""
        # Find position of expression
        pos = text.find(expression)
        if pos == -1:
            return False
        
        # Count $ before this position
        dollars_before = text[:pos].count('$')
        
        # If odd number of $ before, we're in math mode
        return dollars_before % 2 == 1
    
    @staticmethod
    def show_format_comparison():
        """Show comparison of all formats to help users choose."""
        print("""
📊 Setwise Format Comparison Guide

┌─────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Format      │ Best For        │ Pros            │ Cons            │
├─────────────┼─────────────────┼─────────────────┼─────────────────┤
│ YAML        │ 📚 Educators    │ • Human readable│ • Indent-sensitive │
│ (.yaml)     │   Non-technical │ • Clean syntax  │ • YAML rules    │
│             │   Version ctrl  │ • Git friendly  │                 │
├─────────────┼─────────────────┼─────────────────┼─────────────────┤
│ JSON        │ 💻 Developers   │ • Standard fmt  │ • Less readable │
│ (.json)     │   Web apps      │ • Tool support  │ • Strict syntax │
│             │   APIs          │ • Validation    │                 │
├─────────────┼─────────────────┼─────────────────┼─────────────────┤
│ CSV         │ 📊 Spreadsheets │ • Excel compat  │ • Limited format│
│ (.csv)      │   Bulk editing  │ • Familiar UI   │ • Special chars │
│             │   Collaboration │ • Mass import   │                 │
├─────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Markdown    │ 📖 Docs/GitHub  │ • Readable      │ • Basic structure│
│ (.md)       │   Documentation │ • GitHub UI     │ • Limited power │
│             │   Sharing       │ • Preview       │                 │
├─────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Python      │ 🐍 Programmers  │ • Full power    │ • Requires coding│
│ (.py)       │   Advanced use  │ • Templates     │ • Complex syntax │
│             │   Complex logic │ • Variables     │                 │
└─────────────┴─────────────────┴─────────────────┴─────────────────┘

💡 Not sure? Run: setwise questions recommend-format
""")
    
    @staticmethod
    def show_workflow_help(workflow_type: str):
        """Show help for specific workflows."""
        workflows = {
            "first-time": """
🎯 First-Time User Workflow

1. Create example files to learn from:
   $ setwise questions create-examples --output-dir examples

2. Pick your preferred format:
   $ setwise questions recommend-format

3. Edit the example file in your chosen format

4. Validate your questions:
   $ setwise questions validate examples/sample_questions.yaml

5. Generate your first quiz:
   $ setwise generate --questions-file examples/sample_questions.yaml

6. Open the generated PDF and celebrate! 🎉
""",
            
            "collaboration": """
🤝 Team Collaboration Workflow

1. Choose a common format (recommended: YAML):
   $ setwise questions create-examples --format yaml

2. Set up version control:
   $ git init quiz-bank
   $ git add *.yaml
   $ git commit -m "Initial question bank"

3. Create shared conventions:
   - Use consistent naming: subject_topic_questions.yaml
   - Document question sources in comments
   - Review changes before merging

4. Convert between formats as needed:
   $ setwise questions convert shared.yaml personal.csv

5. Generate quizzes from shared repository:
   $ setwise generate --questions-file shared.yaml --sets 5
""",
            
            "bulk-editing": """
📊 Bulk Question Creation Workflow

1. Create CSV template:
   $ setwise questions create-examples --format csv

2. Open in Excel/Google Sheets:
   - Copy/paste existing questions
   - Use formulas for marks calculation
   - Filter and sort by topic/difficulty

3. Export back to CSV format

4. Convert to other formats if needed:
   $ setwise questions convert bulk_questions.csv questions.yaml

5. Validate and generate:
   $ setwise questions validate bulk_questions.csv
   $ setwise generate --questions-file bulk_questions.csv --sets 10
""",
            
            "latex-heavy": """
🔬 LaTeX-Heavy Content Workflow

1. Start with Python format for maximum control:
   $ setwise questions create-sample advanced_questions.py

2. Use raw strings for complex LaTeX:
   question = r"Calculate $\\int_0^{\\pi} \\sin^2(x) dx$"

3. Validate LaTeX syntax:
   $ setwise questions validate advanced_questions.py

4. Auto-fix common errors:
   $ setwise questions fix-latex advanced_questions.py

5. Get LaTeX help when needed:
   $ setwise questions latex-help

6. Test compilation:
   $ setwise generate --questions-file advanced_questions.py --sets 1
"""
        }
        
        if workflow_type in workflows:
            print(workflows[workflow_type])
        else:
            print(f"❌ Unknown workflow: {workflow_type}")
            print("Available workflows: first-time, collaboration, bulk-editing, latex-heavy")


def main():
    """CLI interface for user guidance."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python user_guidance.py [command]")
        print("Commands: recommend-format, format-comparison, workflow [type]")
        return
    
    command = sys.argv[1]
    
    if command == "recommend-format":
        rec = UserGuidance.get_format_recommendation()
        print(f"\n🎯 Recommended format: {rec['primary']}")
        print(f"📝 Reason: {rec['reason']}")
        print(f"💡 Example use: {rec['example']}")
    
    elif command == "format-comparison":
        UserGuidance.show_format_comparison()
    
    elif command == "workflow":
        if len(sys.argv) < 3:
            print("Available workflows: first-time, collaboration, bulk-editing, latex-heavy")
        else:
            UserGuidance.show_workflow_help(sys.argv[2])
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()