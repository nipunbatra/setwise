#!/usr/bin/env python3
"""
Debug script to reproduce the webapp issue locally
"""

import tempfile
import os
from pathlib import Path
from setwise.quiz_generator import QuizGenerator

def test_webapp_scenario():
    """Test the exact scenario the webapp uses"""
    
    # Sample questions that webapp might use
    questions_text = """# ✨ Setwise v2.0 Demo - Tested and Working!
quiz_metadata = {
    "title": "Enhanced Setwise Demo Quiz",
    "subject": "Mathematics & Science",
    "duration": "45 minutes", 
    "total_marks": 20,
    "instructions": ["Show your work", "Use proper units"]
}

mcq = [
    {
        "question": r"What is $2 + 2$?",
        "options": [r"2", r"3", r"4", r"5"],
        "answer": r"4",
        "marks": 2
    },
    {
        "template": r"What is {{ a }} $\\times$ {{ b }}?",
        "options": [
            r"{{ a * b }}",
            r"{{ a + b }}", 
            r"{{ a - b }}",
            r"{{ a / b if b != 0 else 0 }}"
        ],
        "answer": r"{{ a * b }}",
        "variables": [
            {"a": 3, "b": 4},
            {"a": 5, "b": 6}
        ],
        "marks": 3
    }
]

subjective = [
    {
        "question": r"Explain why these operations give these results.",
        "answer": r"Addition combines quantities: 15 + 25 counts all units together. Division splits equally: 40 $\\div$ 8 means 40 split into 8 equal groups of 5.",
        "marks": 4
    }
]"""

    print("🧪 Testing webapp scenario...")
    
    # Create temporary questions file like webapp does
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(questions_text)
        questions_file = f.name
    
    print(f"✓ Questions file created: {questions_file}")
    
    # Create temporary output directory
    output_dir = tempfile.mkdtemp()
    print(f"✓ Output directory created: {output_dir}")
    
    try:
        # Find setwise templates like webapp does
        import setwise
        setwise_dir = Path(setwise.__file__).parent
        templates_dir = setwise_dir / 'templates'
        print(f"✓ Using templates from: {templates_dir}")
        
        # Change to setwise directory like webapp does
        original_cwd = os.getcwd()
        print(f"Changing directory from {original_cwd} to {setwise_dir}")
        os.chdir(str(setwise_dir))
        
        # Initialize QuizGenerator like webapp does
        print("Initializing QuizGenerator...")
        generator = QuizGenerator(
            questions_file=questions_file,
            output_dir=output_dir
        )
        print("✓ QuizGenerator initialized")
        
        # Test without PDF compilation first
        print("\n=== TEST 1: Without PDF compilation ===")
        success1 = generator.generate_quizzes(
            num_sets=2,
            template_name="default",
            compile_pdf=False  # No LaTeX required
        )
        print(f"Result without PDF: {success1}")
        
        # List what was created
        files = list(Path(output_dir).glob("*"))
        print(f"Files created: {len(files)}")
        for f in files:
            print(f"  - {f.name} ({f.stat().st_size} bytes)")
        
        # Test with PDF compilation (this might fail)
        print("\n=== TEST 2: With PDF compilation ===")
        # Clear output directory first
        for f in files:
            f.unlink()
            
        try:
            success2 = generator.generate_quizzes(
                num_sets=2,
                template_name="default", 
                compile_pdf=True  # Requires LaTeX
            )
            print(f"Result with PDF: {success2}")
            
            # List what was created
            files = list(Path(output_dir).glob("*"))
            print(f"Files created: {len(files)}")
            for f in files:
                print(f"  - {f.name} ({f.stat().st_size} bytes)")
                
        except Exception as e:
            print(f"❌ PDF compilation failed: {e}")
            print("This is likely the webapp issue - LaTeX not available or not configured")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        os.chdir(original_cwd)
        os.unlink(questions_file)
        
        # Cleanup output directory
        import shutil
        shutil.rmtree(output_dir, ignore_errors=True)

if __name__ == "__main__":
    test_webapp_scenario()