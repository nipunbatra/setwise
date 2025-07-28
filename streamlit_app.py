import streamlit as st
import tempfile
import os
import sys
import subprocess
from pathlib import Path
import base64
from io import BytesIO

# Add the setwise package to path for import
sys.path.insert(0, str(Path(__file__).parent))

from setwise.quiz_generator import QuizGenerator
from setwise.formats import QuestionFormatConverter

st.set_page_config(
    page_title="Setwise Quiz Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_example_questions(subject):
    """Load example questions for different subjects"""
    examples = {
        "Physics": '''mcq_questions = [
    {
        "question": r"What is the SI unit of force?",
        "options": [
            r"Joule",
            r"Newton", 
            r"Watt",
            r"Pascal"
        ],
        "answer": r"Newton",
        "marks": 1
    },
    {
        "question": r"The acceleration due to gravity on Earth is approximately:",
        "options": [
            r"$9.8 \\, \\text{m/s}^2$",
            r"$10 \\, \\text{m/s}^2$",
            r"$8.9 \\, \\text{m/s}^2$",
            r"$11 \\, \\text{m/s}^2$"
        ],
        "answer": r"$9.8 \\, \\text{m/s}^2$",
        "marks": 1
    }
]

subjective_questions = [
    {
        "question": r"Derive the equation for kinetic energy. Show that $KE = \\frac{1}{2}mv^2$.",
        "answer": r"Starting with Newton's second law and work-energy theorem...",
        "marks": 5
    }
]''',
        "Mathematics": '''mcq_questions = [
    {
        "question": r"What is the derivative of $\\sin(x)$?",
        "options": [
            r"$\\cos(x)$",
            r"$-\\cos(x)$",
            r"$\\tan(x)$",
            r"$-\\sin(x)$"
        ],
        "answer": r"$\\cos(x)$",
        "marks": 1
    },
    {
        "question": r"The integral $\\int x^2 dx$ equals:",
        "options": [
            r"$\\frac{x^3}{3} + C$",
            r"$2x + C$",
            r"$x^3 + C$",
            r"$\\frac{x^2}{2} + C$"
        ],
        "answer": r"$\\frac{x^3}{3} + C$",
        "marks": 1
    }
]

subjective_questions = [
    {
        "question": r"Prove that the sum of first $n$ natural numbers is $\\frac{n(n+1)}{2}$.",
        "answer": r"We can prove this using mathematical induction...",
        "marks": 5
    }
]''',
        "Programming": '''mcq_questions = [
    {
        "question": r"Which of the following is used to create a list in Python?",
        "options": [
            r"[]",
            r"{}",
            r"()",
            r"<>"
        ],
        "answer": r"[]",
        "marks": 1
    },
    {
        "question": r"What is the time complexity of binary search?",
        "options": [
            r"$O(n)$",
            r"$O(\\log n)$",
            r"$O(n^2)$",
            r"$O(1)$"
        ],
        "answer": r"$O(\\log n)$",
        "marks": 1
    }
]

subjective_questions = [
    {
        "question": r"Explain the concept of recursion with an example. Write a recursive function to calculate factorial.",
        "answer": r"Recursion is when a function calls itself. Example: def factorial(n): return 1 if n <= 1 else n * factorial(n-1)",
        "marks": 5
    }
]'''
    }
    return examples.get(subject, "")

def generate_quiz_preview(questions_text, template, num_sets):
    """Generate quiz preview PDFs"""
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
        
        # Find generated PDFs
        pdf_files = []
        for i in range(1, num_sets + 1):
            pdf_path = os.path.join(output_dir, f'quiz_set_{i}.pdf')
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()
                pdf_files.append({
                    'name': f'Quiz Set {i}',
                    'data': pdf_data,
                    'path': pdf_path
                })
        
        # Cleanup
        os.unlink(questions_file)
        
        return pdf_files, None
        
    except Exception as e:
        return None, f"Error generating quiz: {str(e)}"

def display_pdf(pdf_data, height=600):
    """Display PDF in iframe"""
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    pdf_display = f'''
    <iframe src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" height="{height}px" type="application/pdf">
    </iframe>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.title("🎯 Setwise Quiz Generator")
    st.markdown("Create professional LaTeX quizzes with live preview")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Template selection
        template = st.selectbox(
            "Template",
            ["default", "compact", "minimal"],
            help="Choose quiz template style"
        )
        
        # Number of sets
        num_sets = st.slider(
            "Number of Sets",
            min_value=1,
            max_value=5,
            value=2,
            help="Generate multiple quiz variations"
        )
        
        st.header("📚 Examples")
        example_subject = st.selectbox(
            "Load Example",
            ["", "Physics", "Mathematics", "Programming"],
            help="Load sample questions"
        )
        
        if st.button("Load Example", disabled=not example_subject):
            st.session_state.questions_text = load_example_questions(example_subject)
            st.rerun()
    
    # Main layout - two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Questions Editor")
        
        # Initialize session state
        if 'questions_text' not in st.session_state:
            st.session_state.questions_text = '''mcq_questions = [
    {
        "question": r"What is the capital of France?",
        "options": [
            r"London",
            r"Berlin",
            r"Paris",
            r"Madrid"
        ],
        "answer": r"Paris",
        "marks": 1
    }
]

subjective_questions = [
    {
        "question": r"Explain the concept of democracy.",
        "answer": r"Democracy is a system of government...",
        "marks": 5
    }
]'''
        
        # Text area for questions
        questions_text = st.text_area(
            "Questions (Python format)",
            value=st.session_state.questions_text,
            height=400,
            help="Edit your questions here. Use Python dictionary format.",
            key="questions_editor"
        )
        
        # Update session state
        st.session_state.questions_text = questions_text
        
        # Validation
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            if st.button("🔍 Validate", type="secondary"):
                try:
                    exec(questions_text)
                    st.success("✅ Questions format is valid!")
                except Exception as e:
                    st.error(f"❌ Syntax error: {str(e)}")
        
        with col1_2:
            if st.button("🚀 Generate Preview", type="primary"):
                st.session_state.generate_preview = True
                st.rerun()
    
    with col2:
        st.header("👀 Live Preview")
        
        if st.session_state.get('generate_preview', False) and questions_text.strip():
            with st.spinner(f"Generating {num_sets} quiz set(s)..."):
                pdf_files, error = generate_quiz_preview(questions_text, template, num_sets)
            
            if error:
                st.error(error)
            elif pdf_files:
                # Display each PDF set
                for i, pdf_file in enumerate(pdf_files):
                    st.subheader(f"📄 {pdf_file['name']}")
                    
                    # Display PDF
                    display_pdf(pdf_file['data'], height=400)
                    
                    # Download button
                    st.download_button(
                        label=f"⬇️ Download {pdf_file['name']}",
                        data=pdf_file['data'],
                        file_name=f"quiz_set_{i+1}.pdf",
                        mime="application/pdf"
                    )
                    
                    if i < len(pdf_files) - 1:
                        st.divider()
                
                # Reset generate flag
                st.session_state.generate_preview = False
            else:
                st.warning("No PDFs generated. Check your questions format.")
        else:
            st.info("📋 Enter questions and click 'Generate Preview' to see live preview")
            st.markdown("""
            **Features:**
            - 📝 Real-time editing
            - 👀 Live PDF preview
            - 📄 Multiple quiz sets
            - ⬇️ Direct downloads
            - 🎨 Template options
            - 📚 Example questions
            """)

if __name__ == "__main__":
    main()