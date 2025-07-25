#!/usr/bin/env python3
"""
Command-line interface for Setwise Quiz Generator
"""

import argparse
import sys
from pathlib import Path

from .quiz_generator import QuizGenerator

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
    
    # List templates command
    subparsers.add_parser('list-templates', help='List available templates')
    
    # Generate figures command
    subparsers.add_parser('generate-figures', help='Generate TikZ and matplotlib figures')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'generate':
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
    
    elif args.command == 'list-templates':
        tm = TemplateManager()
        print(tm.list_templates())
    
    elif args.command == 'generate-figures':
        print("Generating figures for ML quiz...")
        generate_figures()
        print("✅ Figures generated successfully!")


if __name__ == "__main__":
    main()