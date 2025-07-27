#!/usr/bin/env python3
"""
Command-line interface for Setwise Quiz Generator
"""

import argparse
import sys
from pathlib import Path

from .quiz_generator import QuizGenerator
from .question_manager import QuestionManager
from .latex_validator import LaTeXValidator, LaTeXErrorFixer
from .formats import QuestionFormatConverter
from .user_guidance import UserGuidance

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
  setwise generate --questions-file questions.yaml --template compact
  setwise questions convert questions.py questions.yaml
  setwise questions create-examples --output-dir examples
  setwise list-templates
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
    gen_parser.add_argument("--questions-file", help="Path to custom questions file (.py, .yaml, .json, .csv, .md)")
    
    # List templates command
    subparsers.add_parser('list-templates', help='List available templates')
    
    # Generate figures command
    subparsers.add_parser('generate-figures', help='Generate TikZ and matplotlib figures')
    
    # Welcome command for new users
    subparsers.add_parser('welcome', help='Welcome guide for new users')
    
    # Question management commands
    questions_parser = subparsers.add_parser('questions', help='Question library management')
    questions_subparsers = questions_parser.add_subparsers(dest='questions_command', help='Question commands')
    
    # List questions command
    list_q_parser = questions_subparsers.add_parser('list', help='List available question libraries')
    list_q_parser.add_argument('--search-dirs', nargs='+', help='Directories to search for question files')
    
    # Validate questions command
    validate_q_parser = questions_subparsers.add_parser('validate', help='Validate a questions file')
    validate_q_parser.add_argument('file', help='Path to questions.py file to validate')
    validate_q_parser.add_argument('--verbose', action='store_true', help='Show detailed suggestions and tips')
    validate_q_parser.add_argument('--auto-suggest', action='store_true', help='Provide automatic improvement suggestions')
    
    # Create sample command
    sample_q_parser = questions_subparsers.add_parser('create-sample', help='Create a sample questions.py file')
    sample_q_parser.add_argument('output', help='Output path for sample questions file')
    
    # Stats command
    stats_q_parser = questions_subparsers.add_parser('stats', help='Show statistics for a questions file')
    stats_q_parser.add_argument('file', help='Path to questions.py file')
    
    # Fix LaTeX command
    fix_q_parser = questions_subparsers.add_parser('fix-latex', help='Automatically fix common LaTeX errors in questions file')
    fix_q_parser.add_argument('file', help='Path to questions.py file to fix')
    fix_q_parser.add_argument('--output', help='Output file (default: overwrites input)')
    fix_q_parser.add_argument('--dry-run', action='store_true', help='Show fixes without applying them')
    
    # LaTeX help command
    questions_subparsers.add_parser('latex-help', help='Show LaTeX syntax help for writing questions')
    
    # Convert format command
    convert_q_parser = questions_subparsers.add_parser('convert', help='Convert questions between different formats')
    convert_q_parser.add_argument('input', help='Input questions file')
    convert_q_parser.add_argument('output', help='Output file with desired format extension (.py, .yaml, .json, .csv, .md)')
    convert_q_parser.add_argument('--format', choices=['python', 'yaml', 'json', 'csv', 'markdown'], 
                                 help='Override output format detection')
    
    # Create examples command
    examples_q_parser = questions_subparsers.add_parser('create-examples', help='Create example question files in all formats')
    examples_q_parser.add_argument('--output-dir', default='examples', help='Directory to create example files')
    
    # User guidance commands
    questions_subparsers.add_parser('recommend-format', help='Get personalized format recommendation')
    questions_subparsers.add_parser('format-comparison', help='Compare all available formats')
    
    workflow_q_parser = questions_subparsers.add_parser('workflow', help='Show workflow help for specific scenarios')
    workflow_q_parser.add_argument('type', choices=['first-time', 'collaboration', 'bulk-editing', 'latex-heavy'], 
                                   help='Type of workflow help')
    
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
    
    elif args.command == 'welcome':
        print("""
🎉 Welcome to Setwise - Professional LaTeX Quiz Generator!

🚀 Quick Start Guide:

1️⃣ Get Your First Quiz in 3 Steps:
   $ setwise questions create-examples --output-dir my_questions
   $ setwise questions validate my_questions/sample_questions.yaml --verbose
   $ setwise generate --questions-file my_questions/sample_questions.yaml

2️⃣ Choose Your Format:
   • 📚 Educator? Try YAML (human-readable)
   • 💻 Developer? Try JSON (web-friendly) 
   • 📊 Spreadsheet user? Try CSV (Excel-compatible)
   • 🐍 Programmer? Try Python (full power)
   
   Get personalized recommendation:
   $ setwise questions recommend-format

3️⃣ Need Help?
   • Format comparison: setwise questions format-comparison
   • LaTeX help: setwise questions latex-help  
   • Workflow guide: setwise questions workflow first-time
   • Validate files: setwise questions validate <file> --verbose

4️⃣ Pro Tips:
   ✨ Auto-fix LaTeX: setwise questions fix-latex <file>
   ✨ Convert formats: setwise questions convert input.yaml output.json
   ✨ Batch create: setwise questions create-examples --output-dir examples

🎯 Ready to create amazing quizzes? Start with step 1 above!

💡 Need detailed help? Run: setwise --help
        """)
    
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
                print(f"✅ Valid: {message}")
                
                # Show additional suggestions for valid files
                try:
                    suggestions = UserGuidance.detect_common_issues(args.file)
                    if suggestions:
                        print(f"\n💡 Suggestions for improvement ({len(suggestions)} found):")
                        for i, suggestion in enumerate(suggestions[:10]):  # Limit to 10 suggestions
                            print(f"   {i+1}. {suggestion}")
                        
                        if len(suggestions) > 10:
                            print(f"   ... and {len(suggestions) - 10} more suggestions")
                            
                        if args.auto_suggest:
                            print(f"\n🔧 To auto-fix common issues, run:")
                            print(f"   setwise questions fix-latex {args.file}")
                    else:
                        print("\n✨ No issues detected - your questions look great!")
                        
                    if args.verbose:
                        print(f"\n📊 Quick Stats:")
                        stats = QuestionManager.get_question_stats(args.file)
                        if 'error' not in stats:
                            print(f"   📝 Total questions: {stats['total_questions']}")
                            print(f"   🔢 MCQ: {stats['mcq_count']} ({stats['total_mcq_marks']} marks)")
                            print(f"   📖 Subjective: {stats['subjective_count']} ({stats['total_subjective_marks']} marks)")
                            print(f"   🏆 Total marks: {stats['total_marks']}")
                            
                except Exception as e:
                    if args.verbose:
                        print(f"\n⚠️ Could not generate suggestions: {e}")
            else:
                # Enhanced error message with guidance
                enhanced_message = UserGuidance.enhance_error_message(message)
                print(f"❌ Invalid: {enhanced_message}")
                
                if args.verbose:
                    print(f"\n🔍 Troubleshooting tips:")
                    print(f"   • Check file format and syntax")
                    print(f"   • Ensure all required fields are present")
                    print(f"   • Validate LaTeX expressions")
                    print(f"   • Run: setwise questions latex-help for LaTeX syntax help")
                
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
        
        elif args.questions_command == 'fix-latex':
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                fixed_content, fixes_applied = LaTeXErrorFixer.fix_common_errors(content)
                
                if args.dry_run:
                    print("LaTeX fixes that would be applied:")
                    if fixes_applied:
                        for fix in fixes_applied:
                            print(f"  - {fix}")
                    else:
                        print("  No automatic fixes needed")
                    
                    if fixed_content != content:
                        print("\nPreview of changes:")
                        print("-" * 40)
                        print(fixed_content[:500] + "..." if len(fixed_content) > 500 else fixed_content)
                else:
                    output_file = args.output or args.file
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    print(f"Fixed LaTeX errors in: {output_file}")
                    if fixes_applied:
                        print("Applied fixes:")
                        for fix in fixes_applied:
                            print(f"  - {fix}")
                    else:
                        print("No automatic fixes were needed")
                        
            except Exception as e:
                print(f"Error fixing LaTeX: {e}")
                sys.exit(1)
        
        elif args.questions_command == 'latex-help':
            print(LaTeXValidator.get_latex_help())
        
        elif args.questions_command == 'convert':
            # Convert between formats
            try:
                # Load questions from input format
                mcq, subjective = QuestionFormatConverter.load_questions(args.input)
                
                # Determine output format
                output_format = args.format
                if not output_format:
                    output_format = QuestionFormatConverter.detect_format(args.output)
                
                # Save in output format
                success = QuestionFormatConverter.save_questions(mcq, subjective, args.output, output_format)
                
                if success:
                    print(f"✅ Successfully converted {args.input} to {args.output} ({output_format} format)")
                    
                    # Show statistics
                    print(f"📊 Converted {len(mcq)} MCQ and {len(subjective)} subjective questions")
                else:
                    print(f"❌ Failed to convert {args.input} to {args.output}")
                    sys.exit(1)
                    
            except Exception as e:
                print(f"❌ Conversion failed: {e}")
                sys.exit(1)
        
        elif args.questions_command == 'create-examples':
            # Create example files in all formats
            try:
                output_dir = Path(args.output_dir)
                output_dir.mkdir(exist_ok=True)
                
                # Sample questions for examples
                mcq = [
                    {
                        "question": r"What is the capital of France?",
                        "options": [r"London", r"Berlin", r"Paris", r"Madrid"],
                        "answer": r"Paris",
                        "marks": 1
                    },
                    {
                        "question": r"Calculate: $2^3 + 5 \times 2$",
                        "options": [r"16", r"18", r"20", r"22"],
                        "answer": r"18",
                        "marks": 2
                    }
                ]
                
                subjective = [
                    {
                        "question": r"Explain Newton's first law of motion.",
                        "answer": r"An object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.",
                        "marks": 5
                    },
                    {
                        "question": r"Derive the quadratic formula from $ax^2 + bx + c = 0$.",
                        "answer": r"Starting with $ax^2 + bx + c = 0$, divide by $a$: $x^2 + \frac{b}{a}x + \frac{c}{a} = 0$. Complete the square to get $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$.",
                        "marks": 8
                    }
                ]
                
                # Create files in all formats
                formats = [
                    ('sample_questions.py', 'python'),
                    ('sample_questions.yaml', 'yaml'),
                    ('sample_questions.json', 'json'),
                    ('sample_questions.csv', 'csv'),
                    ('sample_questions.md', 'markdown')
                ]
                
                created_files = []
                for filename, format_type in formats:
                    file_path = output_dir / filename
                    success = QuestionFormatConverter.save_questions(mcq, subjective, str(file_path), format_type)
                    if success:
                        created_files.append(str(file_path))
                
                print(f"✅ Created {len(created_files)} example files in {output_dir}:")
                for file_path in created_files:
                    print(f"   📄 {file_path}")
                
                print(f"\n📚 Usage examples:")
                print(f"   setwise generate --questions-file {output_dir}/sample_questions.yaml")
                print(f"   setwise generate --questions-file {output_dir}/sample_questions.json")
                print(f"   setwise questions validate {output_dir}/sample_questions.csv")
                
            except Exception as e:
                print(f"❌ Failed to create examples: {e}")
                sys.exit(1)
        
        elif args.questions_command == 'recommend-format':
            # Get personalized format recommendation
            try:
                rec = UserGuidance.get_format_recommendation()
                print(f"\n🎯 Recommended format: {rec['primary'].upper()}")
                print(f"📝 Reason: {rec['reason']}")
                print(f"💡 Example use: {rec['example']}")
                
                # Show how to get started
                print(f"\n🚀 Get started:")
                print(f"   setwise questions create-examples --format {rec['primary']}")
                
            except Exception as e:
                print(f"❌ Error getting recommendation: {e}")
                sys.exit(1)
        
        elif args.questions_command == 'format-comparison':
            # Show format comparison table
            UserGuidance.show_format_comparison()
        
        elif args.questions_command == 'workflow':
            # Show workflow-specific help
            UserGuidance.show_workflow_help(args.type)


if __name__ == "__main__":
    main()