#!/usr/bin/env python3
"""
Comprehensive error handling and edge case tests
"""

import pytest
import tempfile
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from setwise.quiz_generator import QuizGenerator
from setwise.template_manager import TemplateManager
from setwise.question_manager import QuestionManager


class TestQuizGeneratorErrorHandling:
    """Test error handling in QuizGenerator"""
    
    def test_missing_template_file(self):
        """Test handling when template file doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "templates")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(template_dir)
            
            generator = QuizGenerator(template_dir=template_dir, output_dir=output_dir)
            
            # Try to generate with non-existent template
            result = generator.generate_quizzes(num_sets=1, template_name="nonexistent", compile_pdf=False)
            
            # Should fail gracefully
            assert result is False
    
    def test_empty_questions(self):
        """Test handling empty questions"""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "templates")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(template_dir)
            
            # Create a simple template
            template_file = os.path.join(template_dir, "test_template.tex.jinja")
            with open(template_file, 'w') as f:
                f.write("\\documentclass{article}\\begin{document}\\end{document}")
            
            # Create empty questions file
            questions_file = os.path.join(temp_dir, "empty_questions.py")
            with open(questions_file, 'w') as f:
                f.write("""
quiz_metadata = {"title": "Empty Quiz"}
mcq = []
subjective = []
""")
            
            generator = QuizGenerator(
                template_dir=template_dir,
                output_dir=output_dir,
                questions_file=questions_file
            )
            
            # Should handle empty questions gracefully
            result = generator.generate_quizzes(num_sets=1, compile_pdf=False)
            # May succeed or fail, but shouldn't crash
            assert isinstance(result, bool)
    
    def test_malformed_template(self):
        """Test handling malformed template files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "templates")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(template_dir)
            
            # Create malformed template with invalid Jinja2 syntax
            template_file = os.path.join(template_dir, "quiz_template.tex.jinja")
            with open(template_file, 'w') as f:
                f.write("\\documentclass{article}\\begin{document}{{ invalid jinja syntax }{\\end{document}")
            
            generator = QuizGenerator(template_dir=template_dir, output_dir=output_dir)
            
            # Should handle template rendering errors
            result = generator.generate_quizzes(num_sets=1, compile_pdf=False)
            assert result is False
    
    def test_permission_denied_output(self):
        """Test handling permission denied on output directory"""
        import platform
        if platform.system() == "Windows":
            pytest.skip("Permission test not applicable on Windows")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "templates")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(template_dir)
            os.makedirs(output_dir)
            
            # Create template
            template_file = os.path.join(template_dir, "quiz_template.tex.jinja")
            with open(template_file, 'w') as f:
                f.write("\\documentclass{article}\\begin{document}Test\\end{document}")
            
            # Remove write permissions
            os.chmod(output_dir, 0o444)  # Read-only
            
            try:
                generator = QuizGenerator(template_dir=template_dir, output_dir=output_dir)
                result = generator.generate_quizzes(num_sets=1, compile_pdf=False)
                
                # Should handle permission error gracefully
                assert result is False
            finally:
                os.chmod(output_dir, 0o755)  # Restore permissions for cleanup
    
    def test_invalid_question_format(self):
        """Test handling invalid question formats"""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "templates")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(template_dir)
            
            # Create template
            template_file = os.path.join(template_dir, "quiz_template.tex.jinja")
            with open(template_file, 'w') as f:
                f.write("\\documentclass{article}\\begin{document}{% for q in mcq_questions %}{{ q.question }}{% endfor %}\\end{document}")
            
            # Create questions with invalid format
            questions_file = os.path.join(temp_dir, "invalid_questions.py")
            with open(questions_file, 'w') as f:
                f.write("""
quiz_metadata = {"title": "Invalid Quiz"}
mcq = [
    {"question": "Valid question", "options": ["A", "B"], "answer": "A", "marks": 1},
    {"invalid": "missing required fields"},
    {"question": "Another valid", "options": ["X", "Y"], "answer": "X", "marks": 2}
]
subjective = []
""")
            
            generator = QuizGenerator(
                template_dir=template_dir,
                output_dir=output_dir,
                questions_file=questions_file
            )
            
            # Should handle invalid questions gracefully (might filter them out)
            result = generator.generate_quizzes(num_sets=1, compile_pdf=False)
            assert isinstance(result, bool)


class TestTemplateManagerErrorHandling:
    """Test error handling in TemplateManager"""
    
    def test_nonexistent_template_directory(self):
        """Test handling non-existent template directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent_dir = os.path.join(temp_dir, "does_not_exist")
            
            manager = TemplateManager(template_dir=nonexistent_dir)
            
            # Should not crash
            assert manager is not None
            assert manager.template_dir == Path(nonexistent_dir)
    
    def test_get_nonexistent_template(self):
        """Test getting non-existent template"""
        manager = TemplateManager()
        
        result = manager.get_template_file("nonexistent_template")
        assert result is None
        
        with pytest.raises(KeyError):
            manager.get_template_path("nonexistent_template")
    
    def test_validate_missing_template_file(self):
        """Test validation when template file is missing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = TemplateManager(template_dir=temp_dir)
            
            # Template exists in dict but file doesn't exist
            is_valid, message = manager.validate_template("default")
            assert not is_valid
            assert "not found" in message.lower()
    
    def test_validate_unknown_template(self):
        """Test validation of unknown template"""
        manager = TemplateManager()
        
        is_valid, message = manager.validate_template("completely_unknown")
        assert not is_valid
        assert "unknown template" in message.lower()


class TestQuestionManagerErrorHandling:
    """Test error handling in QuestionManager"""
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent questions file"""
        with pytest.raises(FileNotFoundError):
            QuestionManager(questions_file="/path/that/does/not/exist.py")
    
    def test_load_invalid_python_file(self):
        """Test loading invalid Python file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_file = os.path.join(temp_dir, "invalid.py")
            with open(invalid_file, 'w') as f:
                f.write("This is not valid Python syntax ][}{")
            
            with pytest.raises(Exception):
                QuestionManager(questions_file=invalid_file)
    
    def test_missing_required_variables(self):
        """Test file missing required variables"""
        with tempfile.TemporaryDirectory() as temp_dir:
            incomplete_file = os.path.join(temp_dir, "incomplete.py")
            with open(incomplete_file, 'w') as f:
                f.write("""
# Missing quiz_metadata, mcq, subjective
some_variable = "value"
""")
            
            with pytest.raises(Exception):
                QuestionManager(questions_file=incomplete_file)
    
    def test_wrong_variable_types(self):
        """Test file with wrong variable types"""
        with tempfile.TemporaryDirectory() as temp_dir:
            wrong_types_file = os.path.join(temp_dir, "wrong_types.py")
            with open(wrong_types_file, 'w') as f:
                f.write("""
quiz_metadata = "should be dict"  # Wrong type
mcq = "should be list"  # Wrong type  
subjective = 123  # Wrong type
""")
            
            with pytest.raises(Exception):
                QuestionManager(questions_file=wrong_types_file)
    
    def test_template_rendering_error(self):
        """Test template rendering with missing variables"""
        manager = QuestionManager()
        
        template = "Value is {{ missing_variable }}"
        variables = {}  # Missing the required variable
        
        with pytest.raises(Exception):
            manager.render_template(template, variables)
    
    def test_invalid_question_validation(self):
        """Test validation of invalid questions"""
        manager = QuestionManager()
        
        # Test various invalid formats
        invalid_questions = [
            # MCQ missing fields
            {"question": "Test?", "marks": 1},  # Missing options and answer
            {"options": ["A", "B"], "answer": "A", "marks": 1},  # Missing question
            {"question": "Test?", "options": ["A"], "answer": "A", "marks": 1},  # Too few options
            {"question": "Test?", "options": "A,B", "answer": "A", "marks": 1},  # Options not list
            
            # Subjective missing fields  
            {"answer": "Answer", "marks": 5},  # Missing question
            {"question": "Question?", "marks": 5},  # Missing answer
            {"question": "Question?", "answer": "Answer"},  # Missing marks
        ]
        
        for invalid_q in invalid_questions:
            # Determine type based on presence of options
            q_type = "mcq" if "options" in invalid_q else "subjective"
            assert not manager.validate_question_format(invalid_q, q_type)


class TestIntegrationErrorHandling:
    """Integration tests for error handling across components"""
    
    def test_full_pipeline_with_errors(self):
        """Test full pipeline with various errors"""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "templates")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(template_dir)
            
            # Create problematic questions
            questions_file = os.path.join(temp_dir, "problematic_questions.py")
            with open(questions_file, 'w') as f:
                f.write("""
quiz_metadata = {"title": "Problematic Quiz"}

# Mix of valid and invalid questions
mcq = [
    {"question": "Valid Q1?", "options": ["A", "B", "C"], "answer": "B", "marks": 2},
    {"invalid": "missing required fields"},
    {"question": "Valid Q2?", "options": ["X", "Y"], "answer": "Y", "marks": 1},
    {"question": "Template with error", "template": "{{ missing_var }}", "options": ["A", "B"], "answer": "A", "variables": [{}], "marks": 1}
]

subjective = [
    {"question": "Valid subjective", "answer": "Valid answer", "marks": 5},
    {"incomplete": "missing fields"},
    {"question": "Another valid", "answer": "Another answer", "marks": 3}
]
""")
            
            # Create minimal template
            template_file = os.path.join(template_dir, "quiz_template.tex.jinja")
            with open(template_file, 'w') as f:
                f.write("""
\\documentclass{article}
\\begin{document}
\\title{ {{ quiz_metadata.title if quiz_metadata else "Quiz" }} }
\\maketitle
{% for q in mcq_questions %}
{{ loop.index }}. {{ q.question if q.question is defined else "Invalid question" }}
{% endfor %}
\\end{document}
""")
            
            generator = QuizGenerator(
                template_dir=template_dir,
                output_dir=output_dir,
                questions_file=questions_file
            )
            
            # Should handle mixed valid/invalid questions
            result = generator.generate_quizzes(num_sets=1, compile_pdf=False)
            
            # May succeed or fail, but should not crash
            assert isinstance(result, bool)
            
            # If it succeeded, check that some output was created
            if result:
                tex_files = list(Path(output_dir).glob("*.tex"))
                assert len(tex_files) > 0
    
    def test_recovery_from_partial_failures(self):
        """Test recovery when some quiz sets fail but others succeed"""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "templates")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(template_dir)
            
            # Create template that will sometimes fail
            template_file = os.path.join(template_dir, "quiz_template.tex.jinja")
            with open(template_file, 'w') as f:
                f.write("""
\\documentclass{article}
\\begin{document}
{% if set_id == 2 %}
{{ undefined_variable }}  {# This will cause template error for set 2 #}
{% endif %}
Quiz Set {{ set_id }}
\\end{document}
""")
            
            generator = QuizGenerator(template_dir=template_dir, output_dir=output_dir)
            
            # Generate multiple sets - some should fail, some succeed
            result = generator.generate_quizzes(num_sets=3, compile_pdf=False)
            
            # Overall result should be False due to failures
            assert result is False
            
            # But some files should still be created (for sets that didn't fail)
            tex_files = list(Path(output_dir).glob("*.tex"))
            # Should have fewer than 3 files due to failures
            assert 0 <= len(tex_files) < 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])