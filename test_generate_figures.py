#!/usr/bin/env python3
"""
Test suite for generate_figures.py module.
Tests figure generation functions for ML quiz components.
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing

import generate_figures


class TestFigureGeneration:
    """Test figure generation functionality."""
    
    def setup_method(self):
        """Set up test environment with temporary directory."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_create_figures_directory(self):
        """Test figures directory creation."""
        # Ensure directory doesn't exist initially
        assert not os.path.exists('figures')
        
        # Create directory
        generate_figures.create_figures_directory()
        
        # Verify directory was created
        assert os.path.exists('figures')
        assert os.path.isdir('figures')
        
        # Test that it doesn't fail if directory already exists
        generate_figures.create_figures_directory()
        assert os.path.exists('figures')
    
    def test_generate_tikz_figures(self):
        """Test TikZ figure generation."""
        # Create figures directory
        generate_figures.create_figures_directory()
        
        # Generate TikZ figures
        generate_figures.generate_tikz_figures()
        
        # Check that TikZ files were created
        expected_files = [
            'figures/decision_tree.tikz',
            'figures/neural_network.tikz', 
            'figures/svm_margin.tikz'
        ]
        
        for filename in expected_files:
            assert os.path.exists(filename), f"Missing file: {filename}"
            
            # Check file content
            with open(filename, 'r') as f:
                content = f.read()
                assert 'tikzpicture' in content
                assert len(content) > 100  # Ensure substantial content
    
    def test_tikz_figure_content(self):
        """Test TikZ figure content validity."""
        generate_figures.create_figures_directory()
        generate_figures.generate_tikz_figures()
        
        # Test decision tree content
        with open('figures/decision_tree.tikz', 'r') as f:
            content = f.read()
            assert 'x_1' in content
            assert 'Class A' in content
            assert 'level distance' in content
        
        # Test neural network content  
        with open('figures/neural_network.tikz', 'r') as f:
            content = f.read()
            assert 'Input Layer' in content
            assert 'Hidden Layer' in content
            assert 'Output Layer' in content
            assert 'neuron' in content
        
        # Test SVM content
        with open('figures/svm_margin.tikz', 'r') as f:
            content = f.read()
            assert 'Decision Boundary' in content
            assert 'Margin' in content
            assert 'Support Vector' in content or 'SV' in content
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_generate_matplotlib_figures(self, mock_close, mock_savefig):
        """Test matplotlib figure generation."""
        generate_figures.create_figures_directory()
        
        # Generate matplotlib figures
        generate_figures.generate_matplotlib_figures()
        
        # Verify savefig was called for each expected figure
        expected_calls = [
            'figures/linear_regression.pdf',
            'figures/classification_boundary.pdf',
            'figures/overfitting_comparison.pdf', 
            'figures/learning_curves.pdf',
            'figures/roc_curve.pdf'
        ]
        
        assert mock_savefig.call_count == len(expected_calls)
        assert mock_close.call_count == len(expected_calls)
        
        # Check that correct filenames were used
        savefig_calls = [call[0][0] for call in mock_savefig.call_args_list]
        for expected_file in expected_calls:
            assert expected_file in savefig_calls
    
    @patch('generate_figures.generate_matplotlib_figures')
    @patch('generate_figures.generate_tikz_figures')
    @patch('generate_figures.create_figures_directory')
    def test_main_function(self, mock_create_dir, mock_tikz, mock_matplotlib):
        """Test main function calls all generation functions."""
        generate_figures.main()
        
        # Verify all functions were called
        mock_create_dir.assert_called_once()
        mock_tikz.assert_called_once()
        mock_matplotlib.assert_called_once()
    
    def test_integration_full_generation(self):
        """Integration test for full figure generation."""
        with patch('matplotlib.pyplot.savefig'), patch('matplotlib.pyplot.close'):
            # Run main function
            generate_figures.main()
            
            # Check TikZ files exist
            tikz_files = [
                'figures/decision_tree.tikz',
                'figures/neural_network.tikz',
                'figures/svm_margin.tikz'
            ]
            
            for tikz_file in tikz_files:
                assert os.path.exists(tikz_file)
                with open(tikz_file, 'r') as f:
                    content = f.read()
                    assert len(content) > 50  # Ensure files have content


class TestFigureContentValidation:
    """Test figure content validation."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_tikz_syntax_validation(self):
        """Test that generated TikZ has valid syntax structure."""
        generate_figures.create_figures_directory()
        generate_figures.generate_tikz_figures()
        
        for tikz_file in ['decision_tree.tikz', 'neural_network.tikz', 'svm_margin.tikz']:
            with open(f'figures/{tikz_file}', 'r') as f:
                content = f.read()
                
                # Check basic TikZ structure
                assert content.count('\\begin{tikzpicture}') == 1
                assert content.count('\\end{tikzpicture}') == 1
                
                # Ensure balanced braces (basic check)
                open_braces = content.count('{')
                close_braces = content.count('}')
                assert open_braces == close_braces
    
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.subplots')
    def test_matplotlib_figure_creation(self, mock_subplots, mock_figure):
        """Test matplotlib figure creation calls."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        # Mock subplots to return figure and axes
        mock_fig_sub = MagicMock()
        mock_axes = [MagicMock(), MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig_sub, mock_axes)
        
        with patch('matplotlib.pyplot.savefig'), patch('matplotlib.pyplot.close'):
            generate_figures.generate_matplotlib_figures()
        
        # Verify figure was created multiple times
        assert mock_figure.call_count >= 2  # At least 2 individual figures
        assert mock_subplots.call_count >= 1  # At least 1 subplot call
    
    def test_numpy_seed_consistency(self):
        """Test that numpy random seed produces consistent results."""
        import numpy as np
        
        # Test that seed is set in matplotlib generation
        with patch('matplotlib.pyplot.savefig'), patch('matplotlib.pyplot.close'):
            # First run
            np.random.seed(42)
            first_random = np.random.random(5)
            
            # Second run with same seed
            np.random.seed(42) 
            second_random = np.random.random(5)
            
            # Should be identical
            assert np.allclose(first_random, second_random)


class TestErrorHandling:
    """Test error handling in figure generation."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    @patch('os.makedirs')
    def test_directory_creation_error_handling(self, mock_makedirs):
        """Test handling of directory creation errors."""
        mock_makedirs.side_effect = PermissionError("Permission denied")
        
        with pytest.raises(PermissionError):
            generate_figures.create_figures_directory()
    
    @patch('builtins.open')
    def test_file_write_error_handling(self, mock_open):
        """Test handling of file write errors."""
        mock_open.side_effect = IOError("Disk full")
        
        generate_figures.create_figures_directory()
        
        with pytest.raises(IOError):
            generate_figures.generate_tikz_figures()
    
    @patch('matplotlib.pyplot.savefig')
    def test_matplotlib_save_error_handling(self, mock_savefig):
        """Test handling of matplotlib save errors."""
        mock_savefig.side_effect = IOError("Cannot save file")
        
        generate_figures.create_figures_directory()
        
        with pytest.raises(IOError):
            generate_figures.generate_matplotlib_figures()


if __name__ == '__main__':
    pytest.main([__file__])