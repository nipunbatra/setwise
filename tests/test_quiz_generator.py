#!/usr/bin/env python3
"""
Comprehensive tests for QuizGenerator class
"""

import pytest
import tempfile
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from setwise.quiz_generator import QuizGenerator


class TestQuizGeneratorInitialization:
    """Test QuizGenerator initialization and setup"""
    
    def test_default_initialization(self):
        """Test default initialization"""
        generator = QuizGenerator()
        assert generator.template_dir == Path("templates")
        assert generator.output_dir == Path("output")
        assert hasattr(generator, 'template_manager')
        assert hasattr(generator, 'quiz_metadata')
    
    def test_custom_directories(self):
        """Test initialization with custom directories"""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "custom_templates")
            output_dir = os.path.join(temp_dir, "custom_output")
            
            generator = QuizGenerator(template_dir=template_dir, output_dir=output_dir)
            assert str(generator.template_dir).endswith("custom_templates")
            assert str(generator.output_dir).endswith("custom_output")
    
    def test_output_directory_creation(self):
        """Test that output directory is created"""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, "new_output")
            generator = QuizGenerator(output_dir=output_dir)
            assert os.path.exists(output_dir)
    
    def test_questions_file_loading(self):
        """Test custom questions file loading"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a custom questions file
            questions_file = os.path.join(temp_dir, "custom_questions.py")
            with open(questions_file, 'w') as f:
                f.write("""
quiz_metadata = {"title": "Custom Quiz"}
mcq = [{"question": "Test?", "options": ["A", "B"], "answer": "A", "marks": 1}]
subjective = [{"question": "Explain", "answer": "Answer", "marks": 5}]
""")
            
            generator = QuizGenerator(questions_file=questions_file)
            assert generator.quiz_metadata["title"] == "Custom Quiz"


class TestQuizGeneration:
    """Test quiz generation functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.template_dir = os.path.join(self.temp_dir, "templates")
        self.output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Copy default template
        setwise_root = Path(__file__).parent.parent
        template_src = setwise_root / "setwise" / "templates" / "quiz_template.tex.jinja"
        if template_src.exists():
            shutil.copy(template_src, self.template_dir)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_generate_without_compilation(self):
        """Test quiz generation without PDF compilation"""
        generator = QuizGenerator(template_dir=self.template_dir, output_dir=self.output_dir)
        result = generator.generate_quizzes(num_sets=2, compile_pdf=False)
        
        # Should create TEX files
        tex_files = list(Path(self.output_dir).glob("*.tex"))
        assert len(tex_files) >= 2
        
        # Should create answer keys
        answer_files = list(Path(self.output_dir).glob("answer_key_*.txt"))
        assert len(answer_files) >= 2
    
    def test_generate_different_num_sets(self):
        """Test generating different numbers of quiz sets"""
        generator = QuizGenerator(template_dir=self.template_dir, output_dir=self.output_dir)
        
        for num_sets in [1, 3, 5]:
            # Clear output directory
            for file in Path(self.output_dir).glob("*"):
                file.unlink()
            
            generator.generate_quizzes(num_sets=num_sets, compile_pdf=False)
            tex_files = list(Path(self.output_dir).glob("*.tex"))
            assert len(tex_files) == num_sets
    
    def test_generate_with_different_templates(self):
        """Test generation with different template names"""
        generator = QuizGenerator(template_dir=self.template_dir, output_dir=self.output_dir)
        
        # Test with different template names (even if file doesn't exist, should handle gracefully)
        templates = ["default", "compact", "minimal", "nonexistent"]
        
        for template in templates:
            # Clear output directory
            for file in Path(self.output_dir).glob("*"):
                file.unlink()
            
            try:
                result = generator.generate_quizzes(num_sets=1, template_name=template, compile_pdf=False)
                # Should not crash, but may return False for missing templates
                assert isinstance(result, bool)
            except Exception as e:
                # Should handle missing templates gracefully
                assert "template" in str(e).lower() or "file not found" in str(e).lower()
    
    def test_randomization(self):
        """Test that different runs produce different results"""
        generator = QuizGenerator(template_dir=self.template_dir, output_dir=self.output_dir)
        
        # Generate first set
        generator.generate_quizzes(num_sets=1, compile_pdf=False, seed=42)
        first_content = ""
        tex_file = list(Path(self.output_dir).glob("*.tex"))[0]
        with open(tex_file, 'r') as f:
            first_content = f.read()
        
        # Clear and generate second set with different seed
        for file in Path(self.output_dir).glob("*"):
            file.unlink()
            
        generator.generate_quizzes(num_sets=1, compile_pdf=False, seed=123)
        second_content = ""
        tex_file = list(Path(self.output_dir).glob("*.tex"))[0]
        with open(tex_file, 'r') as f:
            second_content = f.read()
        
        # Content should be different (randomization working)
        assert first_content != second_content
    
    def test_seed_reproducibility(self):
        """Test that same seed produces same results"""
        generator = QuizGenerator(template_dir=self.template_dir, output_dir=self.output_dir)
        
        # Generate first set
        generator.generate_quizzes(num_sets=1, compile_pdf=False, seed=42)
        first_content = ""
        tex_file = list(Path(self.output_dir).glob("*.tex"))[0]
        with open(tex_file, 'r') as f:
            first_content = f.read()
        
        # Clear and generate second set with same seed
        for file in Path(self.output_dir).glob("*"):
            file.unlink()
            
        generator.generate_quizzes(num_sets=1, compile_pdf=False, seed=42)
        second_content = ""
        tex_file = list(Path(self.output_dir).glob("*.tex"))[0]
        with open(tex_file, 'r') as f:
            second_content = f.read()
        
        # Content should be identical (reproducibility)
        assert first_content == second_content


class TestLatexCompilation:
    """Test LaTeX compilation functionality"""
    
    def test_compile_latex_missing_file(self):
        """Test compilation with missing LaTeX file"""
        generator = QuizGenerator()
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_file = Path(temp_dir) / "missing.tex"
            result = generator.compile_latex(missing_file, Path(temp_dir))
            assert result is False
    
    @patch('subprocess.run')
    def test_compile_latex_success(self, mock_run):
        """Test successful LaTeX compilation"""
        mock_run.return_value.returncode = 0
        
        generator = QuizGenerator()
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = Path(temp_dir) / "test.tex"
            tex_file.write_text("\\documentclass{article}\\begin{document}Test\\end{document}")
            
            result = generator.compile_latex(tex_file, Path(temp_dir))
            assert result is True
            mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_compile_latex_failure(self, mock_run):
        """Test failed LaTeX compilation"""
        mock_run.return_value.returncode = 1
        
        generator = QuizGenerator()
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = Path(temp_dir) / "test.tex"
            tex_file.write_text("invalid latex content")
            
            result = generator.compile_latex(tex_file, Path(temp_dir))
            assert result is False


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_template_directory(self):
        """Test handling of invalid template directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_template_dir = os.path.join(temp_dir, "nonexistent")
            
            # Should not crash during initialization
            generator = QuizGenerator(template_dir=invalid_template_dir)
            assert generator is not None
    
    def test_permission_denied_output_directory(self):
        """Test handling of permission denied on output directory"""
        # Skip on Windows as permission handling is different
        import platform
        if platform.system() == "Windows":
            pytest.skip("Permission test not applicable on Windows")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            restricted_dir = os.path.join(temp_dir, "restricted")
            os.makedirs(restricted_dir)
            os.chmod(restricted_dir, 0o000)  # Remove all permissions
            
            try:
                generator = QuizGenerator(output_dir=restricted_dir)
                # Should handle permission error gracefully
                result = generator.generate_quizzes(num_sets=1, compile_pdf=False)
                assert isinstance(result, bool)
            finally:
                os.chmod(restricted_dir, 0o755)  # Restore permissions for cleanup
    
    def test_empty_questions_data(self):
        """Test handling of empty questions data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            questions_file = os.path.join(temp_dir, "empty_questions.py")
            with open(questions_file, 'w') as f:
                f.write("""
quiz_metadata = {"title": "Empty Quiz"}
mcq = []
subjective = []
""")
            
            generator = QuizGenerator(questions_file=questions_file)
            result = generator.generate_quizzes(num_sets=1, compile_pdf=False)
            # Should handle empty questions gracefully
            assert isinstance(result, bool)
    
    def test_malformed_questions_data(self):
        """Test handling of malformed questions data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            questions_file = os.path.join(temp_dir, "malformed_questions.py")
            with open(questions_file, 'w') as f:
                f.write("""
quiz_metadata = {"title": "Bad Quiz"}
mcq = [{"question": "Missing required fields"}]  # Missing options, answer, marks
subjective = "not a list"  # Should be a list
""")
            
            # Should handle malformed data gracefully
            try:
                generator = QuizGenerator(questions_file=questions_file)
                result = generator.generate_quizzes(num_sets=1, compile_pdf=False)
                assert isinstance(result, bool)
            except Exception as e:
                # Should raise meaningful error
                assert "questions" in str(e).lower() or "format" in str(e).lower()


class TestIntegration:
    """Integration tests for full workflow"""
    
    def test_full_workflow_without_latex(self):
        """Test complete workflow without LaTeX compilation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_dir = os.path.join(temp_dir, "templates")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(template_dir)
            
            # Copy template
            setwise_root = Path(__file__).parent.parent
            template_src = setwise_root / "setwise" / "templates" / "quiz_template.tex.jinja"
            if template_src.exists():
                shutil.copy(template_src, template_dir)
            
            # Create custom questions
            questions_file = os.path.join(temp_dir, "test_questions.py")
            with open(questions_file, 'w') as f:
                f.write("""
quiz_metadata = {
    "title": "Integration Test Quiz",
    "subject": "Testing",
    "duration": "60 minutes",
    "total_marks": 10
}

mcq = [
    {
        "question": "What is 2+2?",
        "options": ["2", "3", "4", "5"],
        "answer": "4",
        "marks": 2
    },
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "answer": "Paris",
        "marks": 2
    }
]

subjective = [
    {
        "question": "Explain the concept of testing in software development.",
        "answer": "Testing is the process of evaluating software to ensure it meets requirements.",
        "marks": 6
    }
]
""")
            
            # Run full workflow
            generator = QuizGenerator(
                template_dir=template_dir,
                output_dir=output_dir,
                questions_file=questions_file
            )
            
            result = generator.generate_quizzes(num_sets=3, compile_pdf=False)
            
            # Verify outputs
            assert result is True
            
            # Check generated files
            tex_files = list(Path(output_dir).glob("*.tex"))
            answer_files = list(Path(output_dir).glob("answer_key_*.txt"))
            
            assert len(tex_files) == 3
            assert len(answer_files) == 3
            
            # Verify content exists and is reasonable
            for tex_file in tex_files:
                content = tex_file.read_text()
                assert "Integration Test Quiz" in content
                assert "What is 2+2?" in content or "capital of France" in content
                assert len(content) > 1000  # Should be substantial content
            
            for answer_file in answer_files:
                content = answer_file.read_text()
                assert "ANSWER KEY" in content
                assert len(content) > 50  # Should have actual answers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])