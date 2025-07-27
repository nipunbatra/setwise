#!/usr/bin/env python3
"""
Setwise Web Interface using Streamlit

A user-friendly web interface for generating quizzes without command-line usage.
Makes it easy for educators to create quizzes with LaTeX validation and preview.

Usage: streamlit run setwise_web.py
"""

import streamlit as st
import tempfile
import zipfile
from pathlib import Path
import os
import sys

# Add setwise to path if running from repo
if Path('setwise').exists():
    sys.path.insert(0, str(Path.cwd()))

try:
    from setwise import QuizGenerator, TemplateManager
    from setwise.question_manager import QuestionManager
    from setwise.latex_validator import LaTeXValidator, LaTeXErrorFixer
except ImportError:
    st.error("""
    Setwise package not found. Please install it first:
    
    ```bash
    pip install git+https://github.com/nipunbatra/setwise.git
    ```
    """)
    st.stop()


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Setwise Quiz Generator",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Setwise Quiz Generator")
    st.markdown("**Professional LaTeX Quiz Generator with Custom Question Libraries**")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Generate Quiz", "Question Library Manager", "LaTeX Help", "Examples"]
    )
    
    if page == "Generate Quiz":
        generate_quiz_page()
    elif page == "Question Library Manager":
        question_manager_page()
    elif page == "LaTeX Help":
        latex_help_page()
    elif page == "Examples":
        examples_page()


def generate_quiz_page():
    """Quiz generation interface."""
    st.header("Generate Quiz")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Quiz Configuration")
        
        # Quiz parameters
        num_sets = st.number_input("Number of quiz sets", min_value=1, max_value=10, value=3)
        seed = st.number_input("Random seed (for reproducibility)", value=42, help="Use the same seed to generate identical quizzes")
        
        col_a, col_b = st.columns(2)
        with col_a:
            num_mcq = st.number_input("MCQ questions per set", min_value=0, value=None, help="Leave empty for all available")
        with col_b:
            num_subjective = st.number_input("Subjective questions per set", min_value=0, value=None, help="Leave empty for all available")
        
        # Template selection
        try:
            tm = TemplateManager()
            templates = ["default", "compact", "minimal"]  # Known templates
            template = st.selectbox("Template", templates, help="Choose quiz layout style")
        except:
            template = "default"
            st.warning("Could not load template manager, using default template")
        
        compile_pdf = st.checkbox("Compile to PDF", value=True, help="Uncheck to generate only LaTeX files")
    
    with col2:
        st.subheader("Question Source")
        
        # Question source options
        source_type = st.radio(
            "Question source:",
            ["Built-in ML Questions", "Upload Custom Questions", "Create New Questions"]
        )
        
        custom_questions_file = None
        
        if source_type == "Upload Custom Questions":
            uploaded_file = st.file_uploader(
                "Upload questions.py file",
                type=['py'],
                help="Upload a Python file with MCQ and subjective questions"
            )
            
            if uploaded_file:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                    f.write(uploaded_file.read().decode('utf-8'))
                    custom_questions_file = f.name
                
                # Validate the uploaded file
                is_valid, message = QuestionManager.validate_questions_file(custom_questions_file)
                if is_valid:
                    st.success(f"Valid questions file: {message}")
                else:
                    st.error(f"Invalid questions file: {message}")
                    custom_questions_file = None
        
        elif source_type == "Create New Questions":
            st.info("Use the 'Question Library Manager' page to create and edit questions")
    
    # Generate button
    if st.button("Generate Quiz", type="primary", use_container_width=True):
        if source_type == "Upload Custom Questions" and not custom_questions_file:
            st.error("Please upload a valid questions file")
            return
        
        with st.spinner("Generating quiz..."):
            try:
                # Create temporary directory for output
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Initialize quiz generator
                    generator = QuizGenerator(
                        output_dir=temp_dir,
                        questions_file=custom_questions_file if source_type == "Upload Custom Questions" else None
                    )
                    
                    # Generate quizzes
                    success = generator.generate_quizzes(
                        num_sets=num_sets,
                        num_mcq=num_mcq if num_mcq > 0 else None,
                        num_subjective=num_subjective if num_subjective > 0 else None,
                        template_name=template,
                        compile_pdf=compile_pdf,
                        seed=seed
                    )
                    
                    if success:
                        st.success(f"Successfully generated {num_sets} quiz sets!")
                        
                        # Create download package
                        zip_path = create_download_package(temp_dir, num_sets, compile_pdf)
                        
                        # Offer download
                        with open(zip_path, 'rb') as f:
                            st.download_button(
                                label="Download Quiz Files",
                                data=f.read(),
                                file_name="quiz_sets.zip",
                                mime="application/zip"
                            )
                        
                        # Show preview of first quiz
                        show_quiz_preview(temp_dir, compile_pdf)
                    
                    else:
                        st.error("Quiz generation failed. Check the logs above for details.")
            
            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}")
        
        # Clean up temporary file
        if custom_questions_file and os.path.exists(custom_questions_file):
            os.unlink(custom_questions_file)


def question_manager_page():
    """Question library management interface."""
    st.header("Question Library Manager")
    
    tab1, tab2, tab3 = st.tabs(["Create Questions", "Validate Questions", "Fix LaTeX"])
    
    with tab1:
        st.subheader("Create New Questions File")
        
        # Question file creator
        subject = st.text_input("Subject/Topic", placeholder="e.g., Physics, Chemistry, Mathematics")
        
        st.markdown("### Sample MCQ Question")
        mcq_question = st.text_area(
            "Question text (LaTeX supported)",
            placeholder=r"What is the derivative of $f(x) = x^2$?",
            height=100
        )
        
        mcq_options = []
        for i in range(4):
            option = st.text_input(f"Option {i+1}", key=f"mcq_option_{i}")
            if option:
                mcq_options.append(option)
        
        correct_answer = st.selectbox("Correct answer", mcq_options if mcq_options else [""])
        mcq_marks = st.number_input("Marks for MCQ", min_value=1, value=1)
        
        st.markdown("### Sample Subjective Question")
        subj_question = st.text_area(
            "Question text (LaTeX supported)",
            placeholder=r"Derive the quadratic formula starting from $ax^2 + bx + c = 0$.",
            height=100
        )
        subj_answer = st.text_area(
            "Sample answer/solution",
            placeholder="Detailed solution steps...",
            height=100
        )
        subj_marks = st.number_input("Marks for subjective", min_value=1, value=5)
        
        if st.button("Generate Questions File"):
            if mcq_question and len(mcq_options) >= 2 and correct_answer:
                questions_content = generate_questions_file_content(
                    subject, mcq_question, mcq_options, correct_answer, mcq_marks,
                    subj_question, subj_answer, subj_marks
                )
                
                st.download_button(
                    label="Download Questions File",
                    data=questions_content,
                    file_name=f"{subject.lower().replace(' ', '_')}_questions.py",
                    mime="text/plain"
                )
                
                st.success("Questions file generated! Download and use with the quiz generator.")
            else:
                st.error("Please fill in all required fields for at least one complete MCQ question.")
    
    with tab2:
        st.subheader("Validate Questions File")
        
        uploaded_file = st.file_uploader(
            "Upload questions.py file to validate",
            type=['py'],
            key="validate_upload"
        )
        
        if uploaded_file:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(uploaded_file.read().decode('utf-8'))
                temp_file = f.name
            
            try:
                # Validate file
                is_valid, message = QuestionManager.validate_questions_file(temp_file)
                
                if is_valid:
                    st.success(f"✅ {message}")
                    
                    # Show statistics
                    stats = QuestionManager.get_question_stats(temp_file)
                    if 'error' not in stats:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Questions", stats['total_questions'])
                        with col2:
                            st.metric("MCQ Questions", stats['mcq_count'])
                        with col3:
                            st.metric("Subjective Questions", stats['subjective_count'])
                        
                        st.metric("Total Marks", stats['total_marks'])
                else:
                    st.error(f"❌ {message}")
                    
                    # Offer to fix common errors
                    st.markdown("### Automatic Fixes Available")
                    content = uploaded_file.read().decode('utf-8')
                    fixed_content, fixes = LaTeXErrorFixer.fix_common_errors(content)
                    
                    if fixes:
                        st.info("The following fixes can be applied automatically:")
                        for fix in fixes:
                            st.write(f"• {fix}")
                        
                        st.download_button(
                            label="Download Fixed File",
                            data=fixed_content,
                            file_name=f"fixed_{uploaded_file.name}",
                            mime="text/plain"
                        )
                    else:
                        st.warning("No automatic fixes available. Please check the error message above.")
            
            finally:
                os.unlink(temp_file)
    
    with tab3:
        st.subheader("Fix LaTeX Errors")
        
        st.markdown("""
        Upload a questions file to automatically fix common LaTeX syntax errors:
        - Missing $ delimiters for math expressions
        - Unescaped special characters
        - Common chemistry formulas
        - Degree symbols
        """)
        
        uploaded_file = st.file_uploader(
            "Upload questions.py file to fix",
            type=['py'],
            key="fix_upload"
        )
        
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            fixed_content, fixes = LaTeXErrorFixer.fix_common_errors(content)
            
            if fixes:
                st.success("Applied the following fixes:")
                for fix in fixes:
                    st.write(f"• {fix}")
                
                # Show diff preview
                with st.expander("Preview Changes"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original:**")
                        st.code(content[:500] + "..." if len(content) > 500 else content)
                    with col2:
                        st.markdown("**Fixed:**")
                        st.code(fixed_content[:500] + "..." if len(fixed_content) > 500 else fixed_content)
                
                st.download_button(
                    label="Download Fixed File",
                    data=fixed_content,
                    file_name=f"fixed_{uploaded_file.name}",
                    mime="text/plain"
                )
            else:
                st.info("No automatic fixes needed - the file looks good!")


def latex_help_page():
    """LaTeX help and reference."""
    st.header("LaTeX Help")
    
    st.markdown(LaTeXValidator.get_latex_help())
    
    st.subheader("Interactive LaTeX Tester")
    
    latex_input = st.text_area(
        "Test your LaTeX here:",
        placeholder=r"Enter LaTeX text like: The quadratic formula is $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$",
        height=100
    )
    
    if latex_input:
        is_valid, errors = LaTeXValidator.validate_latex_syntax(latex_input)
        
        if is_valid:
            st.success("✅ Valid LaTeX syntax!")
        else:
            st.error("❌ LaTeX syntax errors found:")
            for error in errors:
                st.write(f"• {error}")
        
        # Suggest fixes
        fixed_text, fixes = LaTeXErrorFixer.fix_common_errors(latex_input)
        if fixes:
            st.subheader("Suggested Fixes:")
            for fix in fixes:
                st.write(f"• {fix}")
            
            st.markdown("**Fixed version:**")
            st.code(fixed_text)


def examples_page():
    """Show examples of different subject question libraries."""
    st.header("Example Question Libraries")
    
    st.markdown("""
    Here are example question libraries for different subjects that you can download and use as templates:
    """)
    
    examples = [
        {
            "subject": "Physics",
            "description": "Mechanics, electricity, and wave physics with LaTeX equations",
            "file": "examples/physics_questions.py"
        },
        {
            "subject": "Chemistry", 
            "description": "Chemical equations, molarity calculations, and equilibrium",
            "file": "examples/chemistry_questions.py"
        },
        {
            "subject": "Mathematics",
            "description": "Calculus, algebra, and statistics with proper math notation",
            "file": "examples/mathematics_questions.py"
        },
        {
            "subject": "Computer Science",
            "description": "Algorithms, data structures, and programming concepts",
            "file": "examples/computer_science_questions.py"
        }
    ]
    
    for example in examples:
        with st.expander(f"{example['subject']} Questions"):
            st.markdown(f"**Description:** {example['description']}")
            
            # Try to load and show preview
            try:
                if Path(example['file']).exists():
                    with open(example['file'], 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    st.markdown("**Preview:**")
                    st.code(content[:800] + "..." if len(content) > 800 else content, language='python')
                    
                    st.download_button(
                        label=f"Download {example['subject']} Questions",
                        data=content,
                        file_name=f"{example['subject'].lower()}_questions.py",
                        mime="text/plain",
                        key=f"download_{example['subject']}"
                    )
                else:
                    st.warning(f"Example file not found: {example['file']}")
            except Exception as e:
                st.error(f"Error loading example: {e}")


def create_download_package(temp_dir: str, num_sets: int, include_pdf: bool) -> str:
    """Create a zip file with all generated quiz files."""
    zip_path = Path(temp_dir) / "quiz_sets.zip"
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        temp_path = Path(temp_dir)
        
        # Add LaTeX files
        for tex_file in temp_path.glob("*.tex"):
            zipf.write(tex_file, tex_file.name)
        
        # Add PDF files if they exist
        if include_pdf:
            for pdf_file in temp_path.glob("*.pdf"):
                zipf.write(pdf_file, pdf_file.name)
        
        # Add answer keys
        for answer_file in temp_path.glob("*.txt"):
            zipf.write(answer_file, answer_file.name)
    
    return str(zip_path)


def show_quiz_preview(temp_dir: str, include_pdf: bool):
    """Show preview of the first generated quiz."""
    temp_path = Path(temp_dir)
    
    # Find first quiz file
    tex_files = list(temp_path.glob("quiz_set_*.tex"))
    if tex_files:
        st.subheader("Preview: First Quiz")
        
        with open(tex_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Show LaTeX source
        with st.expander("LaTeX Source"):
            st.code(content, language='latex')
        
        # Show answer key if available
        answer_files = list(temp_path.glob("answer_key_*.txt"))
        if answer_files:
            with st.expander("Answer Key"):
                with open(answer_files[0], 'r', encoding='utf-8') as f:
                    st.text(f.read())


def generate_questions_file_content(subject, mcq_q, mcq_opts, mcq_ans, mcq_marks, subj_q, subj_ans, subj_marks):
    """Generate a complete questions.py file content."""
    options_str = ',\n            '.join([f'r"{opt}"' for opt in mcq_opts])
    
    return f'''"""
{subject} Questions for Setwise Quiz Generator

Custom question library created using the Setwise web interface.
Usage: setwise generate --questions-file {subject.lower().replace(' ', '_')}_questions.py
"""

# Multiple Choice Questions
mcq = [
    {{
        "question": r"""{mcq_q}""",
        "options": [
            {options_str}
        ],
        "answer": r"{mcq_ans}",
        "marks": {mcq_marks}
    }}
]

# Subjective Questions
subjective = [
    {{
        "question": r"""{subj_q}""",
        "answer": r"""{subj_ans}""",
        "marks": {subj_marks}
    }}
]
'''


if __name__ == "__main__":
    main()