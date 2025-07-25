"""
Setwise: Professional LaTeX Quiz Generator

A professional Python-based quiz generation system that creates beautiful, 
randomized PDF quizzes with comprehensive machine learning content.
"""

__version__ = "1.0.0"
__author__ = "Nipun Batra"
__email__ = "nipunbatra0@gmail.com"
__description__ = "Professional LaTeX Quiz Generator for Machine Learning Content"

from .quiz_generator import QuizGenerator

# Import TemplateManager with fallback
try:
    from .template_manager import TemplateManager
except ImportError:
    from templates.template_config import TemplateManager

__all__ = ["QuizGenerator", "TemplateManager"]