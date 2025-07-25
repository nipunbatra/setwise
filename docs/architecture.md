# Setwise System Architecture

## Data Flow Diagram

```mermaid
graph TD
    A[CLI Arguments] --> B[main.py]
    B --> C[validate_inputs()]
    C --> D[Parse Arguments]
    D --> E{Template Selection?}
    E -->|default| F[quiz_template.tex.jinja]
    E -->|compact| G[quiz_template_compact.tex.jinja]
    E -->|academic| H[quiz_template_academic.tex.jinja]
    E -->|minimal| I[quiz_template_minimal.tex.jinja]
    
    H[data/questions.py] --> I[MCQ Questions<br/>20 questions, 5-6 options]
    H --> J[Subjective Questions<br/>15 questions with templates]
    
    I --> K[shuffle_mcq_options()]
    J --> L[process_subjective_questions()]
    
    K --> M[generate_quiz_set()]
    L --> M
    F --> M
    G --> M
    H --> M
    I --> M
    
    M --> N[Jinja2 Template Engine]
    N --> O[LaTeX Content]
    O --> P[quiz_set_N.tex]
    O --> Q[answer_key_N.txt]
    
    P --> R{PDF Compilation?}
    R -->|Yes| S[pdflatex]
    R -->|No| T[LaTeX Only]
    S --> U[quiz_set_N.pdf]
    
    V[figures/] --> W[TikZ Diagrams<br/>decision_tree.tikz<br/>neural_network.tikz<br/>svm_margin.tikz]
    V --> X[Matplotlib Plots<br/>roc_curve.pdf<br/>learning_curves.pdf<br/>classification_boundary.pdf]
    
    W --> N
    X --> N
    
    Y[GitHub Actions] --> Z[generate_figures.py]
    Z --> V
    Y --> AA[Deploy to GitHub Pages]
    AA --> BB[Quarto Site]
    BB --> CC[https://nipunbatra.github.io/setwise/]
```

## Component Breakdown

### 1. Input Layer
- **CLI Arguments**: User-specified parameters (seed, sets, questions, template selection)
- **Question Database**: Structured MCQ and subjective questions with metadata
- **Template System**: 4 built-in Jinja2 LaTeX templates with management system

### 2. Processing Layer
- **Validation**: Input validation and system requirements check
- **Randomization**: Question shuffling and option randomization
- **Template Processing**: Variable substitution in templated questions
- **Content Generation**: LaTeX document creation via Jinja2

### 3. Output Layer
- **LaTeX Files**: Human-readable quiz source code
- **PDF Files**: Compiled professional quiz documents
- **Answer Keys**: Text files with correct answers and explanations

### 4. Deployment Layer
- **GitHub Actions**: Automated CI/CD pipeline
- **Figure Generation**: Automated TikZ and matplotlib content creation
- **GitHub Pages**: Quarto-based documentation website

## Key Features

### Randomization Strategy
```mermaid
graph LR
    A[Same Questions] --> B[Shuffle Order]
    B --> C[Shuffle MCQ Options]  
    C --> D[Randomize Template Variables]
    D --> E[Different Quiz Sets]
```

### Template System
```mermaid
graph TD
    A[questions.py] --> B{Question Type?}
    B -->|MCQ| C[Static Content]
    B -->|Templated Subjective| D[Jinja2 Variables]
    B -->|Non-templated Subjective| E[Static Content]
    
    C --> F[Direct Rendering]
    D --> G[Variable Substitution]
    E --> F
    G --> F
    F --> H[LaTeX Output]
```

### Template Management System
```mermaid
graph TD
    A[CLI: --template NAME] --> B[TemplateManager]
    B --> C{Template Selection}
    
    C -->|default| D[quiz_template.tex.jinja<br/>- Single column<br/>- Color-coded sections<br/>- Professional styling<br/>- 4-6 pages]
    
    C -->|compact| E[quiz_template_compact.tex.jinja<br/>- Two column layout<br/>- Multi-column MCQ options<br/>- Reduced spacing<br/>- 2-3 pages]
    
    C -->|academic| F[quiz_template_academic.tex.jinja<br/>- Traditional format<br/>- Minimal colors<br/>- Standard typography<br/>- 3-5 pages]
    
    C -->|minimal| G[quiz_template_minimal.tex.jinja<br/>- Black & white<br/>- Clean typography<br/>- No decorations<br/>- 3-4 pages]
    
    D --> H[Professional Use]
    E --> I[Space-Efficient Printing]
    F --> J[Academic Assessments]
    G --> K[Minimal Distraction]
```