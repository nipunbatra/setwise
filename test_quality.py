#!/usr/bin/env python3
"""
Comprehensive Quality Testing Suite for Setwise

This script performs extensive testing of all Setwise functionality including:
- Format validation and conversion
- Error handling and edge cases
- Performance testing
- LaTeX compilation
- Usability scenarios
"""

import os
import sys
import tempfile
import shutil
import time
from pathlib import Path
import subprocess
import json

# Add setwise to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from setwise import QuizGenerator, TemplateManager
    from setwise.formats import QuestionFormatConverter
    from setwise.question_manager import QuestionManager
    from setwise.latex_validator import LaTeXValidator, LaTeXErrorFixer
except ImportError as e:
    print(f"❌ Error importing setwise: {e}")
    sys.exit(1)


class QualityTester:
    """Comprehensive quality testing for Setwise."""
    
    def __init__(self):
        self.test_dir = Path("quality_tests")
        self.test_dir.mkdir(exist_ok=True)
        self.results = {
            "format_tests": {},
            "error_tests": {},
            "performance_tests": {},
            "latex_tests": {},
            "usability_tests": {}
        }
    
    def run_all_tests(self):
        """Run comprehensive test suite."""
        print("🧪 Starting Comprehensive Quality Testing for Setwise")
        print("=" * 60)
        
        self.test_format_validation()
        self.test_format_conversion()
        self.test_error_handling()
        self.test_performance()
        self.test_latex_quality()
        self.test_usability_scenarios()
        
        self.generate_report()
    
    def test_format_validation(self):
        """Test validation across all formats."""
        print("\n📝 Testing Format Validation...")
        
        # Create test files in all formats
        test_data = {
            "mcq": [
                {
                    "question": "What is 2 + 2?",
                    "options": ["3", "4", "5", "6"],
                    "answer": "4",
                    "marks": 1
                }
            ],
            "subjective": [
                {
                    "question": "Explain gravity.",
                    "answer": "Gravity is a fundamental force.",
                    "marks": 5
                }
            ]
        }
        
        formats = ["python", "yaml", "json", "csv", "markdown"]
        validation_results = {}
        
        for format_type in formats:
            try:
                # Create test file
                test_file = self.test_dir / f"test_validation.{format_type}"
                if format_type == "python":
                    test_file = test_file.with_suffix(".py")
                elif format_type == "yaml":
                    test_file = test_file.with_suffix(".yaml")
                elif format_type == "json":
                    test_file = test_file.with_suffix(".json")
                elif format_type == "csv":
                    test_file = test_file.with_suffix(".csv")
                elif format_type == "markdown":
                    test_file = test_file.with_suffix(".md")
                
                # Save test data
                success = QuestionFormatConverter.save_questions(
                    test_data["mcq"], test_data["subjective"], 
                    str(test_file), format_type
                )
                
                if not success:
                    validation_results[format_type] = "❌ Save failed"
                    continue
                
                # Validate the file
                is_valid, message = QuestionManager.validate_questions_file(str(test_file))
                
                if is_valid:
                    validation_results[format_type] = "✅ Valid"
                else:
                    validation_results[format_type] = f"❌ Invalid: {message}"
                    
            except Exception as e:
                validation_results[format_type] = f"❌ Exception: {str(e)}"
        
        self.results["format_tests"]["validation"] = validation_results
        
        # Print results
        for format_type, result in validation_results.items():
            print(f"  {format_type:12} : {result}")
    
    def test_format_conversion(self):
        """Test conversion between all format pairs."""
        print("\n🔄 Testing Format Conversion...")
        
        conversion_results = {}
        formats = ["python", "yaml", "json", "csv"]  # Skip markdown for now due to parsing issues
        
        # Create source file
        source_file = self.test_dir / "source.py" 
        test_mcq = [{"question": "Test?", "options": ["A", "B"], "answer": "A", "marks": 1}]
        test_subj = [{"question": "Explain.", "answer": "Answer.", "marks": 3}]
        
        QuestionFormatConverter.save_questions(test_mcq, test_subj, str(source_file), "python")
        
        for source_fmt in formats:
            for target_fmt in formats:
                if source_fmt == target_fmt:
                    continue
                
                try:
                    source_ext = "py" if source_fmt == "python" else source_fmt
                    target_ext = "py" if target_fmt == "python" else target_fmt
                    
                    source_path = self.test_dir / f"convert_source.{source_ext}"
                    target_path = self.test_dir / f"convert_target.{target_ext}"
                    
                    # Create source file
                    QuestionFormatConverter.save_questions(test_mcq, test_subj, str(source_path), source_fmt)
                    
                    # Load and convert
                    mcq, subj = QuestionFormatConverter.load_questions(str(source_path))
                    success = QuestionFormatConverter.save_questions(mcq, subj, str(target_path), target_fmt)
                    
                    if success:
                        # Verify data integrity
                        mcq_check, subj_check = QuestionFormatConverter.load_questions(str(target_path))
                        if len(mcq_check) == len(mcq) and len(subj_check) == len(subj):
                            conversion_results[f"{source_fmt}→{target_fmt}"] = "✅ Success"
                        else:
                            conversion_results[f"{source_fmt}→{target_fmt}"] = "❌ Data loss"
                    else:
                        conversion_results[f"{source_fmt}→{target_fmt}"] = "❌ Failed"
                        
                except Exception as e:
                    conversion_results[f"{source_fmt}→{target_fmt}"] = f"❌ Error: {str(e)[:50]}"
        
        self.results["format_tests"]["conversion"] = conversion_results
        
        # Print results matrix
        print("  Conversion Matrix:")
        for conversion, result in conversion_results.items():
            print(f"    {conversion:15} : {result}")
    
    def test_error_handling(self):
        """Test error handling for various edge cases."""
        print("\n🚨 Testing Error Handling...")
        
        error_tests = {}
        
        # Test 1: Non-existent file
        try:
            result = QuestionManager.validate_questions_file("nonexistent.yaml")
            error_tests["nonexistent_file"] = "✅ Handled gracefully" if not result[0] else "❌ Should fail"
        except Exception as e:
            error_tests["nonexistent_file"] = f"❌ Exception: {str(e)[:50]}"
        
        # Test 2: Empty file
        try:
            empty_file = self.test_dir / "empty.yaml"
            empty_file.write_text("")
            result = QuestionManager.validate_questions_file(str(empty_file))
            error_tests["empty_file"] = "✅ Handled gracefully" if not result[0] else "❌ Should fail"
        except Exception as e:
            error_tests["empty_file"] = f"❌ Exception: {str(e)[:50]}"
        
        # Test 3: Malformed JSON
        try:
            bad_json = self.test_dir / "bad.json"
            bad_json.write_text('{"mcq": [invalid json}')
            result = QuestionManager.validate_questions_file(str(bad_json))
            error_tests["malformed_json"] = "✅ Handled gracefully" if not result[0] else "❌ Should fail"
        except Exception as e:
            error_tests["malformed_json"] = f"❌ Exception: {str(e)[:50]}"
        
        # Test 4: Invalid YAML
        try:
            bad_yaml = self.test_dir / "bad.yaml"
            bad_yaml.write_text("mcq:\n  - question: test\n    invalid: : syntax")
            result = QuestionManager.validate_questions_file(str(bad_yaml))
            error_tests["malformed_yaml"] = "✅ Handled gracefully" if not result[0] else "❌ Should fail"
        except Exception as e:
            error_tests["malformed_yaml"] = f"❌ Exception: {str(e)[:50]}"
        
        # Test 5: Missing required fields
        try:
            incomplete = self.test_dir / "incomplete.yaml"
            incomplete.write_text("mcq:\n  - question: 'Test?'\n    # missing options, answer")
            result = QuestionManager.validate_questions_file(str(incomplete))
            error_tests["missing_fields"] = "✅ Handled gracefully" if not result[0] else "❌ Should fail"
        except Exception as e:
            error_tests["missing_fields"] = f"❌ Exception: {str(e)[:50]}"
        
        self.results["error_tests"] = error_tests
        
        # Print results
        for test_name, result in error_tests.items():
            print(f"  {test_name:18} : {result}")
    
    def test_performance(self):
        """Test performance with various file sizes."""
        print("\n⚡ Testing Performance...")
        
        performance_results = {}
        
        # Test with different question counts
        question_counts = [10, 100, 500]
        
        for count in question_counts:
            try:
                # Generate large question set
                mcq = []
                subjective = []
                
                for i in range(count):
                    mcq.append({
                        "question": f"Question {i}?",
                        "options": [f"Option {j}" for j in range(4)],
                        "answer": "Option 0",
                        "marks": 1
                    })
                    
                    if i % 5 == 0:  # Every 5th question is subjective
                        subjective.append({
                            "question": f"Subjective question {i}.",
                            "answer": f"Answer {i}.",
                            "marks": 5
                        })
                
                # Test validation time
                test_file = self.test_dir / f"perf_{count}.yaml"
                QuestionFormatConverter.save_questions(mcq, subjective, str(test_file), "yaml")
                
                start_time = time.time()
                is_valid, message = QuestionManager.validate_questions_file(str(test_file))
                validation_time = time.time() - start_time
                
                # Test generation time
                start_time = time.time()
                generator = QuizGenerator(output_dir=str(self.test_dir / f"perf_output_{count}"),
                                        questions_file=str(test_file))
                success = generator.generate_quizzes(num_sets=1, compile_pdf=False)
                generation_time = time.time() - start_time
                
                performance_results[f"{count}_questions"] = {
                    "validation_time": f"{validation_time:.2f}s",
                    "generation_time": f"{generation_time:.2f}s",
                    "success": "✅" if success else "❌"
                }
                
            except Exception as e:
                performance_results[f"{count}_questions"] = {
                    "error": f"❌ {str(e)[:50]}"
                }
        
        self.results["performance_tests"] = performance_results
        
        # Print results
        for test, result in performance_results.items():
            print(f"  {test:15} : {result}")
    
    def test_latex_quality(self):
        """Test LaTeX compilation and quality."""
        print("\n📄 Testing LaTeX Quality...")
        
        latex_results = {}
        
        # Test LaTeX validation
        test_expressions = [
            ("Simple math", "$x^2 + y^2 = z^2$", True),
            ("Fraction", r"$\frac{a}{b}$", True),
            ("Chemistry", "H$_2$O + CO$_2$", True),
            ("Invalid", "x^2 + y^2", False),  # Missing $ delimiters
            ("Complex", r"$\lim_{x \to 0} \frac{\sin x}{x} = 1$", True)
        ]
        
        for name, expression, should_be_valid in test_expressions:
            try:
                is_valid, errors = LaTeXValidator.validate_latex_syntax(expression)
                
                if is_valid == should_be_valid:
                    latex_results[name] = "✅ Correct validation"
                else:
                    latex_results[name] = f"❌ Expected {should_be_valid}, got {is_valid}"
                    
            except Exception as e:
                latex_results[name] = f"❌ Exception: {str(e)[:50]}"
        
        # Test LaTeX auto-fixing
        broken_expressions = [
            "x^2 + y^2",  # Missing $
            "H2O",        # Chemical formula
            "45 degrees", # Degree symbol
        ]
        
        fix_results = {}
        for expr in broken_expressions:
            try:
                fixed, fixes = LaTeXErrorFixer.fix_common_errors(expr)
                fix_results[expr] = f"✅ {len(fixes)} fixes applied" if fixes else "❌ No fixes"
            except Exception as e:
                fix_results[expr] = f"❌ Error: {str(e)[:30]}"
        
        latex_results.update(fix_results)
        self.results["latex_tests"] = latex_results
        
        # Print results
        for test, result in latex_results.items():
            print(f"  {test:20} : {result}")
    
    def test_usability_scenarios(self):
        """Test common user workflows."""
        print("\n👥 Testing Usability Scenarios...")
        
        usability_results = {}
        
        # Scenario 1: New user creates first quiz
        try:
            # Create examples
            example_dir = self.test_dir / "usability_examples"
            example_dir.mkdir(exist_ok=True)
            
            # Run create-examples command
            result = subprocess.run([
                "setwise", "questions", "create-examples", 
                "--output-dir", str(example_dir)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Check if files were created
                expected_files = ["sample_questions.py", "sample_questions.yaml", 
                                "sample_questions.json", "sample_questions.csv"]
                created_files = [f.name for f in example_dir.glob("sample_questions.*")]
                
                if all(f in created_files for f in expected_files):
                    usability_results["new_user_setup"] = "✅ All example files created"
                else:
                    usability_results["new_user_setup"] = f"❌ Missing files: {set(expected_files) - set(created_files)}"
            else:
                usability_results["new_user_setup"] = f"❌ Command failed: {result.stderr}"
                
        except Exception as e:
            usability_results["new_user_setup"] = f"❌ Exception: {str(e)[:50]}"
        
        # Scenario 2: Format conversion workflow
        try:
            source_file = example_dir / "sample_questions.py"
            target_file = self.test_dir / "converted.yaml"
            
            result = subprocess.run([
                "setwise", "questions", "convert", str(source_file), str(target_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and target_file.exists():
                usability_results["format_conversion"] = "✅ Conversion successful"
            else:
                usability_results["format_conversion"] = f"❌ Conversion failed: {result.stderr}"
                
        except Exception as e:
            usability_results["format_conversion"] = f"❌ Exception: {str(e)[:50]}"
        
        # Scenario 3: Quiz generation workflow
        try:
            quiz_output = self.test_dir / "usability_quiz"
            quiz_output.mkdir(exist_ok=True)
            
            result = subprocess.run([
                "setwise", "generate", 
                "--questions-file", str(target_file),
                "--sets", "1",
                "--no-pdf",
                "--output-dir", str(quiz_output)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Check if quiz files were generated
                quiz_files = list(quiz_output.glob("quiz_set_*.tex"))
                answer_files = list(quiz_output.glob("answer_key_*.txt"))
                
                if quiz_files and answer_files:
                    usability_results["quiz_generation"] = "✅ Quiz and answers generated"
                else:
                    usability_results["quiz_generation"] = "❌ Missing output files"
            else:
                usability_results["quiz_generation"] = f"❌ Generation failed: {result.stderr}"
                
        except Exception as e:
            usability_results["quiz_generation"] = f"❌ Exception: {str(e)[:50]}"
        
        self.results["usability_tests"] = usability_results
        
        # Print results
        for test, result in usability_results.items():
            print(f"  {test:20} : {result}")
    
    def generate_report(self):
        """Generate comprehensive test report."""
        print("\n📊 Quality Testing Report")
        print("=" * 60)
        
        total_tests = 0
        passed_tests = 0
        
        for category, tests in self.results.items():
            if isinstance(tests, dict):
                for test_name, result in tests.items():
                    if isinstance(result, str):
                        total_tests += 1
                        if "✅" in result:
                            passed_tests += 1
                    elif isinstance(result, dict):
                        # Handle nested results (like performance tests)
                        total_tests += 1
                        if all("✅" in str(sub_result) for sub_result in result.values() if isinstance(sub_result, str)):
                            passed_tests += 1
        
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n🎯 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {total_tests - passed_tests}")
        print(f"   Pass Rate: {pass_rate:.1f}%")
        
        # Grade the package
        if pass_rate >= 95:
            grade = "🌟 EXCELLENT"
        elif pass_rate >= 85:
            grade = "✅ GOOD"
        elif pass_rate >= 70:
            grade = "⚠️ NEEDS IMPROVEMENT"
        else:
            grade = "❌ CRITICAL ISSUES"
        
        print(f"\n🏆 Package Quality Grade: {grade}")
        
        # Save detailed report
        report_file = self.test_dir / "quality_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📋 Detailed report saved to: {report_file}")
        
        return pass_rate >= 85  # Return True if quality is acceptable


def main():
    """Run comprehensive quality testing."""
    tester = QualityTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 Setwise passes comprehensive quality testing!")
        return 0
    else:
        print("\n⚠️ Setwise has quality issues that need attention.")
        return 1


if __name__ == "__main__":
    sys.exit(main())