#!/usr/bin/env python3
"""
Test header customization functionality
"""

import tempfile
import os
from pathlib import Path
from setwise.quiz_generator import QuizGenerator

def test_header_customization():
    """Test that header customization works"""
    
    # Questions with custom metadata
    questions_text = """quiz_metadata = {
    "title": "Custom Physics Quiz",
    "subject": "Advanced Physics",
    "duration": "90 minutes", 
    "total_marks": 50,
    "instructions": ["Use calculator when needed", "Show all working steps", "Round to 2 decimal places"]
}

mcq = [
    {
        "question": r"What is the speed of light?",
        "options": [r"3×10⁸ m/s", r"3×10⁹ m/s", r"3×10⁷ m/s", r"3×10¹⁰ m/s"],
        "answer": r"3×10⁸ m/s",
        "marks": 5
    }
]

subjective = [
    {
        "question": r"Derive the equation for kinetic energy.",
        "answer": r"KE = ½mv² derived from work-energy theorem",
        "marks": 15
    }
]"""

    print("🧪 Testing header customization...")
    
    # Create temporary questions file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(questions_text)
        questions_file = f.name
    
    # Create temporary output directory
    output_dir = tempfile.mkdtemp()
    
    try:
        # Change to setwise directory like webapp does
        import setwise
        setwise_dir = Path(setwise.__file__).parent
        original_cwd = os.getcwd()
        os.chdir(str(setwise_dir))
        
        # Initialize QuizGenerator
        generator = QuizGenerator(
            questions_file=questions_file,
            output_dir=output_dir
        )
        
        # Generate without PDF compilation to check TEX content
        success = generator.generate_quizzes(
            num_sets=1,
            template_name="default",
            compile_pdf=False
        )
        
        if success:
            # Read generated TEX file
            tex_file = Path(output_dir) / "quiz_set_1.tex"
            if tex_file.exists():
                content = tex_file.read_text()
                
                print("✅ Quiz generated successfully!")
                print("\n🔍 Checking for customization:")
                
                # Check for custom title
                if "Custom Physics Quiz" in content:
                    print("✅ Custom title found in TEX")
                else:
                    print("❌ Custom title NOT found in TEX")
                
                # Check for custom subject
                if "Advanced Physics" in content:
                    print("✅ Custom subject found in TEX")
                else:
                    print("❌ Custom subject NOT found in TEX")
                
                # Check for custom duration
                if "90 minutes" in content:
                    print("✅ Custom duration found in TEX")
                else:
                    print("❌ Custom duration NOT found in TEX")
                
                # Check for custom instructions
                if "Use calculator when needed" in content:
                    print("✅ Custom instructions found in TEX")
                else:
                    print("❌ Custom instructions NOT found in TEX")
                
                # Show excerpt
                print("\n📝 TEX file excerpt (first 50 lines):")
                lines = content.split('\n')
                for i, line in enumerate(lines[:50], 1):
                    if any(keyword in line for keyword in ["Custom Physics", "Advanced Physics", "90 minutes", "calculator"]):
                        print(f"  {i:2d}: {line} ← CUSTOMIZATION")
                    elif i <= 10 or "textbf" in line:
                        print(f"  {i:2d}: {line}")
                        
            else:
                print("❌ TEX file not created")
        else:
            print("❌ Quiz generation failed")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        os.chdir(original_cwd)  # Restore directory
        os.unlink(questions_file)
        import shutil
        shutil.rmtree(output_dir, ignore_errors=True)

if __name__ == "__main__":
    test_header_customization()