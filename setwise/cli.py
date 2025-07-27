#!/usr/bin/env python3
"""
Command-line interface for Setwise Quiz Generator
"""

import argparse
import sys
from pathlib import Path

from .quiz_generator import QuizGenerator
from .question_manager import QuestionManager

# Import with fallbacks  
try:
    from .template_manager import TemplateManager
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "templates"))
    from template_config import TemplateManager

try:
    from .figure_generator import main as generate_figures
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from generate_figures import main as generate_figures


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Setwise: Professional LaTeX Quiz Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  setwise generate --seed 42 --sets 3 --mcq 5 --subjective 2
  setwise generate --template compact --output-dir my_quizzes
  setwise list-templates
  setwise generate-figures
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate quiz sets')
    gen_parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    gen_parser.add_argument("--sets", type=int, default=3, help="Number of quiz sets to generate")
    gen_parser.add_argument("--mcq", type=int, help="Number of MCQ questions per set")
    gen_parser.add_argument("--subjective", type=int, help="Number of subjective questions per set")
    gen_parser.add_argument("--template", default="default", help="Template to use")
    gen_parser.add_argument("--output-dir", default="output", help="Output directory")
    gen_parser.add_argument("--no-pdf", action="store_true", help="Skip PDF compilation")
    gen_parser.add_argument("--questions-file", help="Path to custom questions.py file")
    
    # List templates command
    subparsers.add_parser('list-templates', help='List available templates')
    
    # Generate figures command
    subparsers.add_parser('generate-figures', help='Generate TikZ and matplotlib figures')
    
    # Question management commands
    questions_parser = subparsers.add_parser('questions', help='Question library management')
    questions_subparsers = questions_parser.add_subparsers(dest='questions_command', help='Question commands')
    
    # List questions command
    list_q_parser = questions_subparsers.add_parser('list', help='List available question libraries')
    list_q_parser.add_argument('--search-dirs', nargs='+', help='Directories to search for question files')
    
    # Validate questions command
    validate_q_parser = questions_subparsers.add_parser('validate', help='Validate a questions file')
    validate_q_parser.add_argument('file', help='Path to questions.py file to validate')
    
    # Create sample command
    sample_q_parser = questions_subparsers.add_parser('create-sample', help='Create a sample questions.py file')
    sample_q_parser.add_argument('output', help='Output path for sample questions file')
    
    # Stats command
    stats_q_parser = questions_subparsers.add_parser('stats', help='Show statistics for a questions file')
    stats_q_parser.add_argument('file', help='Path to questions.py file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'generate':
        # Create quiz generator
        generator = QuizGenerator(
            output_dir=args.output_dir,
            questions_file=args.questions_file
        )
        
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
    
    elif args.command == 'list-templates':
        tm = TemplateManager()
        print(tm.list_templates())
    
    elif args.command == 'generate-figures':
        print("Generating figures for ML quiz...")
        generate_figures()
        print("Figures generated successfully!")
    
    elif args.command == 'questions':
        if not args.questions_command:
            questions_parser.print_help()
            return
        
        if args.questions_command == 'list':
            libraries = QuestionManager.list_question_libraries(args.search_dirs)
            if not libraries:
                print("No question libraries found.")
                return
            
            print(f"Found {len(libraries)} question libraries:")
            print("-" * 80)
            for lib in libraries:
                status = "Valid" if lib['valid'] else "Invalid"
                print(f"Name: {lib['name']}")
                print(f"Path: {lib['path']}")
                print(f"Status: {status}")
                print(f"Info: {lib['info']}")
                print(f"Size: {lib['size']} bytes")
                print("-" * 80)
        
        elif args.questions_command == 'validate':
            is_valid, message = QuestionManager.validate_questions_file(args.file)
            if is_valid:
                print(f"Valid: {message}")
            else:
                print(f"Invalid: {message}")
                sys.exit(1)
        
        elif args.questions_command == 'create-sample':
            if QuestionManager.create_sample_questions_file(args.output):
                print(f"Sample questions file created: {args.output}")
            else:
                print("Failed to create sample file")
                sys.exit(1)
        
        elif args.questions_command == 'stats':
            stats = QuestionManager.get_question_stats(args.file)
            if 'error' in stats:
                print(f"Error: {stats['error']}")
                sys.exit(1)
            
            print(f"Question Library Statistics: {args.file}")
            print("-" * 50)
            print(f"File size: {stats['file_size']} bytes")
            print(f"Total questions: {stats['total_questions']}")
            print(f"MCQ questions: {stats['mcq_count']} ({stats['total_mcq_marks']} marks)")
            print(f"Subjective questions: {stats['subjective_count']} ({stats['total_subjective_marks']} marks)")
            print(f"Templated subjective: {stats['templated_subjective']}")
            print(f"Total marks: {stats['total_marks']}")


if __name__ == "__main__":
    main()