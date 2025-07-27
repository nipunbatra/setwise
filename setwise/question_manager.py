#!/usr/bin/env python3
"""
Question Library Management System

Provides utilities for managing, validating, and listing question libraries.
"""

import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import sys
from .latex_validator import LaTeXValidator, LaTeXErrorFixer
from .formats import QuestionFormatConverter


class QuestionManager:
    """Manager for question libraries and validation."""
    
    @staticmethod
    def validate_questions_file(file_path: str) -> Tuple[bool, str]:
        """Validate a questions file format and structure (supports multiple formats).
        
        Args:
            file_path: Path to the questions file (.py, .yaml, .json, .csv, .md)
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            questions_path = Path(file_path)
            if not questions_path.exists():
                return False, f"File not found: {file_path}"
            
            # Detect format and load questions
            format_type = QuestionFormatConverter.detect_format(file_path)
            
            if format_type == 'unknown':
                return False, f"Unsupported file format: {questions_path.suffix}. Supported: .py, .yaml, .json, .csv, .md"
            
            # Load questions using format converter
            mcq, subjective = QuestionFormatConverter.load_questions(file_path)
            
            # Validate structure
            if not isinstance(mcq, list):
                return False, "'mcq' must be a list"
            
            if not isinstance(subjective, list):
                return False, "'subjective' must be a list"
            
            if not isinstance(mcq, list):
                return False, "'mcq' must be a list"
            
            if not isinstance(subjective, list):
                return False, "'subjective' must be a list"
            
            # Validate MCQ format
            for i, q in enumerate(mcq):
                if not isinstance(q, dict):
                    return False, f"MCQ question {i+1} must be a dictionary"
                
                required_fields = ['question', 'options', 'answer']
                for field in required_fields:
                    if field not in q:
                        return False, f"MCQ question {i+1} missing required field: {field}"
                
                if not isinstance(q['options'], list):
                    return False, f"MCQ question {i+1} 'options' must be a list"
                
                if len(q['options']) < 2:
                    return False, f"MCQ question {i+1} must have at least 2 options"
                
                if q['answer'] not in q['options']:
                    return False, f"MCQ question {i+1} answer must be one of the options"
                
                # Validate LaTeX syntax
                is_valid, latex_errors = LaTeXValidator.validate_question_dict(q)
                if not is_valid:
                    return False, f"MCQ question {i+1} LaTeX errors: {'; '.join(latex_errors)}"
            
            # Validate subjective format
            for i, q in enumerate(subjective):
                if not isinstance(q, dict):
                    return False, f"Subjective question {i+1} must be a dictionary"
                
                # Check for either 'question' or 'template' field
                if 'question' not in q and 'template' not in q:
                    return False, f"Subjective question {i+1} must have either 'question' or 'template' field"
                
                # If template is used, validate variables
                if 'template' in q:
                    if 'variables' not in q:
                        return False, f"Subjective question {i+1} with template must have 'variables' field"
                    
                    if not isinstance(q['variables'], list):
                        return False, f"Subjective question {i+1} 'variables' must be a list"
                
                # Validate LaTeX syntax
                is_valid, latex_errors = LaTeXValidator.validate_question_dict(q)
                if not is_valid:
                    return False, f"Subjective question {i+1} LaTeX errors: {'; '.join(latex_errors)}"
            
            return True, f"Valid questions file with {len(mcq)} MCQ and {len(subjective)} subjective questions"
            
        except Exception as e:
            return False, f"Error validating file: {str(e)}"
    
    @staticmethod
    def list_question_libraries(search_dirs: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Find and list available question libraries (supports multiple formats).
        
        Args:
            search_dirs: Directories to search for question files
            
        Returns:
            List of dictionaries with library information
        """
        if search_dirs is None:
            search_dirs = ['.', 'data', 'questions', 'examples']
        
        libraries = []
        
        # Supported extensions
        extensions = ['*.py', '*.yaml', '*.yml', '*.json', '*.csv', '*.md']
        
        for search_dir in search_dirs:
            search_path = Path(search_dir)
            if search_path.exists():
                # Look for question files with supported extensions
                for extension in extensions:
                    for question_file in search_path.rglob(f"*questions*{extension[1:]}"):
                        is_valid, message = QuestionManager.validate_questions_file(str(question_file))
                    
                        libraries.append({
                            'path': str(question_file),
                            'name': question_file.stem,
                            'format': QuestionFormatConverter.detect_format(str(question_file)),
                            'valid': is_valid,
                            'info': message,
                            'size': question_file.stat().st_size if question_file.exists() else 0
                        })
        
        return libraries
    
    @staticmethod
    def create_sample_questions_file(output_path: str) -> bool:
        """Create a sample questions.py file template.
        
        Args:
            output_path: Where to create the sample file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            sample_content = '''"""
Sample Questions File for Setwise Quiz Generator

This file demonstrates the required format for custom question libraries.
Copy and modify this file to create your own question sets.
"""

# Multiple Choice Questions
# Each question must have: question, options, answer, marks (optional)
mcq = [
    {
        "question": r"What is the capital of France?",
        "options": [
            r"London",
            r"Berlin", 
            r"Paris",
            r"Madrid",
            r"Rome"
        ],
        "answer": r"Paris",
        "marks": 1
    },
    {
        "question": r"Which of the following is a programming language?",
        "options": [
            r"HTML",
            r"CSS",
            r"Python",
            r"JSON",
            r"XML"
        ],
        "answer": r"Python",
        "marks": 2
    }
]

# Subjective Questions
# Can be simple questions or templated questions with variables
subjective = [
    {
        "question": r"Explain the concept of object-oriented programming and provide an example.",
        "answer": "OOP is a programming paradigm based on objects containing data and methods...",
        "marks": 5
    },
    {
        "template": r"Calculate the area of a rectangle with length {{ length }} and width {{ width }}.",
        "variables": [
            {"length": 5, "width": 3, "answer": "Area = 5 × 3 = 15 square units"},
            {"length": 8, "width": 4, "answer": "Area = 8 × 4 = 32 square units"},
            {"length": 10, "width": 6, "answer": "Area = 10 × 6 = 60 square units"}
        ],
        "marks": 3
    }
]
'''
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(sample_content)
            
            return True
            
        except Exception as e:
            print(f"Error creating sample file: {e}")
            return False
    
    @staticmethod
    def get_question_stats(file_path: str) -> Dict[str, Any]:
        """Get statistics about a questions file (supports multiple formats).
        
        Args:
            file_path: Path to the questions file (.py, .yaml, .json, .csv, .md)
            
        Returns:
            Dictionary with statistics
        """
        try:
            questions_path = Path(file_path)
            if not questions_path.exists():
                return {"error": "File not found"}
            
            # Load questions using format converter
            mcq, subjective = QuestionFormatConverter.load_questions(file_path)
            format_type = QuestionFormatConverter.detect_format(file_path)
            
            stats = {
                "file_path": str(questions_path),
                "file_size": questions_path.stat().st_size,
                "mcq_count": 0,
                "subjective_count": 0,
                "total_mcq_marks": 0,
                "total_subjective_marks": 0,
                "templated_subjective": 0
            }
            
            if hasattr(questions_module, 'mcq'):
                mcq = questions_module.mcq
                stats["mcq_count"] = len(mcq)
                stats["total_mcq_marks"] = sum(q.get("marks", 1) for q in mcq)
            
            if hasattr(questions_module, 'subjective'):
                subjective = questions_module.subjective
                stats["subjective_count"] = len(subjective)
                stats["total_subjective_marks"] = sum(q.get("marks", 5) for q in subjective)
                stats["templated_subjective"] = sum(1 for q in subjective if "template" in q)
            
            stats["total_questions"] = stats["mcq_count"] + stats["subjective_count"]
            stats["total_marks"] = stats["total_mcq_marks"] + stats["total_subjective_marks"]
            
            return stats
            
        except Exception as e:
            return {"error": str(e)}