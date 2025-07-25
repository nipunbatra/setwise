#!/usr/bin/env python3
"""
Test suite for templates/template_config.py module.
Tests template configuration management functionality.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

import sys
import os
sys.path.append('templates')
from template_config import TemplateManager, template_manager


class TestTemplateManager:
    """Test TemplateManager class functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.template_dir = Path(self.test_dir) / "templates"
        self.template_dir.mkdir()
        
        # Create test template files
        test_templates = [
            "quiz_template.tex.jinja",
            "quiz_template_compact.tex.jinja", 
            "quiz_template_academic.tex.jinja",
            "quiz_template_minimal.tex.jinja"
        ]
        
        for template in test_templates:
            (self.template_dir / template).write_text("\\documentclass{article}")
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_template_manager_initialization(self):
        """Test TemplateManager initialization."""
        tm = TemplateManager(str(self.template_dir))
        
        assert tm.template_dir == self.template_dir
        assert len(tm.templates) == 4
        assert "default" in tm.templates
        assert "compact" in tm.templates
        assert "academic" in tm.templates
        assert "minimal" in tm.templates
    
    def test_template_manager_default_directory(self):
        """Test TemplateManager with default directory."""
        tm = TemplateManager()
        
        assert tm.template_dir == Path("templates")
    
    def test_get_template_list(self):
        """Test getting list of available templates."""
        tm = TemplateManager(str(self.template_dir))
        
        template_list = tm.get_template_list()
        
        assert isinstance(template_list, list)
        assert len(template_list) == 4
        assert "default" in template_list
        assert "compact" in template_list
        assert "academic" in template_list
        assert "minimal" in template_list
    
    def test_get_template_info_valid(self):
        """Test getting template info for valid template."""
        tm = TemplateManager(str(self.template_dir))
        
        info = tm.get_template_info("default")
        
        assert info is not None
        assert "file" in info
        assert "name" in info
        assert "description" in info
        assert "features" in info
        assert "pages" in info
        assert "use_case" in info
        
        assert info["file"] == "quiz_template.tex.jinja"
        assert info["name"] == "Professional Default"
        assert isinstance(info["features"], list)
    
    def test_get_template_info_invalid(self):
        """Test getting template info for invalid template."""
        tm = TemplateManager(str(self.template_dir))
        
        info = tm.get_template_info("nonexistent")
        
        assert info is None
    
    def test_get_template_file_valid(self):
        """Test getting template file for valid template."""
        tm = TemplateManager(str(self.template_dir))
        
        file_path = tm.get_template_file("compact")
        
        assert file_path == "quiz_template_compact.tex.jinja"
    
    def test_get_template_file_invalid(self):
        """Test getting template file for invalid template."""
        tm = TemplateManager(str(self.template_dir))
        
        file_path = tm.get_template_file("nonexistent")
        
        assert file_path is None
    
    def test_validate_template_valid(self):
        """Test validating existing template."""
        tm = TemplateManager(str(self.template_dir))
        
        is_valid, message = tm.validate_template("academic")
        
        assert is_valid is True
        assert "valid" in message.lower()
    
    def test_validate_template_unknown(self):
        """Test validating unknown template."""
        tm = TemplateManager(str(self.template_dir))
        
        is_valid, message = tm.validate_template("unknown")
        
        assert is_valid is False
        assert "Unknown template" in message
        assert "Available:" in message
    
    def test_validate_template_missing_file(self):
        """Test validating template with missing file."""
        tm = TemplateManager(str(self.template_dir))
        
        # Remove the template file
        (self.template_dir / "quiz_template_minimal.tex.jinja").unlink()
        
        is_valid, message = tm.validate_template("minimal")
        
        assert is_valid is False
        assert "not found" in message
    
    def test_list_templates_format(self):
        """Test template listing format."""
        tm = TemplateManager(str(self.template_dir))
        
        listing = tm.list_templates()
        
        assert isinstance(listing, str)
        assert "Available Templates:" in listing
        assert "default: Professional Default" in listing
        assert "compact: Space-Efficient Compact" in listing
        assert "Description:" in listing
        assert "Features:" in listing
        assert "Best for:" in listing
    
    def test_template_metadata_completeness(self):
        """Test that all templates have complete metadata."""
        tm = TemplateManager(str(self.template_dir))
        
        required_fields = ["file", "name", "description", "features", "pages", "use_case"]
        
        for template_name in tm.get_template_list():
            info = tm.get_template_info(template_name)
            
            for field in required_fields:
                assert field in info, f"Missing field '{field}' in template '{template_name}'"
                assert info[field], f"Empty field '{field}' in template '{template_name}'"
            
            # Check specific field types
            assert isinstance(info["features"], list)
            assert len(info["features"]) > 0
    
    def test_template_file_extensions(self):
        """Test that all template files have correct extensions."""
        tm = TemplateManager(str(self.template_dir))
        
        for template_name in tm.get_template_list():
            file_path = tm.get_template_file(template_name)
            assert file_path.endswith(".tex.jinja"), f"Invalid extension for {template_name}: {file_path}"
    
    def test_template_names_uniqueness(self):
        """Test that template names are unique."""
        tm = TemplateManager(str(self.template_dir))
        
        template_names = []
        for template_name in tm.get_template_list():
            info = tm.get_template_info(template_name)
            template_names.append(info["name"])
        
        assert len(template_names) == len(set(template_names)), "Template names are not unique"


class TestGlobalTemplateManager:
    """Test global template manager instance."""
    
    def test_global_instance_exists(self):
        """Test that global template manager instance exists."""
        assert template_manager is not None
        assert isinstance(template_manager, TemplateManager)
    
    def test_global_instance_functionality(self):
        """Test global template manager functionality."""
        templates = template_manager.get_template_list()
        
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert "default" in templates
    
    def test_global_instance_template_info(self):
        """Test global template manager template info."""
        info = template_manager.get_template_info("default")
        
        assert info is not None
        assert "Professional Default" in info["name"]


class TestTemplateConfiguration:
    """Test template configuration details."""
    
    def test_default_template_config(self):
        """Test default template configuration."""
        tm = TemplateManager()
        info = tm.get_template_info("default")
        
        assert info["file"] == "quiz_template.tex.jinja"
        assert "Professional" in info["name"]
        assert "Single column" in info["features"]
        assert "color-coded" in info["description"].lower()
    
    def test_compact_template_config(self):
        """Test compact template configuration."""
        tm = TemplateManager()
        info = tm.get_template_info("compact")
        
        assert info["file"] == "quiz_template_compact.tex.jinja"
        assert "Compact" in info["name"]
        assert "Two columns" in info["features"]
        assert "2-3 pages" in info["pages"]
    
    def test_academic_template_config(self):
        """Test academic template configuration."""
        tm = TemplateManager()
        info = tm.get_template_info("academic")
        
        assert info["file"] == "quiz_template_academic.tex.jinja"
        assert "Academic" in info["name"]
        assert "Minimal colors" in info["features"]
        assert "University" in info["use_case"]
    
    def test_minimal_template_config(self):
        """Test minimal template configuration."""
        tm = TemplateManager()
        info = tm.get_template_info("minimal")
        
        assert info["file"] == "quiz_template_minimal.tex.jinja"
        assert "Minimal" in info["name"]
        assert "No colors" in info["features"]
        assert "black & white" in info["use_case"].lower()
    
    def test_template_page_estimates(self):
        """Test template page estimates are reasonable."""
        tm = TemplateManager()
        
        for template_name in tm.get_template_list():
            info = tm.get_template_info(template_name)
            pages = info["pages"]
            
            assert "pages" in pages.lower()
            # Should contain numbers
            assert any(char.isdigit() for char in pages)
    
    def test_template_features_consistency(self):
        """Test template features are consistent."""
        tm = TemplateManager()
        
        # Compact should have space-saving features
        compact_info = tm.get_template_info("compact")
        compact_features = " ".join(compact_info["features"]).lower()
        assert "compact" in compact_features or "column" in compact_features
        
        # Minimal should emphasize simplicity
        minimal_info = tm.get_template_info("minimal")
        minimal_features = " ".join(minimal_info["features"]).lower()
        assert "minimal" in minimal_features or "clean" in minimal_features or "no colors" in minimal_features


class TestErrorHandling:
    """Test error handling in template management."""
    
    def test_invalid_template_directory(self):
        """Test handling of invalid template directory."""
        # This should not raise an error during initialization
        tm = TemplateManager("/nonexistent/directory")
        
        # But validation should fail
        is_valid, message = tm.validate_template("default")
        assert is_valid is False
        assert "not found" in message
    
    def test_template_validation_edge_cases(self):
        """Test template validation edge cases."""
        tm = TemplateManager()
        
        # Empty string
        is_valid, message = tm.validate_template("")
        assert is_valid is False
        
        # None
        is_valid, message = tm.validate_template(None)
        assert is_valid is False
        
        # Whitespace
        is_valid, message = tm.validate_template("   ")
        assert is_valid is False
    
    def test_get_template_info_edge_cases(self):
        """Test get_template_info edge cases."""
        tm = TemplateManager()
        
        # Empty string
        assert tm.get_template_info("") is None
        
        # None
        assert tm.get_template_info(None) is None
        
        # Case sensitivity
        assert tm.get_template_info("DEFAULT") is None
        assert tm.get_template_info("Default") is None
    
    def test_get_template_file_edge_cases(self):
        """Test get_template_file edge cases."""
        tm = TemplateManager()
        
        # Empty string
        assert tm.get_template_file("") is None
        
        # None  
        assert tm.get_template_file(None) is None
        
        # Case sensitivity
        assert tm.get_template_file("COMPACT") is None


class TestTemplateManagerIntegration:
    """Integration tests for TemplateManager."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.template_dir = Path(self.test_dir) / "templates"
        self.template_dir.mkdir()
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_full_workflow(self):
        """Test complete template manager workflow."""
        # Create template files
        (self.template_dir / "quiz_template.tex.jinja").write_text("\\documentclass{article}")
        (self.template_dir / "quiz_template_compact.tex.jinja").write_text("\\documentclass{article}")
        
        tm = TemplateManager(str(self.template_dir))
        
        # Get template list
        templates = tm.get_template_list()
        assert len(templates) >= 2
        
        # Validate each template
        for template_name in templates:
            if template_name in ["default", "compact"]:  # Only test ones we created
                is_valid, message = tm.validate_template(template_name)
                assert is_valid, f"Template {template_name} should be valid: {message}"
        
        # Get template info
        for template_name in ["default", "compact"]:
            info = tm.get_template_info(template_name)
            assert info is not None
            assert "file" in info
        
        # List templates
        listing = tm.list_templates()
        assert isinstance(listing, str)
        assert len(listing) > 100  # Should be substantial content


if __name__ == '__main__':
    pytest.main([__file__])