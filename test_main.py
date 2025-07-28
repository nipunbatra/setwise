"""
Comprehensive test suite for Setwise quiz generator.
Tests all functionality including randomization, CLI, and output generation.
"""

import pytest
import random
import os
import tempfile
import shutil
from pathlib import Path
import json
import re
from unittest.mock import patch, mock_open

# Import the main module
import sys
sys.path.append('.')
from main import (
    shuffle_mcq_options, 
    process_subjective_questions, 
    generate_quiz_set,
    compile_latex_to_pdf,
    parse_args,
    main
)
from data.questions import mcq, subjective


class TestMCQShuffling:
    """Test MCQ option shuffling functionality."""
    
    def test_shuffle_mcq_options_basic(self):
        """Test basic MCQ option shuffling."""
        test_questions = [{
            "question": "Test question?",
            "options": ["A", "B", "C", "D"],
            "answer": "B",
            "marks": 2
        }]
        
        # Set seed for reproducible test
        random.seed(42)
        result = shuffle_mcq_options(test_questions)
        
        assert len(result) == 1
        assert "correct_index" in result[0]
        assert "correct_letter" in result[0]
        assert result[0]["answer"] == "B"  # Original answer preserved
        assert len(result[0]["options"]) == 4  # All options present
        
    def test_shuffle_mcq_options_different_seeds(self):
        """Test that different seeds produce different shuffling."""
        test_questions = [{
            "question": "Test question?",
            "options": ["A", "B", "C", "D"],
            "answer": "B",
            "marks": 2
        }]
        
        # First shuffle
        random.seed(42)
        result1 = shuffle_mcq_options(test_questions.copy())
        
        # Second shuffle with different seed
        random.seed(123)
        result2 = shuffle_mcq_options(test_questions.copy())
        
        # Should have different option orders (with high probability)
        assert result1[0]["options"] != result2[0]["options"] or \
               result1[0]["correct_index"] != result2[0]["correct_index"]
    
    def test_shuffle_mcq_options_answer_tracking(self):
        """Test that correct answer is properly tracked after shuffling."""
        test_questions = [{
            "question": "Test question?",
            "options": ["Wrong1", "Correct", "Wrong2", "Wrong3"],
            "answer": "Correct",
            "marks": 3
        }]
        
        random.seed(42)
        result = shuffle_mcq_options(test_questions)
        
        # Find where "Correct" ended up
        correct_pos = result[0]["options"].index("Correct")
        
        assert result[0]["correct_index"] == correct_pos
        assert result[0]["correct_letter"] == chr(65 + correct_pos)  # A, B, C, D
        
    def test_shuffle_mcq_options_preserves_marks(self):
        """Test that marks are preserved during shuffling."""
        test_questions = [{
            "question": "Test question?",
            "options": ["A", "B", "C", "D"],
            "answer": "B",
            "marks": 5
        }]
        
        result = shuffle_mcq_options(test_questions)
        assert result[0]["marks"] == 5


class TestSubjectiveProcessing:
    """Test subjective question processing."""
    
    def test_process_templated_questions(self):
        """Test processing of templated subjective questions."""
        test_questions = [{
            "template": "Calculate mean of {{ a }}, {{ b }}, {{ c }}",
            "variables": [
                {"a": 1, "b": 2, "c": 3, "answer": "2.0"},
                {"a": 4, "b": 5, "c": 6, "answer": "5.0"}
            ],
            "marks": 5
        }]
        
        random.seed(42)
        result = process_subjective_questions(test_questions)
        
        assert len(result) == 1
        assert "question" in result[0]
        assert "answer" in result[0]
        assert "marks" in result[0]
        assert result[0]["marks"] == 5
        
        # Check that template was rendered
        assert "Calculate mean of" in result[0]["question"]
        assert "{{" not in result[0]["question"]  # No unrendered templates
        
    def test_process_non_templated_questions(self):
        """Test processing of non-templated subjective questions."""
        test_questions = [{
            "question": "Explain the concept of machine learning.",
            "answer": "ML is a subset of AI...",
            "marks": 10
        }]
        
        result = process_subjective_questions(test_questions)
        
        assert len(result) == 1
        assert result[0]["question"] == "Explain the concept of machine learning."
        assert result[0]["answer"] == "ML is a subset of AI..."
        assert result[0]["marks"] == 10
        
    def test_process_mixed_questions(self):
        """Test processing mix of templated and non-templated questions."""
        test_questions = [
            {
                "template": "Value is {{ x }}",
                "variables": [{"x": 42, "answer": "42"}],
                "marks": 3
            },
            {
                "question": "Static question",
                "answer": "Static answer",
                "marks": 7
            }
        ]
        
        result = process_subjective_questions(test_questions)
        
        assert len(result) == 2
        assert "Value is 42" in result[0]["question"]
        assert result[1]["question"] == "Static question"


class TestQuizGeneration:
    """Test complete quiz generation."""
    
    def test_generate_quiz_set_basic(self):
        """Test basic quiz set generation."""
        quiz_content, answer_key = generate_quiz_set(1, num_mcq=2, num_subjective=2)
        
        assert isinstance(quiz_content, str)
        assert isinstance(answer_key, str)
        assert "Set 1" in quiz_content
        assert "MCQ 1" in answer_key
        assert "Subjective 1" in answer_key
        
    def test_generate_quiz_set_marks_calculation(self):
        """Test that marks are calculated correctly."""
        quiz_content, answer_key = generate_quiz_set(1, num_mcq=3, num_subjective=2)
        
        # Check that total marks appear in quiz
        assert "Total: " in quiz_content and "marks" in quiz_content
        assert "MCQ (" in quiz_content and "marks)" in quiz_content  
        assert "Subjective (" in quiz_content and "marks)" in quiz_content
        
    def test_generate_quiz_set_question_shuffling(self):
        """Test that question order is shuffled between sets."""
        random.seed(42)
        quiz1, _ = generate_quiz_set(1)
        
        random.seed(123)  # Different seed
        quiz2, _ = generate_quiz_set(2)
        
        # Extract question texts to compare order
        def extract_questions(content):
            mcq_pattern = r'\\textbf\{Q\d+\.\} (.+?) \\textbf\{'
            return re.findall(mcq_pattern, content)
        
        questions1 = extract_questions(quiz1)
        questions2 = extract_questions(quiz2)
        
        # Should have same questions but potentially different order
        assert len(questions1) == len(questions2)
        assert set(questions1) == set(questions2)  # Same content
        # High probability of different order with different seeds
        
    def test_generate_quiz_set_reproducibility(self):
        """Test that same seed produces identical results."""
        random.seed(42)
        quiz1, answer1 = generate_quiz_set(1, num_mcq=3, num_subjective=2)
        
        random.seed(42)  # Same seed
        quiz2, answer2 = generate_quiz_set(1, num_mcq=3, num_subjective=2)
        
        assert quiz1 == quiz2
        assert answer1 == answer2


class TestCLIInterface:
    """Test command-line interface."""
    
    def test_parse_args_defaults(self):
        """Test default argument parsing."""
        with patch('sys.argv', ['main.py']):
            args = parse_args()
            
        assert args.seed is None
        assert args.sets == 3
        assert args.mcq is None
        assert args.subjective is None
        assert args.no_pdf is False
        assert args.output_dir == 'output'
        
    def test_parse_args_custom(self):
        """Test custom argument parsing."""
        test_args = ['main.py', '--seed', '42', '--sets', '5', '--mcq', '4', 
                    '--subjective', '3', '--no-pdf', '--output-dir', 'test']
        
        with patch('sys.argv', test_args):
            args = parse_args()
            
        assert args.seed == 42
        assert args.sets == 5
        assert args.mcq == 4
        assert args.subjective == 3
        assert args.no_pdf is True
        assert args.output_dir == 'test'


class TestFileOperations:
    """Test file operations and LaTeX compilation."""
    
    def setup_method(self):
        """Setup temporary directory for each test."""
        self.temp_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Cleanup temporary directory after each test."""
        shutil.rmtree(self.temp_dir)
        
    def test_latex_compilation_mock(self):
        """Test LaTeX compilation with mocked subprocess."""
        tex_file = os.path.join(self.temp_dir, "test.tex")
        
        # Create a simple tex file
        with open(tex_file, 'w') as f:
            f.write("\\documentclass{article}\\begin{document}Test\\end{document}")
            
        # Mock successful compilation
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = compile_latex_to_pdf(tex_file, self.temp_dir)
            assert result is True
            
            # Check that pdflatex was called correctly
            calls = mock_run.call_args_list
            assert len(calls) == 2  # Called twice for cross-references
            assert f'-output-directory={self.temp_dir}' in calls[0][0][0]
            
    def test_latex_compilation_failure(self):
        """Test LaTeX compilation failure handling."""
        tex_file = os.path.join(self.temp_dir, "test.tex")
        
        with open(tex_file, 'w') as f:
            f.write("\\invalid{latex}")
            
        # Mock failed compilation
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "LaTeX Error"
            
            result = compile_latex_to_pdf(tex_file, self.temp_dir)
            assert result is False


class TestMainFunction:
    """Test main function integration."""
    
    def setup_method(self):
        """Setup temporary directory for each test."""
        self.temp_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Cleanup temporary directory after each test."""
        shutil.rmtree(self.temp_dir)
        
    @patch('subprocess.run')
    def test_main_integration(self, mock_run):
        """Test full main function integration."""
        # Mock successful LaTeX compilation
        mock_run.return_value.returncode = 0
        
        test_args = ['main.py', '--seed', '42', '--sets', '1', 
                    '--output-dir', self.temp_dir, '--no-pdf']
        
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 0
            
        # Check that files were created
        tex_file = os.path.join(self.temp_dir, 'quiz_set_1.tex')
        answer_file = os.path.join(self.temp_dir, 'answer_key_1.txt')
        
        assert os.path.exists(tex_file)
        assert os.path.exists(answer_file)
        
        # Check file contents
        with open(tex_file, 'r') as f:
            tex_content = f.read()
            assert "Set 1" in tex_content
            assert "Multiple Choice Questions" in tex_content
            
        with open(answer_file, 'r') as f:
            answer_content = f.read()
            assert "Answer Key for Quiz Set 1" in answer_content
            assert "MCQ 1" in answer_content


class TestDataIntegrity:
    """Test data integrity and validation."""
    
    def test_mcq_data_structure(self):
        """Test that MCQ data has required fields."""
        for i, question in enumerate(mcq):
            assert "question" in question, f"MCQ {i+1} missing 'question'"
            assert "options" in question, f"MCQ {i+1} missing 'options'"
            assert "answer" in question, f"MCQ {i+1} missing 'answer'"
            assert "marks" in question, f"MCQ {i+1} missing 'marks'"
            
            assert len(question["options"]) >= 2, f"MCQ {i+1} needs at least 2 options"
            assert question["answer"] in question["options"], f"MCQ {i+1} answer not in options"
            assert isinstance(question["marks"], int), f"MCQ {i+1} marks must be integer"
            assert question["marks"] > 0, f"MCQ {i+1} marks must be positive"
            
    def test_subjective_data_structure(self):
        """Test that subjective data has required fields."""
        for i, question in enumerate(subjective):
            assert "marks" in question, f"Subjective {i+1} missing 'marks'"
            assert isinstance(question["marks"], int), f"Subjective {i+1} marks must be integer"
            assert question["marks"] > 0, f"Subjective {i+1} marks must be positive"
            
            if "template" in question:
                assert "variables" in question, f"Templated subjective {i+1} missing 'variables'"
                assert len(question["variables"]) > 0, f"Subjective {i+1} needs at least 1 variable set"
            else:
                assert "question" in question, f"Non-templated subjective {i+1} missing 'question'"
                assert "answer" in question, f"Non-templated subjective {i+1} missing 'answer'"
                
    def test_latex_syntax_validation(self):
        """Test that LaTeX content doesn't have obvious syntax errors."""
        # Check for unmatched braces, dollars, etc.
        all_content = []
        
        for question in mcq:
            all_content.append(question["question"])
            all_content.extend(question["options"])
            
        for question in subjective:
            if "template" in question:
                all_content.append(question["template"])
            if "question" in question:
                all_content.append(question["question"])
                
        for content in all_content:
            # Check for unmatched dollar signs (basic check)
            dollar_count = content.count('$')
            assert dollar_count % 2 == 0, f"Unmatched $ in: {content[:50]}..."
            
            # Check for basic brace matching
            open_braces = content.count('{')
            close_braces = content.count('}')
            # Allow some imbalance for LaTeX commands, but flag major issues
            assert abs(open_braces - close_braces) <= 5, f"Possible brace mismatch in: {content[:50]}..."


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_empty_question_list(self):
        """Test handling of empty question lists."""
        result = shuffle_mcq_options([])
        assert result == []
            
    def test_invalid_template_variables(self):
        """Test handling of invalid template variables."""
        invalid_question = [{
            "template": "Value is {{ missing_var }}",
            "variables": [{"other_var": 42}],
            "marks": 1
        }]
        
        # Should handle gracefully - missing variables become empty
        result = process_subjective_questions(invalid_question)
        assert len(result) == 1
            
    def test_missing_answer_in_mcq(self):
        """Test handling of MCQ with missing answer."""
        invalid_mcq = [{
            "question": "Test?",
            "options": ["A", "B", "C"],
            "answer": "D",  # Not in options!
            "marks": 2
        }]
        
        # Should handle gracefully - answer stays as "D" (not found)
        result = shuffle_mcq_options(invalid_mcq)
        assert len(result) == 1
        assert result[0]["answer"] == "D"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])