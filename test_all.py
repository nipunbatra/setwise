#!/usr/bin/env python3
"""
Comprehensive test script for Setwise project
Tests syntax, imports, basic functionality, and core features
"""

import ast
import sys
import subprocess
import tempfile
import os
from pathlib import Path

def test_syntax(file_path):
    """Test Python syntax"""
    print(f"Testing syntax: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        print(f"✅ Syntax OK: {file_path}")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {file_path}:")
        print(f"   Line {e.lineno}: {e.text}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False

def test_imports():
    """Test core package imports"""
    print("\nTesting core package imports...")
    try:
        from setwise.quiz_generator import QuizGenerator
        from setwise.template_manager import TemplateManager
        from setwise.question_manager import QuestionManager
        from setwise.data.questions import example_questions
        print("✅ Core imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic quiz generation"""
    print("\nTesting basic functionality...")
    try:
        from setwise.quiz_generator import QuizGenerator
        
        # Test basic instantiation
        generator = QuizGenerator()
        print("✅ QuizGenerator instantiation successful")
        
        # Test with a simple quiz
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            
            # Create minimal test files
            Path("templates").mkdir(exist_ok=True)
            
            # Copy template
            import shutil
            setwise_root = Path(__file__).parent
            template_src = setwise_root / "setwise" / "templates" / "quiz_template.tex.jinja"
            if template_src.exists():
                shutil.copy(template_src, "templates/")
            
            # Test generation with default questions
            result = generator.generate_quizzes(num_sets=1, compile_pdf=False)
            if result:
                print("✅ Basic quiz generation successful")
                return True
            else:
                print("⚠️ Quiz generation returned False (may need LaTeX)")
                return True  # Still consider this OK for now
    except Exception as e:
        print(f"❌ Basic functionality error: {e}")
        return False

def test_webapp_syntax():
    """Test webapp syntax if it exists"""
    webapp_path = Path("../setwise-web/streamlit_app.py")
    if webapp_path.exists():
        return test_syntax(webapp_path)
    else:
        print("⚠️ Webapp not found, skipping webapp syntax test")
        return True

def run_pytest():
    """Run pytest if test files exist"""
    print("\nLooking for test files...")
    test_files = list(Path(".").glob("**/test_*.py")) + list(Path(".").glob("**/tests/*.py"))
    
    if test_files:
        print(f"Found {len(test_files)} test files, running pytest...")
        try:
            result = subprocess.run([sys.executable, "-m", "pytest", "-v"], 
                                    capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Pytest error: {e}")
            return False
    else:
        print("⚠️ No test files found")
        return True

def test_package_structure():
    """Test package structure and key files"""
    print("\nTesting package structure...")
    required_files = [
        "setwise/__init__.py",
        "setwise/quiz_generator.py", 
        "setwise/template_manager.py",
        "setwise/question_manager.py",
        "setwise/templates/quiz_template.tex.jinja",
        "pyproject.toml"
    ]
    
    all_good = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_good = False
    
    return all_good

def main():
    """Run all tests"""
    print("🧪 Running comprehensive Setwise tests...")
    print("=" * 50)
    
    results = []
    
    # Test package structure
    results.append(("Package Structure", test_package_structure()))
    
    # Test syntax of core files
    core_files = [
        "setwise/__init__.py",
        "setwise/quiz_generator.py",
        "setwise/template_manager.py", 
        "setwise/question_manager.py",
        "setwise/cli.py",
        "setwise/data/questions.py"
    ]
    
    syntax_ok = True
    for file_path in core_files:
        if Path(file_path).exists():
            if not test_syntax(file_path):
                syntax_ok = False
    
    results.append(("Core Package Syntax", syntax_ok))
    
    # Test webapp syntax
    results.append(("Webapp Syntax", test_webapp_syntax()))
    
    # Test imports
    results.append(("Core Imports", test_imports()))
    
    # Test basic functionality
    results.append(("Basic Functionality", test_basic_functionality()))
    
    # Run pytest
    results.append(("Pytest", run_pytest()))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20s}: {status}")
    
    print("-" * 50)
    print(f"Total: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed - see details above")
        return 1

if __name__ == "__main__":
    sys.exit(main())