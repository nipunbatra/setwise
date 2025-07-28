#!/usr/bin/env python3
"""
Simple Setwise Web Interface 
Clean split-pane design: questions editor on left, PDF previews on right
"""

import streamlit as st
import tempfile
import subprocess
import os
import base64
from pathlib import Path

st.set_page_config(
    page_title="Setwise Quiz Generator",
    page_icon="🎯",
    layout="wide"
)

def load_example_questions(subject):
    """Load example questions for different subjects"""
    examples = {
        "Physics": '''mcq = [
    {
        "question": r"What is the SI unit of force?",
        "options": [r"Joule", r"Newton", r"Watt", r"Pascal"],
        "answer": r"Newton",
        "marks": 1
    },
    {
        "question": r"The acceleration due to gravity is approximately:",
        "options": [r"$9.8\\,\\text{m/s}^2$", r"$10\\,\\text{m/s}^2$", r"$8.9\\,\\text{m/s}^2$", r"$11\\,\\text{m/s}^2$"],
        "answer": r"$9.8\\,\\text{m/s}^2$",
        "marks": 1
    }
]

subjective = [
    {
        "question": r"Derive the kinetic energy formula. Show that $KE = \\frac{1}{2}mv^2$.",
        "answer": r"Starting with Newton's second law and work-energy theorem...",
        "marks": 5
    }
]''',
        
        "Mathematics": '''mcq = [
    {
        "question": r"What is the derivative of $\\sin(x)$?",
        "options": [r"$\\cos(x)$", r"$-\\cos(x)$", r"$\\tan(x)$", r"$-\\sin(x)$"],
        "answer": r"$\\cos(x)$",
        "marks": 1
    },
    {
        "question": r"The integral $\\int x^2 dx$ equals:",
        "options": [r"$\\frac{x^3}{3} + C$", r"$2x + C$", r"$x^3 + C$", r"$\\frac{x^2}{2} + C$"],
        "answer": r"$\\frac{x^3}{3} + C$",
        "marks": 1
    }
]

subjective = [
    {
        "question": r"Prove that $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$.",
        "answer": r"We can prove this using mathematical induction...",
        "marks": 5
    }
]''',

        "Programming": '''mcq = [
    {
        "question": r"Which creates a list in Python?",
        "options": [r"[]", r"{}", r"()", r"<>"],
        "answer": r"[]",
        "marks": 1
    },
    {
        "question": r"Time complexity of binary search?",
        "options": [r"$O(n)$", r"$O(\\log n)$", r"$O(n^2)$", r"$O(1)$"],
        "answer": r"$O(\\log n)$",
        "marks": 1
    }
]

subjective = [
    {
        "question": r"Explain recursion. Write recursive factorial function.",
        "answer": r"def factorial(n): return 1 if n <= 1 else n * factorial(n-1)",
        "marks": 5
    }
]'''
    }
    return examples.get(subject, "")

def generate_quiz_pdfs(questions_text, template, num_sets):
    """Generate quiz PDFs and return their data with answer keys"""
    try:
        # Create temporary file for questions
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(questions_text)
            questions_file = f.name
        
        # Create temporary output directory
        output_dir = tempfile.mkdtemp()
        
        # Generate quiz using CLI
        cmd = [
            'setwise', 'generate',
            '--questions-file', questions_file,
            '--output-dir', output_dir,
            '--sets', str(num_sets),
            '--template', template,
            '--seed', '42'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return None, f"Error: {result.stderr}"
        
        # Collect generated PDFs and answer keys
        quiz_sets = []
        for i in range(1, num_sets + 1):
            pdf_path = os.path.join(output_dir, f'quiz_set_{i}.pdf')
            answer_path = os.path.join(output_dir, f'answer_key_{i}.txt')
            
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()
                
                answer_key = ""
                if os.path.exists(answer_path):
                    with open(answer_path, 'r') as f:
                        answer_key = f.read()
                
                quiz_sets.append({
                    'name': f'Quiz Set {i}',
                    'pdf_data': pdf_data,
                    'answer_key': answer_key
                })
        
        # Cleanup
        os.unlink(questions_file)
        
        return quiz_sets, None
        
    except Exception as e:
        return None, f"Error: {str(e)}"

def display_pdf_embed(pdf_data, height=400):
    """Display PDF using iframe"""
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    pdf_html = f'''
    <iframe src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" height="{height}px" type="application/pdf"
            style="border: 1px solid #ddd; border-radius: 4px;">
    </iframe>
    '''
    st.markdown(pdf_html, unsafe_allow_html=True)

def main():
    # Custom CSS for better appearance
    st.markdown("""
    <style>
    .main > div { padding-top: 1rem; }
    .stTextArea textarea { 
        font-family: 'Monaco', 'Courier New', monospace;
        font-size: 14px;
    }
    .quiz-set-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        background: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Setwise Quiz Generator")
    st.markdown("Simple interface: Edit questions → Generate PDFs → Download")
    
    # Controls row
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns([1, 1, 1, 2])
    
    with col_ctrl1:
        template = st.selectbox("Template", ["default", "compact", "minimal"])
    
    with col_ctrl2:
        num_sets = st.slider("Sets", 1, 5, 2)
    
    with col_ctrl3:
        example = st.selectbox("Examples", ["", "Physics", "Mathematics", "Programming"])
    
    with col_ctrl4:
        if st.button("Load Example", disabled=not example):
            st.session_state.questions = load_example_questions(example)
            st.rerun()
    
    # Main split pane layout
    col_left, col_right = st.columns([1, 1])
    
    # LEFT PANE: Questions Editor
    with col_left:
        st.subheader("Questions Editor")
        
        # Initialize default questions
        if 'questions' not in st.session_state:
            st.session_state.questions = '''mcq = [
    {
        "question": r"What is $2 + 2$?",
        "options": [r"3", r"4", r"5", r"6"],
        "answer": r"4",
        "marks": 1
    }
]

subjective = [
    {
        "question": r"Explain a concept you want to test.",
        "answer": r"Provide the expected answer here.",
        "marks": 5
    }
]'''
        
        # Text editor
        questions_text = st.text_area(
            "Questions (Python format)",
            value=st.session_state.questions,
            height=500,
            key="editor"
        )
        
        # Update session state
        st.session_state.questions = questions_text
        
        # Generate button
        if st.button("Generate Quiz Sets", type="primary", use_container_width=True):
            st.session_state.generate_now = True
            st.rerun()
    
    # RIGHT PANE: PDF Previews (X rows where X = num_sets)
    with col_right:
        st.subheader(f"PDF Preview ({num_sets} sets)")
        
        if st.session_state.get('generate_now', False) and questions_text.strip():
            with st.spinner(f"Generating {num_sets} quiz sets..."):
                quiz_sets, error = generate_quiz_pdfs(questions_text, template, num_sets)
            
            if error:
                st.error(error)
            elif quiz_sets:
                # Display each PDF set in rows
                for i, quiz_set in enumerate(quiz_sets):
                    st.markdown(f"**{quiz_set['name']}**")
                    
                    # Three sub-columns: PDF preview, downloads, answer key
                    sub_col1, sub_col2, sub_col3 = st.columns([2, 1, 1])
                    
                    with sub_col1:
                        display_pdf_embed(quiz_set['pdf_data'])
                    
                    with sub_col2:
                        st.download_button(
                            label="Download PDF",
                            data=quiz_set['pdf_data'],
                            file_name=f"quiz_set_{i+1}.pdf",
                            mime="application/pdf",
                            key=f"download_pdf_{i}",
                            use_container_width=True
                        )
                    
                    with sub_col3:
                        if quiz_set['answer_key']:
                            st.download_button(
                                label="Download Answers",
                                data=quiz_set['answer_key'],
                                file_name=f"answer_key_{i+1}.txt",
                                mime="text/plain",
                                key=f"download_answers_{i}",
                                use_container_width=True
                            )
                            
                            # Show preview of answer key
                            with st.expander("View Answers"):
                                st.text(quiz_set['answer_key'])
                    
                    # Add spacing between sets
                    if i < len(quiz_sets) - 1:
                        st.markdown("---")
                
                # Reset generate flag
                st.session_state.generate_now = False
            else:
                st.warning("No PDFs generated")
        else:
            # Show instructions when no preview
            st.info("Enter questions and click 'Generate Quiz Sets'")
            st.markdown("""
            **How to use:**
            1. Edit questions in left pane
            2. Choose template and number of sets
            3. Click generate to see live PDF previews
            4. Download PDFs and answer keys
            
            **Question format:**
            - Use `mcq` and `subjective` arrays (not mcq_questions)
            - LaTeX math: `r"What is $x^2$?"`
            - MCQ needs `answer` field matching an option
            """)

if __name__ == "__main__":
    main()