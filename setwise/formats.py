#!/usr/bin/env python3
"""
Enhanced Question File Format Support for Setwise

Supports multiple user-friendly formats:
- YAML (.yaml/.yml) - Most human-readable
- JSON (.json) - Web-friendly 
- CSV (.csv) - Spreadsheet-friendly
- Markdown (.md) - Documentation-friendly
- Python (.py) - Programmer-friendly (existing)
"""

import yaml
import json
import csv
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional


class QuestionFormatConverter:
    """Convert between different question file formats."""
    
    @staticmethod
    def detect_format(file_path: str) -> str:
        """Detect file format from extension."""
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        format_map = {
            '.py': 'python',
            '.yaml': 'yaml',
            '.yml': 'yaml', 
            '.json': 'json',
            '.csv': 'csv',
            '.md': 'markdown',
            '.txt': 'text'
        }
        
        return format_map.get(suffix, 'unknown')
    
    @staticmethod
    def load_questions(file_path: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Load questions from any supported format."""
        format_type = QuestionFormatConverter.detect_format(file_path)
        
        if format_type == 'python':
            return QuestionFormatConverter._load_python(file_path)
        elif format_type == 'yaml':
            return QuestionFormatConverter._load_yaml(file_path)
        elif format_type == 'json':
            return QuestionFormatConverter._load_json(file_path)
        elif format_type == 'csv':
            return QuestionFormatConverter._load_csv(file_path)
        elif format_type == 'markdown':
            return QuestionFormatConverter._load_markdown(file_path)
        else:
            raise ValueError(f"Unsupported file format: {format_type}")
    
    @staticmethod
    def _load_python(file_path: str) -> Tuple[List[Dict], List[Dict]]:
        """Load from Python file (existing functionality)."""
        import importlib.util
        
        spec = importlib.util.spec_from_file_location("questions", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        mcq = getattr(module, 'mcq', [])
        subjective = getattr(module, 'subjective', [])
        
        return mcq, subjective
    
    @staticmethod
    def _load_yaml(file_path: str) -> Tuple[List[Dict], List[Dict]]:
        """Load from YAML file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        mcq = data.get('mcq', data.get('multiple_choice', []))
        subjective = data.get('subjective', data.get('short_answer', []))
        
        return mcq, subjective
    
    @staticmethod
    def _load_json(file_path: str) -> Tuple[List[Dict], List[Dict]]:
        """Load from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        mcq = data.get('mcq', data.get('multiple_choice', []))
        subjective = data.get('subjective', data.get('short_answer', []))
        
        return mcq, subjective
    
    @staticmethod
    def _load_csv(file_path: str) -> Tuple[List[Dict], List[Dict]]:
        """Load from CSV file with intelligent parsing."""
        mcq = []
        subjective = []
        
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            # Try to detect dialect
            sample = f.read(1024)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample)
            
            reader = csv.DictReader(f, dialect=dialect)
            
            for row in reader:
                question_type = row.get('type', '').lower()
                question_text = row.get('question', '')
                
                if not question_text:
                    continue
                
                if question_type.startswith('mcq') or 'option' in row:
                    # Parse MCQ
                    options = []
                    answer = row.get('answer', '')
                    
                    # Collect options (option1, option2, etc. or optionA, optionB, etc.)
                    for key, value in row.items():
                        if key.lower().startswith('option') and value:
                            options.append(value)
                    
                    if options:
                        mcq_item = {
                            'question': question_text,
                            'options': options,
                            'answer': answer,
                            'marks': int(row.get('marks', 1))
                        }
                        mcq.append(mcq_item)
                
                else:
                    # Treat as subjective
                    subj_item = {
                        'question': question_text,
                        'answer': row.get('answer', row.get('solution', '')),
                        'marks': int(row.get('marks', 5))
                    }
                    subjective.append(subj_item)
        
        return mcq, subjective
    
    @staticmethod
    def _load_markdown(file_path: str) -> Tuple[List[Dict], List[Dict]]:
        """Load from Markdown file with structured format."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        mcq = []
        subjective = []
        
        # Parse MCQ sections
        mcq_pattern = r'## MCQ\s*\n(.*?)(?=## |$)'
        mcq_match = re.search(mcq_pattern, content, re.DOTALL)
        
        if mcq_match:
            mcq_section = mcq_match.group(1)
            # Parse individual MCQ questions
            question_pattern = r'\*\*(.*?)\*\*\n((?:- .*\n)*)\*Answer:\* (.*?)(?:\n|$)'
            
            for match in re.finditer(question_pattern, mcq_section):
                question = match.group(1).strip()
                options_text = match.group(2).strip()
                answer = match.group(3).strip()
                
                # Parse options
                options = []
                for line in options_text.split('\n'):
                    if line.strip().startswith('- '):
                        options.append(line.strip()[2:])
                
                if question and options and answer:
                    mcq.append({
                        'question': question,
                        'options': options,
                        'answer': answer,
                        'marks': 1
                    })
        
        # Parse Subjective sections
        subj_pattern = r'## Subjective\s*\n(.*?)(?=## |$)'
        subj_match = re.search(subj_pattern, content, re.DOTALL)
        
        if subj_match:
            subj_section = subj_match.group(1)
            # Parse individual subjective questions
            question_pattern = r'\*\*(.*?)\*\*\n(.*?)(?=\*\*|$)'
            
            for match in re.finditer(question_pattern, subj_section, re.DOTALL):
                question = match.group(1).strip()
                answer = match.group(2).strip()
                
                if question:
                    subjective.append({
                        'question': question,
                        'answer': answer,
                        'marks': 5
                    })
        
        return mcq, subjective
    
    @staticmethod
    def save_questions(mcq: List[Dict], subjective: List[Dict], 
                      file_path: str, format_type: str = None) -> bool:
        """Save questions to specified format."""
        if format_type is None:
            format_type = QuestionFormatConverter.detect_format(file_path)
        
        try:
            if format_type == 'yaml':
                return QuestionFormatConverter._save_yaml(mcq, subjective, file_path)
            elif format_type == 'json':
                return QuestionFormatConverter._save_json(mcq, subjective, file_path)
            elif format_type == 'csv':
                return QuestionFormatConverter._save_csv(mcq, subjective, file_path)
            elif format_type == 'markdown':
                return QuestionFormatConverter._save_markdown(mcq, subjective, file_path)
            elif format_type == 'python':
                return QuestionFormatConverter._save_python(mcq, subjective, file_path)
            else:
                raise ValueError(f"Unsupported output format: {format_type}")
        except Exception as e:
            print(f"Error saving to {format_type}: {e}")
            return False
    
    @staticmethod
    def _save_yaml(mcq: List[Dict], subjective: List[Dict], file_path: str) -> bool:
        """Save to YAML format."""
        data = {
            'metadata': {
                'title': 'Quiz Questions',
                'format': 'setwise-yaml',
                'version': '1.0'
            },
            'mcq': mcq,
            'subjective': subjective
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        return True
    
    @staticmethod
    def _save_json(mcq: List[Dict], subjective: List[Dict], file_path: str) -> bool:
        """Save to JSON format."""
        data = {
            'metadata': {
                'title': 'Quiz Questions',
                'format': 'setwise-json',
                'version': '1.0'
            },
            'mcq': mcq,
            'subjective': subjective
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    
    @staticmethod
    def _save_csv(mcq: List[Dict], subjective: List[Dict], file_path: str) -> bool:
        """Save to CSV format."""
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['type', 'question', 'option1', 'option2', 'option3', 'option4', 'option5', 'answer', 'marks'])
            
            # MCQ questions
            for q in mcq:
                options = q.get('options', [])
                options_padded = options + [''] * (5 - len(options))  # Pad to 5 options
                
                writer.writerow([
                    'MCQ',
                    q.get('question', ''),
                    *options_padded[:5],
                    q.get('answer', ''),
                    q.get('marks', 1)
                ])
            
            # Subjective questions
            for q in subjective:
                writer.writerow([
                    'Subjective',
                    q.get('question', ''),
                    '', '', '', '', '',  # Empty option fields
                    q.get('answer', ''),
                    q.get('marks', 5)
                ])
        
        return True
    
    @staticmethod
    def _save_markdown(mcq: List[Dict], subjective: List[Dict], file_path: str) -> bool:
        """Save to Markdown format."""
        content = "# Quiz Questions\n\n"
        
        if mcq:
            content += "## MCQ Questions\n\n"
            for i, q in enumerate(mcq, 1):
                content += f"**{i}. {q.get('question', '')}**\n\n"
                for option in q.get('options', []):
                    content += f"- {option}\n"
                content += f"\n*Answer:* {q.get('answer', '')}\n"
                content += f"*Marks:* {q.get('marks', 1)}\n\n"
        
        if subjective:
            content += "## Subjective Questions\n\n"
            for i, q in enumerate(subjective, 1):
                content += f"**{i}. {q.get('question', '')}**\n\n"
                content += f"{q.get('answer', '')}\n\n"
                content += f"*Marks:* {q.get('marks', 5)}\n\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    @staticmethod
    def _save_python(mcq: List[Dict], subjective: List[Dict], file_path: str) -> bool:
        """Save to Python format."""
        content = '"""\nQuiz Questions\nGenerated by Setwise\n"""\n\n'
        content += f"mcq = {repr(mcq)}\n\n"
        content += f"subjective = {repr(subjective)}\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True


def create_example_files():
    """Create example files in different formats."""
    # Sample data
    mcq = [
        {
            "question": "What is $2 + 2$?",
            "options": ["3", "4", "5", "6"],
            "answer": "4",
            "marks": 1
        }
    ]
    
    subjective = [
        {
            "question": "Explain the concept of gravity.",
            "answer": "Gravity is a fundamental force that attracts objects with mass.",
            "marks": 5
        }
    ]
    
    converter = QuestionFormatConverter()
    
    # Create examples in different formats
    formats = [
        ('examples/sample_questions.yaml', 'yaml'),
        ('examples/sample_questions.json', 'json'),
        ('examples/sample_questions.csv', 'csv'),
        ('examples/sample_questions.md', 'markdown')
    ]
    
    for file_path, format_type in formats:
        Path(file_path).parent.mkdir(exist_ok=True)
        converter.save_questions(mcq, subjective, file_path, format_type)
        print(f"✅ Created {file_path}")


if __name__ == '__main__':
    create_example_files()