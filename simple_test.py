#!/usr/bin/env python3
"""
Simple test for new setwise features
"""

# Quiz metadata
quiz_metadata = {
    "title": "Test Quiz",
    "subject": "Mathematics", 
    "duration": "60 minutes",
    "total_marks": 20
}

# MCQ with templated question
mcq = [
    {
        "question": r"What is 2 + 2?",
        "options": [r"3", r"4", r"5", r"6"],
        "answer": r"4",
        "marks": 2
    },
    {
        "template": r"What is {{ a }} + {{ b }}?",
        "options": [r"{{ a + b - 1 }}", r"{{ a + b }}", r"{{ a + b + 1 }}", r"{{ a * b }}"],
        "answer": r"{{ a + b }}",
        "variables": [
            {"a": 3, "b": 4},
            {"a": 5, "b": 7},
            {"a": 8, "b": 2}
        ],
        "marks": 2
    }
]

# Subjective questions
subjective = [
    {
        "question": r"Explain addition.",
        "answer": r"Addition combines numbers to get their sum.",
        "marks": 5
    },
    {
        "template": r"Calculate {{ x }} times {{ y }}.",
        "variables": [
            {"x": 6, "y": 7, "answer": "42"},
            {"x": 8, "y": 9, "answer": "72"}
        ],
        "marks": 3
    }
]