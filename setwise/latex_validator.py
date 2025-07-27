#!/usr/bin/env python3
"""
LaTeX Validation and Error Handling

Provides utilities for validating LaTeX syntax, fixing common errors,
and providing helpful error messages for users.
"""

import re
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class LaTeXValidator:
    """Validator for LaTeX syntax in quiz questions."""
    
    # Common LaTeX syntax patterns
    MATH_DELIMITERS = [
        (r'\$[^$]*\$', 'inline math'),
        (r'\$\$[^$]*\$\$', 'display math'),
        (r'\\begin\{equation\}.*?\\end\{equation\}', 'equation environment'),
        (r'\\begin\{align\}.*?\\end\{align\}', 'align environment'),
        (r'\\begin\{gather\}.*?\\end\{gather\}', 'gather environment'),
        (r'\\begin\{split\}.*?\\end\{split\}', 'split environment'),
    ]
    
    # Common LaTeX commands that need validation
    COMMON_COMMANDS = [
        r'\\frac\{[^}]*\}\{[^}]*\}',
        r'\\sqrt\{[^}]*\}',
        r'\\sum_\{[^}]*\}',
        r'\\int_\{[^}]*\}',
        r'\\lim_\{[^}]*\}',
        r'\\textbf\{[^}]*\}',
        r'\\textit\{[^}]*\}',
        r'\\begin\{[^}]*\}',
        r'\\end\{[^}]*\}',
    ]
    
    # Common errors and their fixes
    COMMON_FIXES = {
        # Missing $ delimiters
        r'\b([a-zA-Z])\^([0-9]+)\b': r'$\1^{\2}$',
        r'\b([a-zA-Z])_([0-9]+)\b': r'$\1_{\2}$',
        
        # Fix common subscript/superscript without braces
        r'\$([^$]*)\^([a-zA-Z0-9]+)\$': r'$\1^{\2}$',
        r'\$([^$]*)_([a-zA-Z0-9]+)\$': r'$\1_{\2}$',
        
        # Fix degree symbol
        r'(\d+)\s*degrees?': r'\1°',
        r'(\d+)\s*°': r'\1°',
        
        # Fix common chemistry formulas
        r'H2O': r'H$_2$O',
        r'CO2': r'CO$_2$',
        r'SO4': r'SO$_4$',
        r'NH3': r'NH$_3$',
    }
    
    @staticmethod
    def validate_latex_syntax(text: str) -> Tuple[bool, List[str]]:
        """Validate LaTeX syntax in text.
        
        Args:
            text: Text to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for unmatched $ delimiters
        dollar_count = text.count('$')
        if dollar_count % 2 != 0:
            errors.append("Unmatched $ delimiters - every $ must have a closing $")
        
        # Check for unmatched braces
        brace_depth = 0
        for i, char in enumerate(text):
            if char == '{':
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
                if brace_depth < 0:
                    errors.append(f"Unmatched closing brace at position {i}")
                    break
        
        if brace_depth > 0:
            errors.append(f"Unmatched opening braces - missing {brace_depth} closing braces")
        
        # Check for unmatched \begin{} and \end{}
        begin_envs = re.findall(r'\\begin\{([^}]+)\}', text)
        end_envs = re.findall(r'\\end\{([^}]+)\}', text)
        
        for env in begin_envs:
            if begin_envs.count(env) != end_envs.count(env):
                errors.append(f"Unmatched \\begin{{{env}}} environment")
        
        # Check for common LaTeX errors
        if re.search(r'\\frac\{[^}]*\}\{?\}?$', text):
            errors.append("Incomplete \\frac command - needs both numerator and denominator")
        
        if re.search(r'\\sqrt\{\}', text):
            errors.append("Empty \\sqrt command")
        
        # Check for invalid characters in math mode
        math_sections = re.findall(r'\$([^$]+)\$', text)
        for math in math_sections:
            if re.search(r'[&%#]', math):
                errors.append(f"Invalid characters (&, %, #) in math mode: {math}")
        
        # Check for missing spaces after LaTeX commands
        if re.search(r'\\[a-zA-Z]+[a-zA-Z]', text):
            # This is too strict, so let's be more specific
            pass
        
        return len(errors) == 0, errors
    
    @staticmethod
    def suggest_fixes(text: str) -> str:
        """Suggest automatic fixes for common LaTeX errors.
        
        Args:
            text: Text to fix
            
        Returns:
            Fixed text
        """
        fixed_text = text
        
        # Apply common fixes
        for pattern, replacement in LaTeXValidator.COMMON_FIXES.items():
            fixed_text = re.sub(pattern, replacement, fixed_text)
        
        return fixed_text
    
    @staticmethod
    def validate_question_dict(question: Dict) -> Tuple[bool, List[str]]:
        """Validate LaTeX in a question dictionary.
        
        Args:
            question: Question dictionary
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check question text
        if 'question' in question:
            is_valid, question_errors = LaTeXValidator.validate_latex_syntax(question['question'])
            if not is_valid:
                errors.extend([f"Question text: {err}" for err in question_errors])
        
        # Check template text
        if 'template' in question:
            is_valid, template_errors = LaTeXValidator.validate_latex_syntax(question['template'])
            if not is_valid:
                errors.extend([f"Template text: {err}" for err in template_errors])
        
        # Check options for MCQ
        if 'options' in question:
            for i, option in enumerate(question['options']):
                is_valid, option_errors = LaTeXValidator.validate_latex_syntax(option)
                if not is_valid:
                    errors.extend([f"Option {i+1}: {err}" for err in option_errors])
        
        # Check answer text
        if 'answer' in question:
            is_valid, answer_errors = LaTeXValidator.validate_latex_syntax(question['answer'])
            if not is_valid:
                errors.extend([f"Answer text: {err}" for err in answer_errors])
        
        return len(errors) == 0, errors
    
    @staticmethod
    def check_compilation_errors(latex_log: str) -> List[str]:
        """Parse LaTeX compilation log for errors.
        
        Args:
            latex_log: LaTeX compilation log output
            
        Returns:
            List of user-friendly error messages
        """
        errors = []
        
        # Common LaTeX error patterns
        error_patterns = {
            r'! Undefined control sequence': "Undefined LaTeX command - check spelling of commands like \\frac, \\sqrt",
            r'! Missing \$ inserted': "Missing $ for math mode - surround math expressions with $",
            r'! Extra \}': "Extra closing brace } - check for matching braces",
            r'! Missing \}': "Missing closing brace } - check for matching braces", 
            r'! Package .* Error': "Package error - missing or incompatible LaTeX package",
            r'! LaTeX Error: \\begin\{.*\} on input line .* ended by \\end\{.*\}': "Mismatched environment - \\begin{} and \\end{} don't match",
            r'! Missing number, treated as zero': "Missing number in command - check subscripts/superscripts need braces",
            r'! Double superscript': "Double superscript error - use braces: x^{a^b} not x^a^b",
            r'! Double subscript': "Double subscript error - use braces: x_{a_b} not x_a_b",
        }
        
        for pattern, description in error_patterns.items():
            if re.search(pattern, latex_log, re.IGNORECASE):
                errors.append(description)
        
        # Extract line numbers for context
        line_matches = re.findall(r'l\.(\d+)', latex_log)
        if line_matches:
            errors.append(f"Error around line {line_matches[0]} in LaTeX file")
        
        return errors
    
    @staticmethod
    def get_latex_help() -> str:
        """Get help text for common LaTeX usage in questions.
        
        Returns:
            Help text string
        """
        return """
LaTeX Help for Quiz Questions:

MATH MODE:
- Inline math: $x^2 + y^2 = z^2$
- Display math: $$\\frac{a}{b} + \\sqrt{c}$$

COMMON COMMANDS:
- Fractions: \\frac{numerator}{denominator}
- Square root: \\sqrt{expression}
- Superscript: x^{power} (use braces for multi-character)
- Subscript: x_{index} (use braces for multi-character)
- Bold text: \\textbf{bold text}
- Italic text: \\textit{italic text}

CHEMISTRY:
- H₂O should be: H$_2$O
- CO₂ should be: CO$_2$
- Chemical arrows: $\\rightarrow$ or $\\leftrightharpoons$

PHYSICS:
- Units: 3.0 × 10$^8$ m/s
- Vectors: $\\vec{v}$ or $\\mathbf{F}$
- Greek letters: $\\alpha$, $\\beta$, $\\gamma$, $\\pi$

COMMON MISTAKES:
- Don't forget closing $ for math
- Use braces {} for multi-character super/subscripts
- Match every \\begin{} with \\end{}
- Escape special characters: \\%, \\$, \\&
"""


class LaTeXErrorFixer:
    """Automatic LaTeX error fixing utilities."""
    
    @staticmethod
    def fix_common_errors(text: str) -> Tuple[str, List[str]]:
        """Automatically fix common LaTeX errors.
        
        Args:
            text: Original text
            
        Returns:
            Tuple of (fixed_text, list_of_fixes_applied)
        """
        fixes_applied = []
        fixed_text = text
        
        # Fix unescaped percentages
        if '%' in fixed_text and '\\%' not in fixed_text:
            fixed_text = fixed_text.replace('%', '\\%')
            fixes_applied.append("Escaped percentage symbols")
        
        # Fix degree symbols
        degree_pattern = r'(\d+)\s*degrees?'
        if re.search(degree_pattern, fixed_text):
            fixed_text = re.sub(degree_pattern, r'\1°', fixed_text)
            fixes_applied.append("Converted 'degrees' to degree symbol")
        
        # Fix common chemistry formulas
        chem_fixes = {
            'H2O': 'H$_2$O',
            'CO2': 'CO$_2$',
            'NH3': 'NH$_3$',
            'SO4': 'SO$_4$',
            'CaCl2': 'CaCl$_2$',
        }
        
        for wrong, right in chem_fixes.items():
            if wrong in fixed_text and right not in fixed_text:
                fixed_text = fixed_text.replace(wrong, right)
                fixes_applied.append(f"Fixed chemical formula: {wrong} → {right}")
        
        # Fix common math expressions without proper math mode
        # Be careful not to over-fix
        math_patterns = [
            (r'\b([a-zA-Z])\^([0-9])\b', r'$\1^{\2}$'),  # x^2 → $x^{2}$
            (r'\b([a-zA-Z])_([0-9])\b', r'$\1_{\2}$'),   # x_1 → $x_{1}$
        ]
        
        for pattern, replacement in math_patterns:
            matches = re.findall(pattern, fixed_text)
            if matches:
                fixed_text = re.sub(pattern, replacement, fixed_text)
                fixes_applied.append(f"Added math mode for {len(matches)} expressions")
        
        return fixed_text, fixes_applied