#!/usr/bin/env python3
"""
Core tests for Setwise package
"""

import pytest
import tempfile
import os
from pathlib import Path
import shutil

from setwise.quiz_generator import QuizGenerator
from setwise.template_manager import TemplateManager
from setwise.question_manager import QuestionManager


class TestQuizGenerator:
    """Test QuizGenerator functionality"""
    
    def test_init(self):
        """Test QuizGenerator initialization"""
        generator = QuizGenerator()
        assert generator is not None
        assert isinstance(generator.template_dir, Path)
        assert isinstance(generator.output_dir, Path)
    
    def test_init_with_custom_dirs(self):
        """Test QuizGenerator initialization with custom directories"""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "templates")
            output_dir = os.path.join(temp_dir, "output")
            
            generator = QuizGenerator(template_dir=template_dir, output_dir=output_dir)
            assert str(template_dir) in str(generator.template_dir)
            assert str(output_dir) in str(generator.output_dir)


class TestTemplateManager:
    """Test TemplateManager functionality"""
    
    def test_init(self):
        """Test TemplateManager initialization"""
        manager = TemplateManager()
        assert manager is not None
    
    def test_available_templates(self):
        """Test getting available templates"""
        manager = TemplateManager()
        templates = manager.list_templates()
        assert isinstance(templates, list)
        # Should have at least the default template
        assert len(templates) > 0


class TestQuestionManager:
    """Test QuestionManager functionality"""
    
    def test_init(self):
        """Test QuestionManager initialization"""
        manager = QuestionManager()
        assert manager is not None
    
    def test_load_questions(self):
        """Test loading default questions"""
        manager = QuestionManager()
        mcq, subjective = manager.load_questions()
        assert isinstance(mcq, list)
        assert isinstance(subjective, list)
    
    def test_validate_questions_format(self):
        """Test question format validation"""
        manager = QuestionManager()
        
        # Valid MCQ
        valid_mcq = {
            "question": "What is 2+2?",
            "options": ["3", "4", "5"],
            "answer": "4",
            "marks": 2
        }
        assert manager.validate_question_format(valid_mcq, "mcq")
        
        # Valid subjective
        valid_subjective = {
            "question": "Explain addition",
            "answer": "Adding numbers together",
            "marks": 5
        }
        assert manager.validate_question_format(valid_subjective, "subjective")
        
        # Invalid - missing required field
        invalid_mcq = {
            "question": "What is 2+2?",
            "options": ["3", "4", "5"],
            # missing answer
            "marks": 2
        }
        assert not manager.validate_question_format(invalid_mcq, "mcq")


class TestBasicGeneration:
    """Test basic quiz generation functionality"""
    
    def test_generation_with_simple_questions(self):
        """Test quiz generation with simple questions"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Setup template directory
            template_dir = os.path.join(temp_dir, "templates")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(template_dir, exist_ok=True)
            
            # Copy default template
            setwise_root = Path(__file__).parent.parent
            template_src = setwise_root / "setwise" / "templates" / "quiz_template.tex.jinja"
            if template_src.exists():
                shutil.copy(template_src, template_dir)
            
            # Create generator
            generator = QuizGenerator(template_dir=template_dir, output_dir=output_dir)
            
            # Test with compilation disabled (no LaTeX requirement)
            result = generator.generate_quizzes(num_sets=1, compile_pdf=False)
            
            # Should succeed in creating tex files even without LaTeX
            tex_files = list(Path(output_dir).glob("*.tex"))
            assert len(tex_files) > 0


class TestDataIntegrity:
    """Test data integrity and validation"""
    
    def test_template_files_exist(self):
        """Test that required template files exist"""
        setwise_root = Path(__file__).parent.parent
        template_dir = setwise_root / "setwise" / "templates"
        
        required_templates = [
            "quiz_template.tex.jinja",
            "quiz_template_compact.tex.jinja", 
            "quiz_template_minimal.tex.jinja"
        ]
        
        for template in required_templates:
            template_path = template_dir / template
            assert template_path.exists(), f"Template {template} not found"
    
    def test_questions_data_format(self):
        """Test that question data has correct format"""
        from setwise.data.questions import mcq, subjective
        
        # Test MCQ format
        assert isinstance(mcq, list)
        if mcq:  # If there are MCQs
            sample_mcq = mcq[0]
            required_fields = ['question', 'options', 'answer', 'marks']
            for field in required_fields:
                assert field in sample_mcq, f"MCQ missing field: {field}"
            assert isinstance(sample_mcq['options'], list)
            assert len(sample_mcq['options']) >= 2
        
        # Test subjective format
        assert isinstance(subjective, list)
        if subjective:  # If there are subjective questions
            sample_subj = subjective[0]
            required_fields = ['question', 'answer', 'marks']
            for field in required_fields:
                assert field in sample_subj, f"Subjective question missing field: {field}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])