#!/usr/bin/env python3
"""
Quiz Generator Core Module

Contains the main QuizGenerator class and related functions for generating
randomized LaTeX quiz sets with answer keys.
"""

import random
import os
import sys
import subprocess
import argparse
import importlib.util
from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from .latex_validator import LaTeXValidator

# Import template manager
try:
    from .template_manager import TemplateManager
except ImportError:
    # Fallback for development/backward compatibility
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "templates"))
    from template_config import TemplateManager


class QuizGenerator:
    """Main class for generating randomized quiz sets."""
    
    def __init__(self, template_dir: str = "templates", output_dir: str = "output", 
                 questions_file: Optional[str] = None):
        """Initialize the quiz generator.
        
        Args:
            template_dir: Directory containing LaTeX templates
            output_dir: Directory for generated quiz files
            questions_file: Path to custom questions.py file (optional)
        """
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.template_manager = TemplateManager(template_dir)
        
        # Initialize quiz metadata (will be populated by _load_questions)
        self.quiz_metadata = {}
        
        # Load questions from custom file or default
        self.mcq, self.subjective = self._load_questions(questions_file)
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)
    
    def _load_questions(self, questions_file: Optional[str] = None) -> Tuple[List[Dict], List[Dict]]:
        """Load questions from Python file (.py only for simplicity).
        
        Args:
            questions_file: Path to Python questions file (.py)
            
        Returns:
            Tuple of (mcq_questions, subjective_questions)
        """
        if questions_file:
            # Load from custom Python file only
            questions_path = Path(questions_file)
            if not questions_path.exists():
                raise FileNotFoundError(f"Questions file not found: {questions_file}")
            
            # Ensure it's a Python file
            if questions_path.suffix.lower() != '.py':
                raise ValueError(f"Only Python files (.py) are supported. Got: {questions_path.suffix}")
            
            # Load Python module dynamically
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("questions", questions_path)
                if spec is None or spec.loader is None:
                    raise ImportError(f"Could not load module from {questions_path}")
                
                questions_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(questions_module)
                
                # Extract questions and metadata
                mcq = getattr(questions_module, 'mcq', [])
                subjective = getattr(questions_module, 'subjective', [])
                
                # Also extract quiz metadata if present
                if hasattr(questions_module, 'quiz_metadata'):
                    self.quiz_metadata = questions_module.quiz_metadata
                else:
                    self.quiz_metadata = {}
                
                return mcq, subjective
                
            except Exception as e:
                raise RuntimeError(f"Failed to load questions from {questions_file}: {e}")
        
        else:
            # Load from default location
            try:
                from .data.questions import mcq, subjective
                # Try to load default metadata too
                try:
                    from .data.questions import quiz_metadata
                    self.quiz_metadata = quiz_metadata
                except ImportError:
                    self.quiz_metadata = {}
                return mcq, subjective
            except ImportError:
                # Fallback for development/backward compatibility
                current_dir = Path(__file__).parent.parent
                sys.path.insert(0, str(current_dir / "data"))
                from questions import mcq, subjective
                return mcq, subjective
    
    def shuffle_mcq_options(self, question_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Shuffle MCQ options while tracking correct answers.
        Returns list of questions with shuffled options and updated answer tracking.
        """
        shuffled_questions = []
        
        for q in question_list:
            # Create a copy of the question
            shuffled_q = q.copy()
            
            # Create list of (option, is_correct) tuples
            options_with_correctness = []
            for opt in q["options"]:
                is_correct = (opt == q["answer"])
                options_with_correctness.append((opt, is_correct))
            
            # Shuffle the options
            random.shuffle(options_with_correctness)
            
            # Extract shuffled options and find new correct answer
            shuffled_q["options"] = [opt for opt, _ in options_with_correctness]
            
            # Find the new position of the correct answer
            for i, (opt, is_correct) in enumerate(options_with_correctness):
                if is_correct:
                    shuffled_q["correct_index"] = i
                    shuffled_q["correct_letter"] = chr(65 + i)  # A, B, C, D
                    break
            
            shuffled_questions.append(shuffled_q)
        
        return shuffled_questions

    def process_templated_questions(self, question_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process questions that have multiple variable templates.
        For templated questions, randomly select one variant.
        Now supports both MCQ and subjective templated questions.
        """
        processed_questions = []
        
        for q in question_list:
            if "variables" in q and "template" in q:
                # Templated question - randomly select one variant
                selected_vars = random.choice(q["variables"])
                
                # Create Jinja2 template and render the template field
                template = Template(q["template"])
                rendered_question = template.render(**selected_vars)
                
                # Update the question with rendered content
                processed_q = q.copy()
                processed_q["question"] = rendered_question  # Convert template to question
                
                # For MCQ questions, also render options and answer
                if "options" in q:
                    rendered_options = []
                    for option in q["options"]:
                        option_template = Template(option)
                        rendered_option = option_template.render(**selected_vars)
                        rendered_options.append(rendered_option)
                    processed_q["options"] = rendered_options
                    
                    # Render the answer
                    answer_template = Template(q["answer"])
                    rendered_answer = answer_template.render(**selected_vars)
                    processed_q["answer"] = rendered_answer
                
                # For subjective questions, render answer if it exists in selected_vars
                if "answer" in selected_vars:
                    processed_q["answer"] = selected_vars["answer"]
                
                processed_q["selected_variables"] = selected_vars
                
                # Remove the template field since we've converted it to question
                if "template" in processed_q:
                    del processed_q["template"]
                
                processed_questions.append(processed_q)
            else:
                # Non-templated question - use as-is
                processed_questions.append(q.copy())
        
        return processed_questions

    def generate_quiz_set(self, set_id: int, num_mcq: Optional[int] = None, 
                         num_subjective: Optional[int] = None, 
                         template_name: str = "default") -> Tuple[str, str]:
        """
        Generate a single quiz set with randomized questions and answer key.
        
        Args:
            set_id: Unique identifier for this quiz set
            num_mcq: Number of MCQ questions (None for all)
            num_subjective: Number of subjective questions (None for all)
            template_name: LaTeX template to use
            
        Returns:
            Tuple of (quiz_content, answer_key)
        """
        # Process templated subjective questions first
        processed_subjective = self.process_templated_questions(self.subjective)
        
        # Sample questions if limits specified
        if num_mcq is not None:
            sampled_mcq = random.sample(self.mcq, min(num_mcq, len(self.mcq)))
        else:
            sampled_mcq = self.mcq.copy()
            
        if num_subjective is not None:
            sampled_subjective = random.sample(processed_subjective, 
                                             min(num_subjective, len(processed_subjective)))
        else:
            sampled_subjective = processed_subjective
        
        # Shuffle MCQ options and track correct answers
        shuffled_mcq = self.shuffle_mcq_options(sampled_mcq)
        
        # Shuffle question order
        random.shuffle(shuffled_mcq)
        random.shuffle(sampled_subjective)
        
        # Calculate total marks
        mcq_marks = sum(q.get("marks", 0) for q in shuffled_mcq)
        subjective_marks = sum(q.get("marks", 0) for q in sampled_subjective)
        total_marks = mcq_marks + subjective_marks
        
        # Load and render the LaTeX template
        env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=True  # Enable autoescape for security
        )
        template_file = self.template_manager.get_template_file(template_name)
        template = env.get_template(template_file)
        
        quiz_content = template.render(
            set_id=set_id,
            mcq_questions=shuffled_mcq,
            subjective_questions=sampled_subjective,
            total_marks=total_marks,
            mcq_marks=mcq_marks,
            subjective_marks=subjective_marks
        )
        
        # Generate answer key
        answer_key = self._generate_answer_key(set_id, shuffled_mcq, sampled_subjective)
        
        return quiz_content, answer_key

    def _generate_answer_key(self, set_id: int, mcq_questions: List[Dict[str, Any]], 
                           subjective_questions: List[Dict[str, Any]]) -> str:
        """Generate answer key for a quiz set."""
        answer_lines = [f"ANSWER KEY - Quiz Set {set_id}", "=" * 40, ""]
        
        if mcq_questions:
            answer_lines.append("MULTIPLE CHOICE QUESTIONS:")
            answer_lines.append("-" * 30)
            for i, q in enumerate(mcq_questions, 1):
                correct_letter = q.get("correct_letter", "?")
                marks = q.get("marks", 1)
                answer_lines.append(f"Q{i}: {correct_letter} ({marks} marks)")
            answer_lines.append("")
        
        if subjective_questions:
            answer_lines.append("SUBJECTIVE QUESTIONS:")
            answer_lines.append("-" * 25)
            for i, q in enumerate(subjective_questions, 1):
                marks = q.get("marks", 5)
                solution = q.get("solution", "Solution not provided")
                answer_lines.append(f"Q{len(mcq_questions) + i}: ({marks} marks)")
                answer_lines.append(f"Answer: {solution}")
                answer_lines.append("")
        
        return "\n".join(answer_lines)

    def compile_latex(self, tex_file_path: Path, output_dir: Path) -> bool:
        """Compile LaTeX file to PDF with enhanced error handling."""
        try:
            # Run pdflatex twice for proper cross-references
            for run_num in range(2):
                result = subprocess.run(
                    ['pdflatex', f'-output-directory={output_dir}', tex_file_path],
                    capture_output=True,
                    text=True,
                    check=False  # Don't raise exception immediately
                )
                
                # Check for errors in the output
                if result.returncode != 0:
                    print(f"LaTeX compilation failed on run {run_num + 1}")
                    
                    # Parse LaTeX log for user-friendly errors
                    log_file = output_dir / f"{tex_file_path.stem}.log"
                    if log_file.exists():
                        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            log_content = f.read()
                        
                        latex_errors = LaTeXValidator.check_compilation_errors(log_content)
                        if latex_errors:
                            print("LaTeX Error Help:")
                            for error in latex_errors:
                                print(f"  - {error}")
                        
                        # Show raw error if no specific help available
                        if not latex_errors and result.stderr:
                            print(f"Raw LaTeX error: {result.stderr}")
                    
                    return False
            
            return True
            
        except FileNotFoundError:
            print("Error: pdflatex not found.")
            print("Please install LaTeX:")
            print("  - On Ubuntu/Debian: sudo apt-get install texlive-full")
            print("  - On macOS: brew install --cask mactex")
            print("  - On Windows: Download from https://miktex.org/")
            return False
        except Exception as e:
            print(f"Unexpected error during LaTeX compilation: {e}")
            return False

    def generate_quizzes(self, num_sets: int = 3, num_mcq: Optional[int] = None,
                        num_subjective: Optional[int] = None, 
                        template_name: str = "default",
                        compile_pdf: bool = True, seed: Optional[int] = None) -> bool:
        """
        Generate multiple quiz sets with answer keys.
        
        Args:
            num_sets: Number of quiz sets to generate
            num_mcq: Number of MCQ questions per set
            num_subjective: Number of subjective questions per set
            template_name: LaTeX template to use
            compile_pdf: Whether to compile LaTeX to PDF
            seed: Random seed for reproducibility
            
        Returns:
            True if successful, False otherwise
        """
        if seed is not None:
            random.seed(seed)
            print(f"Using random seed: {seed}")
        
        print(f"Generating {num_sets} quiz sets...")
        
        success = True
        for set_id in range(1, num_sets + 1):
            try:
                # Generate quiz content and answer key
                quiz_content, answer_key = self.generate_quiz_set(
                    set_id, num_mcq, num_subjective, template_name
                )
                
                # Write LaTeX file
                tex_filename = f"quiz_set_{set_id}.tex"
                tex_file_path = self.output_dir / tex_filename
                with open(tex_file_path, 'w', encoding='utf-8') as f:
                    f.write(quiz_content)
                
                # Write answer key
                answer_filename = f"answer_key_{set_id}.txt"
                answer_file_path = self.output_dir / answer_filename
                with open(answer_file_path, 'w', encoding='utf-8') as f:
                    f.write(answer_key)
                
                print(f"✓ Generated Quiz Set {set_id}")
                
                # Compile to PDF if requested
                if compile_pdf:
                    if self.compile_latex(tex_file_path, self.output_dir):
                        print(f"✓ Compiled Quiz Set {set_id} to PDF")
                    else:
                        print(f"✗ Failed to compile Quiz Set {set_id}")
                        success = False
                        
            except Exception as e:
                print(f"✗ Error generating Quiz Set {set_id}: {e}")
                success = False
        
        return success


def main():
    """Command-line interface for the quiz generator."""
    parser = argparse.ArgumentParser(description="Generate randomized LaTeX quiz sets")
    
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--sets", type=int, default=3, help="Number of quiz sets to generate")
    parser.add_argument("--mcq", type=int, help="Number of MCQ questions per set")
    parser.add_argument("--subjective", type=int, help="Number of subjective questions per set")
    parser.add_argument("--template", default="default", help="Template to use")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF compilation")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")
    
    args = parser.parse_args()
    
    # Handle template listing
    if args.list_templates:
        tm = TemplateManager()
        print(tm.list_templates())
        return
    
    # Create quiz generator
    generator = QuizGenerator(output_dir=args.output_dir)
    
    # Validate template
    is_valid, message = generator.template_manager.validate_template(args.template)
    if not is_valid:
        print(f"Error: {message}")
        sys.exit(1)
    
    # Generate quizzes
    success = generator.generate_quizzes(
        num_sets=args.sets,
        num_mcq=args.mcq,
        num_subjective=args.subjective,
        template_name=args.template,
        compile_pdf=not args.no_pdf,
        seed=args.seed
    )
    
    if success:
        print(f"\n✅ Successfully generated {args.sets} quiz sets in '{args.output_dir}/'")
    else:
        print("\n❌ Some errors occurred during generation")
        sys.exit(1)


if __name__ == "__main__":
    main()