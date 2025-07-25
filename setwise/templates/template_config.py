"""
Template configuration system for Setwise quiz generator.
Manages different LaTeX template styles with metadata and validation.
"""

import os
from pathlib import Path

class TemplateManager:
    """Manages LaTeX templates with metadata and validation."""
    
    def __init__(self, template_dir="templates"):
        self.template_dir = Path(template_dir)
        self.templates = {
            "default": {
                "file": "quiz_template.tex.jinja",
                "name": "Professional Default",
                "description": "Professional single-column layout with color-coded sections and spacious design",
                "features": ["Single column", "Large fonts", "Color-coded boxes", "Professional styling"],
                "pages": "4-6 pages typical",
                "use_case": "Formal presentations, exams, professional documentation"
            },
            "compact": {
                "file": "quiz_template_compact.tex.jinja", 
                "name": "Space-Efficient Compact",
                "description": "Two-column layout with multi-column MCQ options for space efficiency",
                "features": ["Two columns", "Compact fonts", "Multi-column MCQs", "Reduced spacing"],
                "pages": "2-3 pages typical",
                "use_case": "Printing, quick distribution, saving paper"
            },
            "academic": {
                "file": "quiz_template_academic.tex.jinja",
                "name": "Academic Standard", 
                "description": "Traditional academic format with minimal colors and standard typography",
                "features": ["Single column", "Minimal colors", "Standard fonts", "Academic styling"],
                "pages": "3-5 pages typical",
                "use_case": "University exams, academic assessments, formal testing"
            },
            "minimal": {
                "file": "quiz_template_minimal.tex.jinja",
                "name": "Clean Minimal",
                "description": "Minimalist black and white design with clean typography",
                "features": ["No colors", "Clean lines", "Minimal decoration", "High contrast"],
                "pages": "3-4 pages typical", 
                "use_case": "Black & white printing, simple assessments, distraction-free"
            }
        }
    
    def get_template_list(self):
        """Return list of available template names."""
        return list(self.templates.keys())
    
    def get_template_info(self, template_name):
        """Get metadata for a specific template."""
        if template_name not in self.templates:
            return None
        return self.templates[template_name]
    
    def get_template_file(self, template_name):
        """Get the template file path for a given template name."""
        if template_name not in self.templates:
            return None
        return self.templates[template_name]["file"]
    
    def validate_template(self, template_name):
        """Check if template exists and file is available."""
        if template_name not in self.templates:
            return False, f"Unknown template '{template_name}'. Available: {', '.join(self.get_template_list())}"
        
        template_file = self.template_dir / self.templates[template_name]["file"]
        if not template_file.exists():
            return False, f"Template file '{template_file}' not found"
        
        return True, "Template is valid"
    
    def list_templates(self):
        """Return formatted string listing all available templates."""
        output = ["Available Templates:"]
        output.append("=" * 50)
        
        for key, info in self.templates.items():
            output.append(f"\n{key}: {info['name']}")
            output.append(f"  Description: {info['description']}")
            output.append(f"  Features: {', '.join(info['features'])}")
            output.append(f"  Typical size: {info['pages']}")
            output.append(f"  Best for: {info['use_case']}")
        
        return "\n".join(output)

# Global template manager instance
template_manager = TemplateManager()