#!/usr/bin/env python3
"""
Setwise: Randomized LaTeX Quiz Generator
Main script to generate randomized quiz sets with answer keys.
"""

import random
import os
import sys
import subprocess
import argparse
from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path

# Import question data and template manager
sys.path.append('data')
sys.path.append('templates')
from questions import mcq, subjective
from template_config import template_manager


def shuffle_mcq_options(question_list):
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


def process_subjective_questions(subjective_list):
    """
    Process subjective questions, handling both templated and non-templated variants.
    Returns list of processed questions with answers for the answer key.
    """
    processed_questions = []
    
    for q in subjective_list:
        if "template" in q and "variables" in q:
            # Templated question - randomly select one variant
            selected_vars = random.choice(q["variables"])
            
            # Render the template with selected variables
            template = Template(q["template"])
            rendered_question = template.render(**{k: v for k, v in selected_vars.items() if k != "answer"})
            
            processed_questions.append({
                "question": rendered_question,
                "answer": selected_vars.get("answer", "Answer not provided"),
                "marks": q.get("marks", 0)
            })
        
        elif "question" in q:
            # Non-templated question
            processed_questions.append({
                "question": q["question"],
                "answer": q.get("answer", "Answer not provided"),
                "marks": q.get("marks", 0)
            })
        
        else:
            print(f"Warning: Invalid subjective question format: {q}")
    
    return processed_questions


def generate_quiz_set(set_id, num_mcq=None, num_subjective=None, template_name="default"):
    """
    Generate a single quiz set with randomized questions.
    
    Args:
        set_id: Identifier for the quiz set
        num_mcq: Number of MCQ questions to include (None = all)
        num_subjective: Number of subjective questions to include (None = all)
    
    Returns:
        tuple: (quiz_content, answer_key_content)
    """
    
    # Use all MCQ questions consistently, shuffle question order and options
    selected_mcq = mcq[:num_mcq] if num_mcq else mcq
    # Shuffle question order within MCQ section
    mcq_copy = selected_mcq.copy()
    random.shuffle(mcq_copy)
    shuffled_mcq = shuffle_mcq_options(mcq_copy)
    
    # Use all subjective questions consistently, shuffle question order and randomize template variables
    selected_subjective = subjective[:num_subjective] if num_subjective else subjective
    # Shuffle question order within subjective section
    subjective_copy = selected_subjective.copy()
    random.shuffle(subjective_copy)
    processed_subjective = process_subjective_questions(subjective_copy)
    
    # Calculate total marks
    mcq_marks = sum(q.get("marks", 0) for q in shuffled_mcq)
    subjective_marks = sum(q.get("marks", 0) for q in processed_subjective)
    total_marks = mcq_marks + subjective_marks
    
    # Load and render the LaTeX template
    env = Environment(loader=FileSystemLoader('templates'))
    template_file = template_manager.get_template_file(template_name)
    template = env.get_template(template_file)
    
    quiz_content = template.render(
        set_number=set_id,
        mcq_questions=shuffled_mcq,
        subjective_questions=processed_subjective,
        total_marks=total_marks,
        mcq_marks=mcq_marks,
        subjective_marks=subjective_marks
    )
    
    # Generate answer key
    answer_key_lines = []
    
    # MCQ answers with original question identification
    for i, q in enumerate(shuffled_mcq, 1):
        # Find original question index for reference
        original_idx = next((idx for idx, orig_q in enumerate(mcq, 1) if orig_q['question'] == q['question']), i)
        answer_key_lines.append(f"MCQ {i} (Original Q{original_idx}): Option {q['correct_letter']} - {q['answer']}")
    
    # Subjective answers with original question identification
    for i, q in enumerate(processed_subjective, 1):
        # Find original question index for reference
        original_idx = next((idx for idx, orig_q in enumerate(subjective, 1) 
                           if ('template' in orig_q and 'template' in q and orig_q.get('template', '') in q['question']) or
                              ('question' in orig_q and orig_q.get('question', '') == q['question'])), i)
        answer_key_lines.append(f"Subjective {i} (Original Q{original_idx}): {q['answer']}")
    
    answer_key_content = "\n".join(answer_key_lines)
    
    return quiz_content, answer_key_content


def compile_latex_to_pdf(tex_file_path, output_dir='output'):
    """
    Compile LaTeX file to PDF using pdflatex.
    
    Args:
        tex_file_path: Path to the .tex file
        output_dir: Directory to save output files
    
    Returns:
        bool: True if compilation successful, False otherwise
    """
    try:
        # Run pdflatex twice for proper cross-references
        for _ in range(2):
            result = subprocess.run(
                ['pdflatex', f'-output-directory={output_dir}', tex_file_path],
                capture_output=True,
                text=True,
                cwd='.',
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode != 0:
                print(f"LaTeX compilation error: {result.stderr}")
                return False
        
        # Clean up auxiliary files
        base_name = Path(tex_file_path).stem
        aux_extensions = ['.aux', '.log', '.out']
        
        for ext in aux_extensions:
            aux_file = Path(output_dir) / f"{base_name}{ext}"
            if aux_file.exists():
                aux_file.unlink()
        
        return True
        
    except FileNotFoundError:
        print("Error: pdflatex not found. Please install a LaTeX distribution.")
        return False
    except Exception as e:
        print(f"Error compiling LaTeX: {e}")
        return False


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Setwise: Randomized LaTeX Quiz Generator')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    parser.add_argument('--sets', type=int, default=3, help='Number of quiz sets to generate (default: 3)')
    parser.add_argument('--mcq', type=int, help='Number of MCQ questions per set (default: all)')
    parser.add_argument('--subjective', type=int, help='Number of subjective questions per set (default: all)')
    parser.add_argument('--no-pdf', action='store_true', help='Skip PDF compilation')
    parser.add_argument('--output-dir', type=str, default='output', help='Output directory (default: output)')
    parser.add_argument('--template', type=str, default='default', 
                        help='Template style to use (default: default). Use --list-templates to see options')
    parser.add_argument('--list-templates', action='store_true', 
                        help='List all available templates and exit')
    
    return parser.parse_args()

def validate_inputs(args):
    """Validate command line arguments and system requirements."""
    # Validate question counts
    if args.mcq and args.mcq > len(mcq):
        print(f"Warning: Requested {args.mcq} MCQ questions, but only {len(mcq)} available. Using all available.")
        args.mcq = len(mcq)
    
    if args.subjective and args.subjective > len(subjective):
        print(f"Warning: Requested {args.subjective} subjective questions, but only {len(subjective)} available. Using all available.")
        args.subjective = len(subjective)
    
    # Validate output directory
    if not os.path.exists(args.output_dir):
        try:
            os.makedirs(args.output_dir, exist_ok=True)
            print(f"Created output directory: {args.output_dir}")
        except OSError as e:
            print(f"Error: Cannot create output directory '{args.output_dir}': {e}")
            sys.exit(1)
    
    # Check for LaTeX if PDF compilation is enabled
    if not args.no_pdf:
        try:
            subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: pdflatex not found. PDF compilation will be skipped.")
            args.no_pdf = True
    
    # Validate template selection
    is_valid, message = template_manager.validate_template(args.template)
    if not is_valid:
        print(f"Error: {message}")
        sys.exit(1)
    
    return args

def main():
    """Main function to generate quiz sets."""
    
    try:
        # Parse command line arguments
        args = parse_args()
        
        # Handle template listing
        if args.list_templates:
            print(template_manager.list_templates())
            sys.exit(0)
        
        # Validate inputs
        args = validate_inputs(args)
        
        # Set random seed if provided
        if args.seed is not None:
            random.seed(args.seed)
            print(f"Using random seed: {args.seed}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during initialization: {e}")
        sys.exit(1)
    
    # Configuration from CLI arguments
    num_sets = args.sets
    num_mcq_per_set = args.mcq  # None for all if not specified
    num_subjective_per_set = args.subjective  # None for all if not specified
    compile_pdf = not args.no_pdf
    output_dir = args.output_dir
    
    print("Setwise Quiz Generator")
    print("=" * 40)
    print(f"Generating {num_sets} quiz sets")
    if args.seed is not None:
        print(f"Random seed: {args.seed}")
    print(f"MCQ questions per set: {num_mcq_per_set or 'all'}")
    print(f"Subjective questions per set: {num_subjective_per_set or 'all'}")
    print(f"PDF compilation: {'enabled' if compile_pdf else 'disabled'}")
    print(f"Output directory: {output_dir}")
    print("=" * 40)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    for set_num in range(1, num_sets + 1):
        print(f"Generating Quiz Set {set_num}...")
        
        # Generate quiz content
        quiz_content, answer_key_content = generate_quiz_set(
            set_id=set_num,
            num_mcq=num_mcq_per_set,
            num_subjective=num_subjective_per_set,
            template_name=args.template
        )
        
        # Save LaTeX file
        tex_filename = f"quiz_set_{set_num}.tex"
        tex_filepath = os.path.join(output_dir, tex_filename)
        
        with open(tex_filepath, 'w', encoding='utf-8') as f:
            f.write(quiz_content)
        
        print(f"  ✓ LaTeX file saved: {tex_filepath}")
        
        # Save answer key
        answer_key_filename = f"answer_key_{set_num}.txt"
        answer_key_filepath = os.path.join(output_dir, answer_key_filename)
        
        with open(answer_key_filepath, 'w', encoding='utf-8') as f:
            f.write(f"Answer Key for Quiz Set {set_num}\n")
            f.write("=" * 40 + "\n\n")
            f.write(answer_key_content)
        
        print(f"  ✓ Answer key saved: {answer_key_filepath}")
        
        # Compile to PDF if requested
        if compile_pdf:
            if compile_latex_to_pdf(tex_filepath, output_dir):
                pdf_filename = f"quiz_set_{set_num}.pdf"
                print(f"  ✓ PDF compiled: {output_dir}/{pdf_filename}")
            else:
                print(f"  ✗ PDF compilation failed for set {set_num}")
        
        print()
    
    print(f"Generated {num_sets} quiz sets successfully!")
    print(f"Files saved in: {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    main()