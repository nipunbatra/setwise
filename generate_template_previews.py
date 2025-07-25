#!/usr/bin/env python3
"""
Generate template preview images for the Setwise website.

This script generates sample PDFs for all templates and converts them to PNG images
for display on the GitHub Pages website.
"""

import os
import sys
import subprocess
import shutil
import shlex
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"Running: {description}")
    try:
        # Use shlex.split for secure command parsing instead of shell=True
        cmd_args = shlex.split(cmd) if isinstance(cmd, str) else cmd
        result = subprocess.run(cmd_args, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error {description}: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def generate_template_samples():
    """Generate sample PDFs for all templates."""
    templates = ['default', 'compact', 'academic', 'minimal']
    temp_dir = Path('assets_temp')
    
    print("=== Generating Template Samples ===")
    
    for template in templates:
        template_dir = temp_dir / template
        template_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = f"python main.py --seed 42 --sets 1 --mcq 4 --subjective 2 --template {template} --output-dir {template_dir}"
        success = run_command(cmd, f"Generating {template} template sample")
        
        if not success:
            print(f"Failed to generate {template} template sample")
            return False
            
    return True

def convert_pdfs_to_images():
    """Convert PDFs to PNG images for website."""
    templates = ['compact', 'academic', 'minimal']  # default already exists
    temp_dir = Path('assets_temp')
    images_dir = Path('assets/images')
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== Converting PDFs to PNG Images ===")
    
    for template in templates:
        pdf_path = temp_dir / template / 'quiz_set_1.pdf'
        output_prefix = images_dir / f'{template}_preview'
        
        if not pdf_path.exists():
            print(f"Warning: PDF not found at {pdf_path}")
            continue
            
        cmd = f"pdftoppm -png -r 150 {pdf_path} {output_prefix}"
        success = run_command(cmd, f"Converting {template} PDF to PNG")
        
        if not success:
            print(f"Failed to convert {template} PDF to PNG")
            return False
            
    return True

def copy_sample_pdfs():
    """Copy sample PDFs to assets directory."""
    templates = ['compact', 'academic', 'minimal']
    temp_dir = Path('assets_temp')
    assets_dir = Path('assets')
    
    print("=== Copying Sample PDFs ===")
    
    for template in templates:
        src_pdf = temp_dir / template / 'quiz_set_1.pdf'
        dst_pdf = assets_dir / f'{template}_sample.pdf'
        
        if src_pdf.exists():
            shutil.copy2(src_pdf, dst_pdf)
            print(f"Copied {template} sample PDF to {dst_pdf}")
        else:
            print(f"Warning: Source PDF not found at {src_pdf}")
            
    return True

def cleanup_temp_files():
    """Clean up temporary files."""
    temp_dir = Path('assets_temp')
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        print("Cleaned up temporary files")

def verify_dependencies():
    """Verify required dependencies are available."""
    print("=== Verifying Dependencies ===")
    
    # Check for pdftoppm
    try:
        subprocess.run(['pdftoppm', '-h'], capture_output=True, check=True)
        print("✓ pdftoppm found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ pdftoppm not found. Install poppler-utils:")
        print("  macOS: brew install poppler")
        print("  Ubuntu: sudo apt-get install poppler-utils")
        return False
        
    # Check for pdflatex
    try:
        subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
        print("✓ pdflatex found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ pdflatex not found. Install LaTeX distribution.")
        return False
        
    return True

def main():
    """Main function to generate all template previews."""
    print("Setwise Template Preview Generator")
    print("=" * 40)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Verify dependencies
    if not verify_dependencies():
        sys.exit(1)
    
    try:
        # Generate template samples
        if not generate_template_samples():
            print("Failed to generate template samples")
            sys.exit(1)
            
        # Convert PDFs to images
        if not convert_pdfs_to_images():
            print("Failed to convert PDFs to images")
            sys.exit(1)
            
        # Copy sample PDFs
        if not copy_sample_pdfs():
            print("Failed to copy sample PDFs")
            sys.exit(1)
            
        print("\n=== Success! ===")
        print("Generated template previews:")
        
        # List generated files
        images_dir = Path('assets/images')
        for template in ['compact', 'academic', 'minimal']:
            preview_file = images_dir / f'{template}_preview-1.png'
            if preview_file.exists():
                print(f"✓ {preview_file}")
            else:
                print(f"✗ Missing: {preview_file}")
                
        assets_dir = Path('assets')
        for template in ['compact', 'academic', 'minimal']:
            sample_file = assets_dir / f'{template}_sample.pdf'
            if sample_file.exists():
                print(f"✓ {sample_file}")
            else:
                print(f"✗ Missing: {sample_file}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Always cleanup temp files
        cleanup_temp_files()

if __name__ == '__main__':
    main()