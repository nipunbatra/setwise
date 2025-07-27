#!/usr/bin/env python3
"""
Question Library Management System

Provides utilities for managing, validating, and listing question libraries.
"""

import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import sys


class QuestionManager:
    """Manager for question libraries and validation."""
    
    @staticmethod
    def validate_questions_file(file_path: str) -> Tuple[bool, str]:
        """Validate a questions.py file format and structure.
        
        Args:
            file_path: Path to the questions.py file
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            questions_path = Path(file_path)
            if not questions_path.exists():
                return False, f"File not found: {file_path}"
            
            if not questions_path.suffix == ".py":
                return False, f"File must have .py extension: {file_path}"
            
            # Load the module
            spec = importlib.util.spec_from_file_location("questions_validation", questions_path)
            if spec is None or spec.loader is None:
                return False, f"Could not load Python file: {file_path}"
            
            questions_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(questions_module)
            
            # Check required variables
            if not hasattr(questions_module, 'mcq'):
                return False, "File must define 'mcq' variable (list of MCQ questions)"
            
            if not hasattr(questions_module, 'subjective'):
                return False, "File must define 'subjective' variable (list of subjective questions)"
            
            # Validate structure
            mcq = questions_module.mcq
            subjective = questions_module.subjective
            
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
            
            return True, f"Valid questions file with {len(mcq)} MCQ and {len(subjective)} subjective questions"
            
        except Exception as e:
            return False, f"Error validating file: {str(e)}"
    
    @staticmethod
    def list_question_libraries(search_dirs: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Find and list available question libraries.
        
        Args:
            search_dirs: Directories to search for questions.py files
            
        Returns:
            List of dictionaries with library information
        """
        if search_dirs is None:
            search_dirs = ['.', 'data', 'questions']
        
        libraries = []
        
        for search_dir in search_dirs:
            search_path = Path(search_dir)
            if search_path.exists():
                # Look for questions.py files
                for py_file in search_path.rglob("*questions*.py"):
                    is_valid, message = QuestionManager.validate_questions_file(str(py_file))
                    
                    libraries.append({
                        'path': str(py_file),
                        'name': py_file.stem,
                        'valid': is_valid,
                        'info': message,
                        'size': py_file.stat().st_size if py_file.exists() else 0
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
        """Get statistics about a questions file.
        
        Args:
            file_path: Path to the questions.py file
            
        Returns:
            Dictionary with statistics
        """
        try:
            questions_path = Path(file_path)
            if not questions_path.exists():
                return {"error": "File not found"}
            
            # Load the module
            spec = importlib.util.spec_from_file_location("questions_stats", questions_path)
            if spec is None or spec.loader is None:
                return {"error": "Could not load file"}
            
            questions_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(questions_module)
            
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