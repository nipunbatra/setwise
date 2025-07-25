#!/usr/bin/env python3
"""
Test suite for generate_template_previews.py module.
Tests template preview generation functionality.
"""

import pytest
import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, call

import generate_template_previews


class TestCommandExecution:
    """Test command execution functionality."""
    
    def test_run_command_success(self):
        """Test successful command execution."""
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            result = generate_template_previews.run_command("echo hello", "test command")
            
            assert result is True
            mock_run.assert_called_once()
            # Verify shlex.split was used (no shell=True)
            args, kwargs = mock_run.call_args
            assert 'shell' not in kwargs or kwargs['shell'] is False
            assert kwargs['check'] is True
            assert kwargs['capture_output'] is True
            assert kwargs['text'] is True
    
    def test_run_command_failure(self):
        """Test command execution failure handling."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "fake_cmd", stdout="output", stderr="error"
            )
            
            with patch('builtins.print') as mock_print:
                result = generate_template_previews.run_command("fake_cmd", "test command")
                
                assert result is False
                assert mock_print.call_count >= 3  # Error message + stdout + stderr
    
    def test_run_command_with_list_args(self):
        """Test command execution with list arguments."""
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            cmd_list = ["python", "--version"]
            result = generate_template_previews.run_command(cmd_list, "test list command")
            
            assert result is True
            args, kwargs = mock_run.call_args
            assert args[0] == cmd_list  # Should pass list directly
    
    def test_shlex_split_security(self):
        """Test that shlex.split is used for security."""
        with patch('subprocess.run') as mock_run, \
             patch('shlex.split') as mock_split:
            
            mock_split.return_value = ["echo", "hello"]
            mock_result = MagicMock()
            mock_run.return_value = mock_result
            
            generate_template_previews.run_command("echo hello", "test")
            
            # Verify shlex.split was called
            mock_split.assert_called_once_with("echo hello")


class TestTemplateGeneration:
    """Test template generation functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    @patch('generate_template_previews.run_command')
    def test_generate_template_samples_success(self, mock_run):
        """Test successful template sample generation."""
        mock_run.return_value = True
        
        result = generate_template_previews.generate_template_samples()
        
        assert result is True
        # Should be called for each template
        expected_templates = ['default', 'compact', 'academic', 'minimal']
        assert mock_run.call_count == len(expected_templates)
        
        # Check command structure
        for call_args in mock_run.call_args_list:
            cmd, description = call_args[0]
            assert "python main.py" in cmd
            assert "--seed 42" in cmd
            assert "--sets 1" in cmd
            assert "--mcq 4" in cmd
            assert "--subjective 2" in cmd
    
    @patch('generate_template_previews.run_command')
    def test_generate_template_samples_failure(self, mock_run):
        """Test template sample generation failure."""
        mock_run.return_value = False
        
        result = generate_template_previews.generate_template_samples()
        
        assert result is False
        # Should stop on first failure
        assert mock_run.call_count == 1
    
    def test_template_directory_creation(self):
        """Test template directory creation."""
        with patch('generate_template_previews.run_command') as mock_run:
            mock_run.return_value = True
            
            generate_template_previews.generate_template_samples()
            
            # Check that temp directories would be created
            temp_dir = Path('assets_temp')
            expected_dirs = ['default', 'compact', 'academic', 'minimal']
            
            # Since we're mocking, we just verify the structure would be correct
            for template in expected_dirs:
                template_dir = temp_dir / template
                # The function should create these paths
                assert str(template_dir) in str(mock_run.call_args_list)


class TestPDFConversion:
    """Test PDF to image conversion functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    @patch('generate_template_previews.run_command')
    def test_convert_pdfs_to_images_success(self, mock_run):
        """Test successful PDF to image conversion."""
        mock_run.return_value = True
        
        # Create mock PDF files
        temp_dir = Path('assets_temp')
        images_dir = Path('assets/images')
        
        for template in ['compact', 'academic', 'minimal']:
            template_dir = temp_dir / template
            template_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = template_dir / 'quiz_set_1.pdf'
            pdf_path.touch()  # Create empty file
        
        result = generate_template_previews.convert_pdfs_to_images()
        
        assert result is True
        assert mock_run.call_count == 3  # One for each template
        
        # Check pdftoppm commands
        for call_args in mock_run.call_args_list:
            cmd, description = call_args[0]
            assert "pdftoppm" in cmd
            assert "-png" in cmd
            assert "-r 150" in cmd
    
    @patch('generate_template_previews.run_command')
    def test_convert_pdfs_to_images_missing_pdf(self, mock_run):
        """Test PDF conversion with missing PDF files."""
        mock_run.return_value = True
        
        # Don't create PDF files - they should be missing
        result = generate_template_previews.convert_pdfs_to_images()
        
        # Should still return True but not call run_command
        assert result is True
        assert mock_run.call_count == 0
    
    @patch('generate_template_previews.run_command')
    def test_convert_pdfs_to_images_command_failure(self, mock_run):
        """Test PDF conversion with command failure."""
        mock_run.return_value = False
        
        # Create mock PDF files
        temp_dir = Path('assets_temp')
        for template in ['compact', 'academic', 'minimal']:
            template_dir = temp_dir / template
            template_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = template_dir / 'quiz_set_1.pdf'
            pdf_path.touch()
        
        result = generate_template_previews.convert_pdfs_to_images()
        
        assert result is False
        assert mock_run.call_count == 1  # Should stop on first failure


class TestFileCopyOperations:
    """Test file copy operations."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_copy_sample_pdfs_success(self):
        """Test successful PDF copying."""
        # Create source PDF files
        temp_dir = Path('assets_temp')
        assets_dir = Path('assets')
        assets_dir.mkdir(exist_ok=True)
        
        for template in ['compact', 'academic', 'minimal']:
            template_dir = temp_dir / template
            template_dir.mkdir(parents=True, exist_ok=True)
            src_pdf = template_dir / 'quiz_set_1.pdf'
            src_pdf.write_text("fake pdf content")
        
        result = generate_template_previews.copy_sample_pdfs()
        
        assert result is True
        
        # Check that files were copied
        for template in ['compact', 'academic', 'minimal']:
            dst_pdf = assets_dir / f'{template}_sample.pdf'
            assert dst_pdf.exists()
            assert dst_pdf.read_text() == "fake pdf content"
    
    def test_copy_sample_pdfs_missing_source(self):
        """Test PDF copying with missing source files."""
        result = generate_template_previews.copy_sample_pdfs()
        
        # Should return True even with missing files
        assert result is True
    
    def test_cleanup_temp_files(self):
        """Test temporary file cleanup."""
        # Create temp directory with files
        temp_dir = Path('assets_temp')
        temp_dir.mkdir(exist_ok=True)
        test_file = temp_dir / 'test.txt'
        test_file.write_text("test content")
        
        assert temp_dir.exists()
        assert test_file.exists()
        
        generate_template_previews.cleanup_temp_files()
        
        assert not temp_dir.exists()
        assert not test_file.exists()
    
    def test_cleanup_temp_files_nonexistent(self):
        """Test cleanup when temp directory doesn't exist."""
        # Should not raise error
        generate_template_previews.cleanup_temp_files()


class TestDependencyVerification:
    """Test dependency verification functionality."""
    
    @patch('subprocess.run')
    def test_verify_dependencies_success(self, mock_run):
        """Test successful dependency verification."""
        mock_run.return_value = MagicMock()
        
        result = generate_template_previews.verify_dependencies()
        
        assert result is True
        assert mock_run.call_count == 2  # pdftoppm and pdflatex
        
        # Check calls
        calls = mock_run.call_args_list
        assert ['pdftoppm', '-h'] in [call[0][0] for call in calls]
        assert ['pdflatex', '--version'] in [call[0][0] for call in calls]
    
    @patch('subprocess.run')
    def test_verify_dependencies_pdftoppm_missing(self, mock_run):
        """Test dependency verification with missing pdftoppm."""
        def side_effect(cmd, **kwargs):
            if 'pdftoppm' in cmd:
                raise FileNotFoundError("pdftoppm not found")
            return MagicMock()
        
        mock_run.side_effect = side_effect
        
        result = generate_template_previews.verify_dependencies()
        
        assert result is False
    
    @patch('subprocess.run')
    def test_verify_dependencies_pdflatex_missing(self, mock_run):
        """Test dependency verification with missing pdflatex."""
        def side_effect(cmd, **kwargs):
            if 'pdflatex' in cmd:
                raise subprocess.CalledProcessError(1, cmd)
            return MagicMock()
        
        mock_run.side_effect = side_effect
        
        result = generate_template_previews.verify_dependencies()
        
        assert result is False


class TestMainFunction:
    """Test main function integration."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    @patch('generate_template_previews.cleanup_temp_files')
    @patch('generate_template_previews.copy_sample_pdfs')
    @patch('generate_template_previews.convert_pdfs_to_images')
    @patch('generate_template_previews.generate_template_samples')
    @patch('generate_template_previews.verify_dependencies')
    def test_main_success_flow(self, mock_verify, mock_generate, mock_convert, 
                              mock_copy, mock_cleanup):
        """Test successful main function execution."""
        # Setup mocks for success
        mock_verify.return_value = True
        mock_generate.return_value = True
        mock_convert.return_value = True
        mock_copy.return_value = True
        
        generate_template_previews.main()
        
        # Verify all functions were called
        mock_verify.assert_called_once()
        mock_generate.assert_called_once()
        mock_convert.assert_called_once()
        mock_copy.assert_called_once()
        mock_cleanup.assert_called_once()
    
    @patch('generate_template_previews.cleanup_temp_files')
    @patch('generate_template_previews.verify_dependencies')
    def test_main_dependency_failure(self, mock_verify, mock_cleanup):
        """Test main function with dependency verification failure."""
        mock_verify.return_value = False
        
        with pytest.raises(SystemExit) as exc_info:
            generate_template_previews.main()
        
        assert exc_info.value.code == 1
        mock_cleanup.assert_called_once()  # Should cleanup even on failure
    
    @patch('generate_template_previews.cleanup_temp_files')
    @patch('generate_template_previews.generate_template_samples')
    @patch('generate_template_previews.verify_dependencies')
    def test_main_generation_failure(self, mock_verify, mock_generate, mock_cleanup):
        """Test main function with generation failure."""
        mock_verify.return_value = True
        mock_generate.return_value = False
        
        with pytest.raises(SystemExit) as exc_info:
            generate_template_previews.main()
        
        assert exc_info.value.code == 1
        mock_cleanup.assert_called_once()
    
    @patch('generate_template_previews.cleanup_temp_files')
    @patch('generate_template_previews.verify_dependencies')
    def test_main_keyboard_interrupt(self, mock_verify, mock_cleanup):
        """Test main function with keyboard interrupt."""
        mock_verify.side_effect = KeyboardInterrupt()
        
        with pytest.raises(SystemExit) as exc_info:
            generate_template_previews.main()
        
        assert exc_info.value.code == 1
        mock_cleanup.assert_called_once()
    
    @patch('generate_template_previews.cleanup_temp_files')
    @patch('generate_template_previews.verify_dependencies')
    def test_main_unexpected_exception(self, mock_verify, mock_cleanup):
        """Test main function with unexpected exception."""
        mock_verify.side_effect = RuntimeError("Unexpected error")
        
        with pytest.raises(SystemExit) as exc_info:
            generate_template_previews.main()
        
        assert exc_info.value.code == 1
        mock_cleanup.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__])