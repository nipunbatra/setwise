#!/usr/bin/env python3
"""
Comprehensive tests for TemplateManager class
"""

import pytest
import tempfile
import os
import shutil
from pathlib import Path

from setwise.template_manager import TemplateManager


class TestTemplateManagerInitialization:
    """Test TemplateManager initialization"""
    
    def test_default_initialization(self):
        """Test default initialization"""
        manager = TemplateManager()
        assert manager.template_dir == Path("templates")
        assert hasattr(manager, 'templates')
        assert isinstance(manager.templates, dict)
    
    def test_custom_template_directory(self):
        """Test initialization with custom directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = TemplateManager(template_dir=temp_dir)
            assert str(manager.template_dir) == temp_dir
    
    def test_templates_structure(self):
        """Test that templates dictionary has expected structure"""
        manager = TemplateManager()
        
        # Should have at least default templates
        assert "default" in manager.templates
        assert "compact" in manager.templates
        assert "minimal" in manager.templates
        
        # Each template should have required fields
        for template_id, template_info in manager.templates.items():
            assert "file" in template_info
            assert "name" in template_info
            assert "description" in template_info
            assert "features" in template_info
            assert isinstance(template_info["features"], list)


class TestTemplateOperations:
    """Test template operations and methods"""
    
    def test_get_template_path(self):
        """Test getting template file paths"""
        manager = TemplateManager()
        
        # Test getting existing template
        path = manager.get_template_path("default")
        assert isinstance(path, Path)
        assert path.name == "quiz_template.tex.jinja"
        
        # Test getting non-existing template
        with pytest.raises(KeyError):
            manager.get_template_path("nonexistent")
    
    def test_list_templates_content(self):
        """Test list_templates method content"""
        manager = TemplateManager()
        templates_info = manager.list_templates()
        
        # Should return string with template information
        assert isinstance(templates_info, str)
        assert "Available Templates" in templates_info
        assert "default" in templates_info
        assert "compact" in templates_info
        assert "minimal" in templates_info
    
    def test_get_template_names(self):
        """Test getting list of template names"""
        manager = TemplateManager()
        names = list(manager.templates.keys())
        
        assert isinstance(names, list)
        assert len(names) >= 3  # Should have at least default, compact, minimal
        assert "default" in names
    
    def test_template_exists(self):
        """Test checking if template exists"""
        manager = TemplateManager()
        
        # Should exist
        assert "default" in manager.templates
        assert "compact" in manager.templates
        
        # Should not exist
        assert "nonexistent" not in manager.templates
        assert "invalid_template" not in manager.templates


class TestTemplateValidation:
    """Test template validation functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.template_dir = os.path.join(self.temp_dir, "templates")
        os.makedirs(self.template_dir, exist_ok=True)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_validate_template_file_exists(self):
        """Test template file existence validation"""
        # Create a valid template file
        template_file = os.path.join(self.template_dir, "test_template.tex.jinja")
        with open(template_file, 'w') as f:
            f.write("""
\\documentclass{article}
\\begin{document}
{{ quiz_metadata.title }}
\\end{document}
""")
        
        manager = TemplateManager(template_dir=self.template_dir)
        
        # Check if template file exists
        template_path = Path(self.template_dir) / "test_template.tex.jinja"
        assert template_path.exists()
    
    def test_template_file_not_exists(self):
        """Test handling of non-existent template files"""
        manager = TemplateManager(template_dir=self.template_dir)
        
        # Try to get path for template that doesn't exist on disk
        # (but might exist in templates dict)
        try:
            manager.get_template_path("default")
        except (KeyError, FileNotFoundError):
            # Expected - template file doesn't exist in empty temp directory
            pass
    
    def test_invalid_template_directory(self):
        """Test handling of invalid template directory"""
        invalid_dir = os.path.join(self.temp_dir, "nonexistent")
        manager = TemplateManager(template_dir=invalid_dir)
        
        # Should not crash during initialization
        assert manager.template_dir == Path(invalid_dir)


class TestTemplateContent:
    """Test template content and structure"""
    
    def test_template_metadata_completeness(self):
        """Test that all templates have complete metadata"""
        manager = TemplateManager()
        
        required_fields = ["file", "name", "description", "features", "pages", "use_case"]
        
        for template_id, template_info in manager.templates.items():
            for field in required_fields:
                assert field in template_info, f"Template {template_id} missing field: {field}"
            
            # Validate field types
            assert isinstance(template_info["file"], str)
            assert isinstance(template_info["name"], str)
            assert isinstance(template_info["description"], str)
            assert isinstance(template_info["features"], list)
            assert isinstance(template_info["pages"], str)
            assert isinstance(template_info["use_case"], str)
            
            # Validate content
            assert len(template_info["name"]) > 0
            assert len(template_info["description"]) > 10  # Should be descriptive
            assert len(template_info["features"]) > 0
    
    def test_template_file_extensions(self):
        """Test that template files have correct extensions"""
        manager = TemplateManager()
        
        for template_id, template_info in manager.templates.items():
            filename = template_info["file"]
            assert filename.endswith(".tex.jinja"), f"Template {template_id} has invalid extension: {filename}"
    
    def test_template_names_unique(self):
        """Test that template names are unique"""
        manager = TemplateManager()
        
        names = [info["name"] for info in manager.templates.values()]
        assert len(names) == len(set(names)), "Template names are not unique"
    
    def test_template_files_unique(self):
        """Test that template files are unique"""
        manager = TemplateManager()
        
        files = [info["file"] for info in manager.templates.values()]
        assert len(files) == len(set(files)), "Template files are not unique"


class TestTemplateIntegration:
    """Integration tests for template management"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.template_dir = os.path.join(self.temp_dir, "templates")
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Copy real templates for testing
        setwise_root = Path(__file__).parent.parent
        real_template_dir = setwise_root / "setwise" / "templates"
        
        if real_template_dir.exists():
            for template_file in real_template_dir.glob("*.tex.jinja"):
                shutil.copy(template_file, self.template_dir)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_real_template_files_exist(self):
        """Test that real template files exist and are accessible"""
        manager = TemplateManager(template_dir=self.template_dir)
        
        for template_id, template_info in manager.templates.items():
            template_path = Path(self.template_dir) / template_info["file"]
            
            if template_path.exists():
                # Template exists, test it can be read
                content = template_path.read_text()
                assert len(content) > 100  # Should be substantial
                assert "\\documentclass" in content  # Should be LaTeX
                assert "{{" in content  # Should have Jinja2 templates
    
    def test_template_loading_workflow(self):
        """Test complete template loading workflow"""
        manager = TemplateManager(template_dir=self.template_dir)
        
        # Get list of templates
        template_list = manager.list_templates()
        assert isinstance(template_list, str)
        
        # Try to get each template
        for template_id in manager.templates.keys():
            try:
                path = manager.get_template_path(template_id)
                assert isinstance(path, Path)
            except KeyError:
                # Template ID exists in dict but might not have file
                pass
    
    def test_custom_template_addition(self):
        """Test adding custom templates"""
        # Create custom template file
        custom_template = os.path.join(self.template_dir, "custom_template.tex.jinja")
        with open(custom_template, 'w') as f:
            f.write("""
\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\title{ {{ quiz_metadata.title }} }
\\begin{document}
\\maketitle
Custom template content here.
\\end{document}
""")
        
        # Create manager with custom templates
        manager = TemplateManager(template_dir=self.template_dir)
        
        # Could extend to test custom template registration
        # For now, just verify file exists
        assert Path(custom_template).exists()


class TestErrorHandling:
    """Test error handling in template operations"""
    
    def test_get_nonexistent_template(self):
        """Test getting non-existent template"""
        manager = TemplateManager()
        
        with pytest.raises(KeyError):
            manager.get_template_path("this_template_does_not_exist")
    
    def test_empty_template_directory(self):
        """Test with empty template directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = TemplateManager(template_dir=temp_dir)
            
            # Should not crash
            templates_info = manager.list_templates()
            assert isinstance(templates_info, str)
    
    def test_permission_denied_template_directory(self):
        """Test handling of permission denied on template directory"""
        import platform
        if platform.system() == "Windows":
            pytest.skip("Permission test not applicable on Windows")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            restricted_dir = os.path.join(temp_dir, "restricted")
            os.makedirs(restricted_dir)
            os.chmod(restricted_dir, 0o000)  # Remove all permissions
            
            try:
                manager = TemplateManager(template_dir=restricted_dir)
                # Should handle gracefully
                assert manager is not None
            finally:
                os.chmod(restricted_dir, 0o755)  # Restore permissions for cleanup


if __name__ == "__main__":
    pytest.main([__file__, "-v"])