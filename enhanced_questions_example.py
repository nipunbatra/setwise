#!/usr/bin/env python3
"""
Enhanced Setwise Questions Example - Demonstrating All New Features

This file shows all the improvements:
1. Easy quiz metadata specification
2. Templated MCQ questions (now supported!)  
3. Multi-part subjective questions
4. Mix of regular and templated questions
5. Python-only format (.py)
"""

# ===============================================================================
# QUIZ METADATA - Easy way to specify quiz information
# ===============================================================================
quiz_metadata = {
    "title": "Machine Learning Fundamentals Quiz",
    "subject": "Computer Science", 
    "course_code": "CS 4780",
    "instructor": "Prof. Smith",
    "semester": "Fall 2024",
    "duration": "90 minutes",
    "total_marks": 50,
    "instructions": [
        "Answer all questions clearly and concisely",
        "Show your work for partial credit", 
        "Use proper mathematical notation where applicable"
    ],
    "exam_date": "December 15, 2024",
    "institution": "Cornell University"
}

# ===============================================================================
# MCQ QUESTIONS - Now supports both regular AND templated questions!
# ===============================================================================
mcq = [
    # Regular MCQ question
    {
        "question": r"Which of the following best describes the bias-variance tradeoff in machine learning?",
        "options": [
            r"High bias models always perform better than high variance models",
            r"Bias and variance are independent and don't affect each other", 
            r"Reducing bias typically increases variance, and vice versa",
            r"Variance only matters in unsupervised learning"
        ],
        "answer": r"Reducing bias typically increases variance, and vice versa",
        "marks": 2
    },
    
    # TEMPLATED MCQ question - NEW FEATURE!
    {
        "template": r"In k-fold cross-validation with k={{ k_value }}, how many times is the model trained and validated?",
        "options": [
            r"Trained {{ k_value-1 }} times, validated {{ k_value }} times",
            r"Trained {{ k_value }} times, validated {{ k_value }} times", 
            r"Trained {{ k_value }} times, validated 1 time",
            r"Trained 1 time, validated {{ k_value }} times"
        ],
        "answer": r"Trained {{ k_value }} times, validated {{ k_value }} times",
        "variables": [
            {"k_value": 5},
            {"k_value": 10},
            {"k_value": 3}
        ],
        "marks": 2
    },
    
    # Another templated MCQ with calculations
    {
        "template": r"A dataset has {{ n_samples }} samples and {{ n_features }} features. Using {{ train_ratio }}% for training, how many samples are used for training?",
        "options": [
            r"{{ n_samples * train_ratio // 100 }} samples",
            r"{{ n_samples * (100-train_ratio) // 100 }} samples", 
            r"{{ n_features * train_ratio // 100 }} samples",
            r"{{ n_samples }} samples"
        ],
        "answer": r"{{ n_samples * train_ratio // 100 }} samples",
        "variables": [
            {"n_samples": 1000, "train_ratio": 80},
            {"n_samples": 500, "train_ratio": 70},
            {"n_samples": 1500, "train_ratio": 75}
        ],
        "marks": 3
    }
]

# ===============================================================================
# SUBJECTIVE QUESTIONS - Regular, templated, and multi-part
# ===============================================================================
subjective = [
    # Regular subjective question
    {
        "question": r"Compare and contrast supervised and unsupervised learning approaches. Provide examples of algorithms and use cases for each.",
        "answer": r"Supervised learning uses labeled data to learn mappings (e.g., classification, regression). Examples: SVM, Random Forest. Unsupervised learning finds patterns in unlabeled data (e.g., clustering, dimensionality reduction). Examples: K-means, PCA.",
        "marks": 8
    },
    
    # Templated subjective question
    {
        "template": r"""Consider a neural network with {{ n_layers }} hidden layers, each with {{ neurons_per_layer }} neurons.

Calculate the total number of parameters if:
- Input dimension: {{ input_dim }}
- Output dimension: {{ output_dim }}
- Each layer is fully connected
- Bias terms are included

Show your calculation step by step.""",
        "variables": [
            {
                "n_layers": 2, "neurons_per_layer": 64, "input_dim": 784, "output_dim": 10,
                "answer": "Layer 1: (784 × 64) + 64 = 50,240\nLayer 2: (64 × 64) + 64 = 4,160\nOutput: (64 × 10) + 10 = 650\nTotal: 55,050 parameters"
            },
            {
                "n_layers": 3, "neurons_per_layer": 128, "input_dim": 1000, "output_dim": 5,
                "answer": "Layer 1: (1000 × 128) + 128 = 128,128\nLayer 2: (128 × 128) + 128 = 16,512\nLayer 3: (128 × 128) + 128 = 16,512\nOutput: (128 × 5) + 5 = 645\nTotal: 161,797 parameters"
            }
        ],
        "marks": 10
    },
    
    # MULTI-PART subjective question - Enhanced feature!
    {
        "question": r"Analyze the performance of a logistic regression model:",
        "parts": [
            {
                "question": r"Given the training accuracy is 95% and validation accuracy is 60%, what problem does this indicate?",
                "answer": r"This indicates overfitting. The large gap between training (95%) and validation (60%) accuracy shows the model memorized the training data rather than learning generalizable patterns.",
                "marks": 3
            },
            {
                "question": r"Suggest three specific techniques to address this problem and explain how each helps.",
                "answer": r"1) Regularization (L1/L2): Penalizes large weights to reduce model complexity. 2) Cross-validation: Better estimates generalization performance. 3) Feature selection: Removes irrelevant features that cause overfitting.",
                "marks": 6
            },
            {
                "question": r"If the training accuracy becomes 85% and validation accuracy becomes 82% after applying your suggestions, evaluate this outcome.",
                "answer": r"This is a significant improvement. The small gap (3%) between training and validation accuracy indicates good generalization. The slight decrease in training accuracy is worthwhile for better validation performance.",
                "marks": 4
            }
        ],
        "marks": 13  # Total marks for all parts
    },
    
    # Templated multi-part question
    {
        "template": r"Consider a dataset with the following characteristics:",
        "parts": [
            {
                "question": r"The dataset has {{ n_samples }} samples with {{ pos_samples }} positive and {{ neg_samples }} negative examples. Calculate the class imbalance ratio.",
                "answer": r"Imbalance ratio = {{ pos_samples }}/{{ neg_samples }} = {{ pos_samples/neg_samples }:.1f}. This shows {{ 'severe' if pos_samples/neg_samples < 0.5 else 'moderate' }} class imbalance.",
                "marks": 3
            },
            {
                "question": r"Suggest appropriate evaluation metrics for this imbalanced dataset and justify your choices.",
                "answer": r"Use precision, recall, F1-score, and AUC-ROC instead of accuracy. Accuracy can be misleading with imbalanced data. F1-score balances precision/recall. AUC-ROC is threshold-independent.",
                "marks": 4
            }
        ],
        "variables": [
            {"n_samples": 1000, "pos_samples": 200, "neg_samples": 800},
            {"n_samples": 500, "pos_samples": 50, "neg_samples": 450}
        ],
        "marks": 7
    }
]