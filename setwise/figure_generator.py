#!/usr/bin/env python3
"""
Figure generation script for Setwise ML quiz generator.
Creates TikZ and matplotlib figures for machine learning questions.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

def create_figures_directory():
    """Ensure figures directory exists."""
    os.makedirs('figures', exist_ok=True)

def generate_tikz_figures():
    """Generate TikZ code files for LaTeX figures."""
    
    # Decision tree TikZ
    decision_tree_tikz = r"""
\begin{tikzpicture}[
  level distance=2cm,
  level 1/.style={sibling distance=4cm},
  level 2/.style={sibling distance=2cm},
  every node/.style={circle, draw, minimum size=1cm}
]
\node {$x_1 \leq 5$}
  child { node {$x_2 \leq 3$}
    child { node[rectangle] {Class A} }
    child { node[rectangle] {Class B} }
  }
  child { node {$x_2 \leq 7$}
    child { node[rectangle] {Class B} }
    child { node[rectangle] {Class C} }
  };
\end{tikzpicture}
"""
    
    # Neural network TikZ
    neural_network_tikz = r"""
\begin{tikzpicture}[
  node distance=2cm,
  neuron/.style={circle, draw, minimum size=0.8cm},
  input/.style={neuron, fill=blue!20},
  hidden/.style={neuron, fill=green!20},
  output/.style={neuron, fill=red!20}
]

% Input layer
\node[input] (i1) at (0,2) {$x_1$};
\node[input] (i2) at (0,0) {$x_2$};
\node[input] (i3) at (0,-2) {$x_3$};

% Hidden layer
\node[hidden] (h1) at (3,1.5) {$h_1$};
\node[hidden] (h2) at (3,0) {$h_2$};
\node[hidden] (h3) at (3,-1.5) {$h_3$};

% Output layer
\node[output] (o1) at (6,0) {$y$};

% Connections
\foreach \i in {1,2,3}
  \foreach \h in {1,2,3}
    \draw (i\i) -- (h\h);

\foreach \h in {1,2,3}
  \draw (h\h) -- (o1);

% Labels
\node at (0,-3) {Input Layer};
\node at (3,-3) {Hidden Layer};
\node at (6,-1.5) {Output Layer};

\end{tikzpicture}
"""
    
    # SVM margin TikZ
    svm_margin_tikz = r"""
\begin{tikzpicture}[scale=0.8]
% Draw axes
\draw[->] (-1,0) -- (6,0) node[right] {$x_1$};
\draw[->] (0,-1) -- (0,5) node[above] {$x_2$};

% Draw support vectors
\fill[red] (1,1) circle (3pt) node[below left] {SV};
\fill[red] (2,0.5) circle (3pt) node[below] {SV};
\fill[blue] (3,3) circle (3pt) node[above] {SV};
\fill[blue] (4,3.5) circle (3pt) node[above right] {SV};

% Draw other points
\fill[red] (0.5,2) circle (2pt);
\fill[red] (1.5,2.5) circle (2pt);
\fill[blue] (4.5,2) circle (2pt);
\fill[blue] (5,1) circle (2pt);

% Draw decision boundary and margins
\draw[thick] (0.5,3.5) -- (5,0.5) node[right] {Decision Boundary};
\draw[dashed] (0,4) -- (4.5,0) node[right] {Margin};
\draw[dashed] (1,4) -- (5.5,1) node[right] {Margin};

% Add margin width indicator
\draw[<->] (2.5,2.75) -- (3.25,2.25) node[midway,above] {Margin Width};

\end{tikzpicture}
"""

    # Write TikZ files
    tikz_figures = {
        'decision_tree.tikz': decision_tree_tikz,
        'neural_network.tikz': neural_network_tikz,
        'svm_margin.tikz': svm_margin_tikz
    }
    
    for filename, content in tikz_figures.items():
        with open(f'figures/{filename}', 'w') as f:
            f.write(content)
    
    print(f"Generated {len(tikz_figures)} TikZ figures")

def generate_matplotlib_figures():
    """Generate matplotlib figures as PDF files."""
    
    # 1. Linear Regression Plot
    plt.figure(figsize=(8, 6))
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    y_true = 2 * x + 1
    y_noisy = y_true + np.random.normal(0, 2, len(x))
    
    plt.scatter(x, y_noisy, alpha=0.6, label='Training Data')
    plt.plot(x, y_true, 'r-', linewidth=2, label='True Relationship')
    plt.plot(x, 2.1 * x + 0.8, 'g--', linewidth=2, label='Learned Model')
    plt.xlabel('Feature X', fontsize=12)
    plt.ylabel('Target Y', fontsize=12)
    plt.title('Linear Regression Example', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/linear_regression.pdf', bbox_inches='tight')
    plt.close()
    
    # 2. Classification Decision Boundary
    plt.figure(figsize=(8, 6))
    np.random.seed(42)
    
    # Generate data
    n_samples = 200
    X1 = np.random.multivariate_normal([2, 2], [[1, 0.5], [0.5, 1]], n_samples//2)
    X2 = np.random.multivariate_normal([5, 5], [[1, -0.3], [-0.3, 1]], n_samples//2)
    
    plt.scatter(X1[:, 0], X1[:, 1], c='red', alpha=0.6, label='Class A')
    plt.scatter(X2[:, 0], X2[:, 1], c='blue', alpha=0.6, label='Class B')
    
    # Draw decision boundary
    x_boundary = np.linspace(0, 7, 100)
    y_boundary = x_boundary + 0.5
    plt.plot(x_boundary, y_boundary, 'k-', linewidth=2, label='Decision Boundary')
    
    plt.xlabel('Feature 1', fontsize=12)
    plt.ylabel('Feature 2', fontsize=12)
    plt.title('Binary Classification with Decision Boundary', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/classification_boundary.pdf', bbox_inches='tight')
    plt.close()
    
    # 3. Overfitting vs Underfitting
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Generate polynomial data
    np.random.seed(42)
    x = np.linspace(0, 1, 20)
    y_true = 1.5 * x**2 + 0.3 * x + 0.1
    y_noisy = y_true + 0.1 * np.random.normal(0, 1, len(x))
    x_plot = np.linspace(0, 1, 100)
    
    # Underfitting (degree 1)
    p1 = np.polyfit(x, y_noisy, 1)
    y_pred1 = np.polyval(p1, x_plot)
    ax1.scatter(x, y_noisy, alpha=0.6)
    ax1.plot(x_plot, y_pred1, 'r-', linewidth=2)
    ax1.set_title('Underfitting (Degree 1)')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.grid(True, alpha=0.3)
    
    # Good fit (degree 2)
    p2 = np.polyfit(x, y_noisy, 2)
    y_pred2 = np.polyval(p2, x_plot)
    ax2.scatter(x, y_noisy, alpha=0.6)
    ax2.plot(x_plot, y_pred2, 'g-', linewidth=2)
    ax2.set_title('Good Fit (Degree 2)')
    ax2.set_xlabel('X')
    ax2.grid(True, alpha=0.3)
    
    # Overfitting (degree 10)
    p10 = np.polyfit(x, y_noisy, 10)
    y_pred10 = np.polyval(p10, x_plot)
    ax3.scatter(x, y_noisy, alpha=0.6)
    ax3.plot(x_plot, y_pred10, 'b-', linewidth=2)
    ax3.set_title('Overfitting (Degree 10)')
    ax3.set_xlabel('X')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/overfitting_comparison.pdf', bbox_inches='tight')
    plt.close()
    
    # 4. Learning Curves
    plt.figure(figsize=(10, 6))
    
    training_sizes = np.array([50, 100, 200, 400, 800, 1600])
    train_scores = np.array([0.95, 0.92, 0.88, 0.85, 0.83, 0.82])
    val_scores = np.array([0.75, 0.78, 0.82, 0.83, 0.84, 0.84])
    
    plt.plot(training_sizes, train_scores, 'o-', color='blue', label='Training Score')
    plt.plot(training_sizes, val_scores, 'o-', color='red', label='Validation Score')
    plt.xlabel('Training Set Size', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.title('Learning Curves: Training vs Validation Performance', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0.7, 1.0)
    plt.tight_layout()
    plt.savefig('figures/learning_curves.pdf', bbox_inches='tight')
    plt.close()
    
    # 5. ROC Curve
    plt.figure(figsize=(8, 6))
    
    # Generate sample ROC data
    fpr = np.array([0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0])
    tpr = np.array([0, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0])
    
    plt.plot(fpr, tpr, 'b-', linewidth=2, label='ROC Curve (AUC = 0.82)')
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Random Classifier')
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curve for Binary Classification', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/roc_curve.pdf', bbox_inches='tight')
    plt.close()
    
    print("Generated 5 matplotlib figures as PDF files")

def main():
    """Main function to generate all figures."""
    print("Generating figures for ML quiz...")
    
    create_figures_directory()
    generate_tikz_figures()
    generate_matplotlib_figures()
    
    print("All figures generated successfully!")
    print("TikZ files: figures/*.tikz")
    print("PDF files: figures/*.pdf")

if __name__ == "__main__":
    main()