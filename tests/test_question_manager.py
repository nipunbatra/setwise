#!/usr/bin/env python3
"""
Comprehensive tests for QuestionManager class
"""

import pytest
import tempfile
import os
from pathlib import Path

from setwise.question_manager import QuestionManager


class TestQuestionManagerInitialization:
    """Test QuestionManager initialization"""
    
    def test_default_initialization(self):
        """Test default initialization"""
        manager = QuestionManager()
        assert manager is not None
        assert hasattr(manager, 'questions_file')
        assert hasattr(manager, 'mcq')
        assert hasattr(manager, 'subjective')
        assert hasattr(manager, 'quiz_metadata')
    
    def test_custom_questions_file(self):
        """Test initialization with custom questions file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            questions_file = os.path.join(temp_dir, "test_questions.py")
            with open(questions_file, 'w') as f:
                f.write("""
quiz_metadata = {"title": "Test Quiz"}
mcq = [{"question": "Test?", "options": ["A", "B"], "answer": "A", "marks": 1}]
subjective = []
""")
            
            manager = QuestionManager(questions_file=questions_file)
            assert manager.quiz_metadata["title"] == "Test Quiz"
            assert len(manager.mcq) == 1


class TestQuestionLoading:
    """Test question loading functionality"""
    
    def test_load_default_questions(self):
        """Test loading default questions"""
        manager = QuestionManager()
        
        # Should have questions loaded
        assert isinstance(manager.mcq, list)
        assert isinstance(manager.subjective, list)
        assert isinstance(manager.quiz_metadata, dict)
        
        # Should have some content
        assert len(manager.mcq) > 0 or len(manager.subjective) > 0
    
    def test_load_custom_questions_file(self):
        """Test loading custom questions file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            questions_file = os.path.join(temp_dir, "custom_questions.py")
            with open(questions_file, 'w') as f:
                f.write("""
quiz_metadata = {
    "title": "Custom Quiz",
    "subject": "Testing",
    "duration": "30 minutes",
    "total_marks": 10
}

mcq = [
    {
        "question": "What is testing?",
        "options": ["A process", "A tool", "A method", "All of the above"],
        "answer": "All of the above",
        "marks": 2
    }
]

subjective = [
    {
        "question": "Explain unit testing.",
        "answer": "Unit testing tests individual components.",
        "marks": 8
    }
]
""")
            
            manager = QuestionManager(questions_file=questions_file)
            
            assert manager.quiz_metadata["title"] == "Custom Quiz"
            assert len(manager.mcq) == 1
            assert len(manager.subjective) == 1
            assert manager.mcq[0]["question"] == "What is testing?"
    
    def test_load_invalid_questions_file(self):
        """Test loading invalid questions file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_file = os.path.join(temp_dir, "invalid.py")
            with open(invalid_file, 'w') as f:
                f.write("This is not valid Python code ][}{")
            
            with pytest.raises(Exception):
                QuestionManager(questions_file=invalid_file)
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent questions file"""
        nonexistent_file = "/path/that/does/not/exist.py"
        
        with pytest.raises(FileNotFoundError):
            QuestionManager(questions_file=nonexistent_file)


class TestQuestionValidation:
    """Test question validation functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.manager = QuestionManager()
    
    def test_validate_mcq_format(self):
        """Test MCQ format validation"""
        # Valid MCQ
        valid_mcq = {
            "question": "What is 2+2?",
            "options": ["2", "3", "4", "5"],
            "answer": "4",
            "marks": 2
        }
        assert self.manager.validate_question_format(valid_mcq, "mcq")
        
        # MCQ with template
        template_mcq = {
            "template": "What is {{ a }} + {{ b }}?",
            "options": ["{{ a + b }}", "{{ a - b }}", "{{ a * b }}", "{{ a / b }}"],
            "answer": "{{ a + b }}",
            "variables": [{"a": 2, "b": 2}],
            "marks": 2
        }
        assert self.manager.validate_question_format(template_mcq, "mcq")
    
    def test_validate_subjective_format(self):
        """Test subjective format validation"""
        # Valid subjective
        valid_subjective = {
            "question": "Explain addition.",
            "answer": "Addition combines numbers.",
            "marks": 5
        }
        assert self.manager.validate_question_format(valid_subjective, "subjective")
        
        # Subjective with template
        template_subjective = {
            "template": "Calculate the sum of {{ a }} and {{ b }}.",
            "answer": "{{ a }} + {{ b }} = {{ a + b }}",
            "variables": [{"a": 5, "b": 3}],
            "marks": 3
        }
        assert self.manager.validate_question_format(template_subjective, "subjective")
    
    def test_validate_invalid_mcq(self):
        """Test invalid MCQ validation"""
        # Missing required fields
        invalid_mcqs = [
            # Missing question
            {"options": ["A", "B"], "answer": "A", "marks": 1},
            # Missing options
            {"question": "Test?", "answer": "A", "marks": 1},
            # Missing answer
            {"question": "Test?", "options": ["A", "B"], "marks": 1},
            # Missing marks
            {"question": "Test?", "options": ["A", "B"], "answer": "A"},
            # Invalid options (not a list)
            {"question": "Test?", "options": "A,B", "answer": "A", "marks": 1},
            # Too few options
            {"question": "Test?", "options": ["A"], "answer": "A", "marks": 1},
        ]
        
        for invalid_mcq in invalid_mcqs:
            assert not self.manager.validate_question_format(invalid_mcq, "mcq")
    
    def test_validate_invalid_subjective(self):
        """Test invalid subjective validation"""
        # Invalid subjectives
        invalid_subjectives = [
            # Missing question
            {"answer": "Answer", "marks": 5},
            # Missing answer
            {"question": "Question?", "marks": 5},
            # Missing marks
            {"question": "Question?", "answer": "Answer"},
            # Invalid marks type
            {"question": "Question?", "answer": "Answer", "marks": "five"},
        ]
        
        for invalid_subjective in invalid_subjectives:
            assert not self.manager.validate_question_format(invalid_subjective, "subjective")


class TestQuestionTemplating:
    """Test question templating functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.manager = QuestionManager()
    
    def test_render_simple_template(self):
        """Test rendering simple templates"""
        template = "What is {{ a }} + {{ b }}?"
        variables = {"a": 2, "b": 3}
        
        rendered = self.manager.render_template(template, variables)
        assert rendered == "What is 2 + 3?"
    
    def test_render_complex_template(self):
        """Test rendering complex templates with calculations"""
        template = "Calculate: {{ a }} × {{ b }} = {{ a * b }}"
        variables = {"a": 4, "b": 5}
        
        rendered = self.manager.render_template(template, variables)
        assert rendered == "Calculate: 4 × 5 = 20"
    
    def test_render_template_with_latex(self):
        """Test rendering templates with LaTeX"""
        template = r"Find $\sqrt{{{ value }}}$ where value = {{ value }}"
        variables = {"value": 16}
        
        rendered = self.manager.render_template(template, variables)
        assert r"$\sqrt{16}$" in rendered
        assert "value = 16" in rendered
    
    def test_render_template_missing_variable(self):
        """Test rendering template with missing variable"""
        template = "What is {{ a }} + {{ b }}?"
        variables = {"a": 2}  # Missing 'b'
        
        with pytest.raises(Exception):
            self.manager.render_template(template, variables)
    
    def test_process_templated_questions(self):
        """Test processing templated questions"""
        templated_mcq = {
            "template": "What is {{ a }} + {{ b }}?",
            "options": ["{{ a + b }}", "{{ a - b }}", "{{ a * b }}", "0"],
            "answer": "{{ a + b }}",
            "variables": [
                {"a": 2, "b": 3},
                {"a": 5, "b": 7}
            ],
            "marks": 2
        }
        
        processed = self.manager.process_templated_question(templated_mcq)
        
        # Should generate multiple questions
        assert len(processed) == 2
        
        # Check first variant
        first = processed[0]
        assert first["question"] == "What is 2 + 3?"
        assert "5" in first["options"]  # a + b = 5
        assert first["answer"] == "5"
        
        # Check second variant  
        second = processed[1]
        assert second["question"] == "What is 5 + 7?"
        assert "12" in second["options"]  # a + b = 12
        assert second["answer"] == "12"


class TestQuestionSelection:
    """Test question selection and randomization"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.manager = QuestionManager()
    
    def test_select_questions_basic(self):
        """Test basic question selection"""
        # Create test questions
        mcq_list = [
            {"question": f"Q{i}", "options": ["A", "B"], "answer": "A", "marks": 1}
            for i in range(10)
        ]
        subjective_list = [
            {"question": f"S{i}", "answer": f"A{i}", "marks": 5}
            for i in range(5)
        ]
        
        selected_mcq, selected_subj = self.manager.select_questions(
            mcq_list, subjective_list, num_mcq=3, num_subjective=2, seed=42
        )
        
        assert len(selected_mcq) == 3
        assert len(selected_subj) == 2
    
    def test_select_questions_reproducible(self):
        """Test that question selection is reproducible with same seed"""
        mcq_list = [
            {"question": f"Q{i}", "options": ["A", "B"], "answer": "A", "marks": 1}
            for i in range(10)
        ]
        subjective_list = [
            {"question": f"S{i}", "answer": f"A{i}", "marks": 5}
            for i in range(5)
        ]
        
        # Select with seed 42
        selected1_mcq, selected1_subj = self.manager.select_questions(
            mcq_list, subjective_list, num_mcq=3, num_subjective=2, seed=42
        )
        
        # Select again with same seed
        selected2_mcq, selected2_subj = self.manager.select_questions(
            mcq_list, subjective_list, num_mcq=3, num_subjective=2, seed=42
        )
        
        # Should be identical
        assert selected1_mcq == selected2_mcq
        assert selected1_subj == selected2_subj
    
    def test_select_more_than_available(self):
        """Test selecting more questions than available"""
        mcq_list = [
            {"question": "Q1", "options": ["A", "B"], "answer": "A", "marks": 1},
            {"question": "Q2", "options": ["A", "B"], "answer": "A", "marks": 1}
        ]
        subjective_list = [
            {"question": "S1", "answer": "A1", "marks": 5}
        ]
        
        # Request more than available
        selected_mcq, selected_subj = self.manager.select_questions(
            mcq_list, subjective_list, num_mcq=5, num_subjective=3
        )
        
        # Should return all available
        assert len(selected_mcq) == 2  # All available MCQ
        assert len(selected_subj) == 1  # All available subjective


class TestErrorHandling:
    """Test error handling in question management"""
    
    def test_malformed_questions_file(self):
        """Test handling malformed questions file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            malformed_file = os.path.join(temp_dir, "malformed.py")
            with open(malformed_file, 'w') as f:
                f.write("""
quiz_metadata = "should be dict"  # Invalid type
mcq = "should be list"  # Invalid type
subjective = 123  # Invalid type
""")
            
            with pytest.raises(Exception):
                QuestionManager(questions_file=malformed_file)
    
    def test_missing_required_variables(self):
        """Test handling missing required variables in questions file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            incomplete_file = os.path.join(temp_dir, "incomplete.py")
            with open(incomplete_file, 'w') as f:
                f.write("""
# Missing quiz_metadata, mcq, subjective
some_other_variable = "value"
""")
            
            with pytest.raises(Exception):
                QuestionManager(questions_file=incomplete_file)


class TestIntegration:
    """Integration tests for question management"""
    
    def test_full_workflow(self):
        """Test complete question management workflow"""
        with tempfile.TemporaryDirectory() as temp_dir:
            questions_file = os.path.join(temp_dir, "workflow_test.py")
            with open(questions_file, 'w') as f:
                f.write("""
quiz_metadata = {
    "title": "Workflow Test Quiz",
    "subject": "Testing",
    "duration": "60 minutes",
    "total_marks": 15
}

mcq = [
    {
        "question": "Simple question 1?",
        "options": ["A", "B", "C", "D"],
        "answer": "B",
        "marks": 2
    },
    {
        "template": "What is {{ a }} + {{ b }}?",
        "options": ["{{ a + b }}", "{{ a - b }}", "{{ a * b }}", "0"],
        "answer": "{{ a + b }}",
        "variables": [{"a": 3, "b": 4}, {"a": 5, "b": 2}],
        "marks": 3
    }
]

subjective = [
    {
        "question": "Explain testing methodology.",
        "answer": "Testing methodology involves systematic approaches to validate software.",
        "marks": 10
    }
]
""")
            
            # Load questions
            manager = QuestionManager(questions_file=questions_file)
            
            # Validate loaded data
            assert manager.quiz_metadata["title"] == "Workflow Test Quiz"
            assert len(manager.mcq) == 2
            assert len(manager.subjective) == 1
            
            # Process templated questions
            processed_mcq = []
            for q in manager.mcq:
                if "template" in q:
                    processed_mcq.extend(manager.process_templated_question(q))
                else:
                    processed_mcq.append(q)
            
            # Should have 3 MCQs now (1 simple + 2 from template)
            assert len(processed_mcq) == 3
            
            # Select subset for quiz
            selected_mcq, selected_subj = manager.select_questions(
                processed_mcq, manager.subjective, num_mcq=2, num_subjective=1, seed=42
            )
            
            assert len(selected_mcq) == 2
            assert len(selected_subj) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])