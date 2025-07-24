"""
Machine Learning Supervised Learning Questions for Setwise quiz generator.
Contains MCQ and subjective questions with LaTeX support, marks, tables, and figures.
"""

# Multiple Choice Questions - Machine Learning Supervised Learning
mcq = [
    {
        "question": r"""Which of the following best describes the bias-variance tradeoff in machine learning?""",
        "options": [
            r"High bias models always perform better than high variance models",
            r"Bias and variance are independent and don't affect each other", 
            r"Reducing bias typically increases variance, and vice versa",
            r"Variance only matters in unsupervised learning"
        ],
        "answer": r"Reducing bias typically increases variance, and vice versa",
        "marks": 2
    },
    {
        "question": r"""Given the confusion matrix below for a binary classification problem:

\begin{center}
\begin{tabular}{|c|c|c|}
\hline
 & \textbf{Predicted 0} & \textbf{Predicted 1} \\
\hline
\textbf{Actual 0} & 85 & 15 \\
\hline
\textbf{Actual 1} & 10 & 90 \\
\hline
\end{tabular}
\end{center}

What is the precision of the classifier?""",
        "options": [r"0.85", r"0.857", r"0.90", r"0.875"],
        "answer": r"0.857",
        "marks": 3
    },
    {
        "question": r"""In a decision tree, which impurity measure is most commonly used for classification tasks?""",
        "options": [
            r"Mean Squared Error (MSE)",
            r"Gini Impurity", 
            r"Mean Absolute Error (MAE)",
            r"R-squared"
        ],
        "answer": r"Gini Impurity",
        "marks": 2
    },
    {
        "question": r"""Which regularization technique adds a penalty term proportional to the sum of absolute values of parameters?""",
        "options": [r"L2 Regularization (Ridge)", r"L1 Regularization (Lasso)", r"Elastic Net", r"Dropout"],
        "answer": r"L1 Regularization (Lasso)",
        "marks": 2
    },
    {
        "question": r"""In Support Vector Machines, what happens when the regularization parameter C is very large?""",
        "options": [
            r"The model becomes more regularized and may underfit",
            r"The model focuses on minimizing training error and may overfit",
            r"The kernel function becomes linear",
            r"The support vectors are ignored"
        ],
        "answer": r"The model focuses on minimizing training error and may overfit",
        "marks": 3
    },
    {
        "question": r"""Which of the following is true about k-fold cross-validation?""",
        "options": [
            r"It uses k different datasets for training",
            r"It splits data into k parts, trains on k-1 parts, tests on 1 part, repeats k times",
            r"It only works when k equals the number of features",
            r"It requires k different algorithms"
        ],
        "answer": r"It splits data into k parts, trains on k-1 parts, tests on 1 part, repeats k times",
        "marks": 2
    },
    {
        "question": r"""Looking at the ROC curve below:

\begin{center}
\includegraphics[width=0.6\textwidth]{figures/roc_curve.pdf}
\end{center}

What does the area under the curve (AUC) represent?""",
        "options": [
            r"The probability that the classifier ranks a random positive instance higher than a random negative instance",
            r"The total number of correct predictions",
            r"The difference between true positive rate and false positive rate",
            r"The computational complexity of the algorithm"
        ],  
        "answer": r"The probability that the classifier ranks a random positive instance higher than a random negative instance",
        "marks": 3
    },
    {
        "question": r"""In the neural network architecture shown:

\begin{center}
\input{figures/neural_network.tikz}
\end{center}

How many parameters (weights and biases) does this network have?""",
        "options": [r"12", r"13", r"15", r"16"],
        "answer": r"16",
        "marks": 4
    }
]

# Subjective Questions with templated variants - Machine Learning
subjective = [
    {
        "template": r"""Consider the following dataset for linear regression:

\begin{center}
\begin{tabular}{|c|c|c|c|}
\hline
\textbf{Sample} & \textbf{Feature 1} & \textbf{Feature 2} & \textbf{Target} \\
\hline
1 & {{ x1_1 }} & {{ x2_1 }} & {{ y1 }} \\
\hline
2 & {{ x1_2 }} & {{ x2_2 }} & {{ y2 }} \\
\hline
3 & {{ x1_3 }} & {{ x2_3 }} & {{ y3 }} \\
\hline
4 & {{ x1_4 }} & {{ x2_4 }} & {{ y4 }} \\
\hline
\end{tabular}
\end{center}

\textbf{a)} Calculate the mean squared error (MSE) if the model predicts $\hat{y} = {{ pred1 }}, {{ pred2 }}, {{ pred3 }}, {{ pred4 }}$ respectively. \textbf{[3 marks]}

\textbf{b)} If we use L2 regularization with $\lambda = {{ lambda_val }}$, write the complete loss function. \textbf{[2 marks]}""",
        "variables": [
            {
                "x1_1": 2, "x2_1": 1, "y1": 5, "x1_2": 4, "x2_2": 3, "y2": 11, 
                "x1_3": 1, "x2_3": 2, "y3": 4, "x1_4": 3, "x2_4": 4, "y4": 10,
                "pred1": 4.8, "pred2": 10.5, "pred3": 4.2, "pred4": 9.8,
                "lambda_val": 0.01,
                "answer": "a) MSE = 0.1425, b) Loss = MSE + 0.01 * Σ(wi²)"
            },
            {
                "x1_1": 1, "x2_1": 2, "y1": 6, "x1_2": 3, "x2_2": 1, "y2": 7, 
                "x1_3": 2, "x2_3": 3, "y3": 9, "x1_4": 4, "x2_4": 2, "y4": 10,
                "pred1": 5.9, "pred2": 7.1, "pred3": 8.8, "pred4": 9.9,
                "lambda_val": 0.05,
                "answer": "a) MSE = 0.0175, b) Loss = MSE + 0.05 * Σ(wi²)"
            }
        ],
        "marks": 5
    },
    {
        "template": r"""Analyze the decision tree structure below:

\begin{center}
\input{figures/decision_tree.tikz}
\end{center}

\textbf{a)} What is the maximum depth of this tree? \textbf{[1 mark]}

\textbf{b)} Calculate the Gini impurity for a node with class distribution: Class A: {{ class_a }} samples, Class B: {{ class_b }} samples, Class C: {{ class_c }} samples. \textbf{[3 marks]}

\textbf{c)} Explain why pruning might be beneficial for this tree. \textbf{[2 marks]}""",
        "variables": [
            {
                "class_a": 40, "class_b": 30, "class_c": 10,
                "answer": "a) Depth = 2, b) Gini = 1 - (0.5² + 0.375² + 0.125²) = 0.609, c) Reduce overfitting and improve generalization"
            },
            {
                "class_a": 50, "class_b": 20, "class_c": 30,
                "answer": "a) Depth = 2, b) Gini = 1 - (0.5² + 0.2² + 0.3²) = 0.62, c) Reduce overfitting and improve generalization"
            }
        ],
        "marks": 6
    },
    {
        "template": r"""Given the learning curves shown below:

\begin{center}
\includegraphics[width=0.8\textwidth]{figures/learning_curves.pdf}
\end{center}

\textbf{a)} Identify whether the model is suffering from high bias or high variance. Justify your answer. \textbf{[3 marks]}

\textbf{b)} Suggest two specific techniques to improve the model performance. \textbf{[2 marks]}

\textbf{c)} If the training accuracy is {{ train_acc }}\% and validation accuracy is {{ val_acc }}\%, calculate the overfitting gap. \textbf{[1 mark]}""",
        "variables": [
            {
                "train_acc": 95, "val_acc": 78,
                "answer": "a) High variance (large gap between training and validation), b) Regularization, more training data, c) Gap = 17%"
            },
            {
                "train_acc": 82, "val_acc": 79,
                "answer": "a) High bias (both curves plateau at low values), b) More complex model, feature engineering, c) Gap = 3%"
            }
        ],
        "marks": 6
    },
    {
        "template": r"""Consider the SVM with margin illustration:

\begin{center}
\input{figures/svm_margin.tikz}
\end{center}

\textbf{a)} Explain the concept of support vectors and their role in SVM. \textbf{[3 marks]}

\textbf{b)} If we have {{ n_pos }} positive samples and {{ n_neg }} negative samples, and {{ n_sv }} of them are support vectors, what percentage of the data points are support vectors? \textbf{[2 marks]}

\textbf{c)} Compare the computational complexity of SVM prediction with and without kernel tricks. \textbf{[2 marks]}""",
        "variables": [
            {
                "n_pos": 120, "n_neg": 80, "n_sv": 15,
                "answer": "a) Support vectors define the decision boundary and margin; only they matter for classification, b) 15/200 = 7.5%, c) Linear: O(d), Kernel: O(number of SVs)"
            },
            {
                "n_pos": 150, "n_neg": 100, "n_sv": 20,
                "answer": "a) Support vectors define the decision boundary and margin; only they matter for classification, b) 20/250 = 8%, c) Linear: O(d), Kernel: O(number of SVs)"
            }
        ],
        "marks": 7
    },
    {
        "template": r"""Examine the overfitting comparison plots:

\begin{center}
\includegraphics[width=0.9\textwidth]{figures/overfitting_comparison.pdf}
\end{center}

\textbf{a)} Identify which model suffers from underfitting, good fit, and overfitting. Justify each choice. \textbf{[4 marks]}

\textbf{b)} If you had to choose a regularization parameter $\lambda$ for ridge regression, would you choose a high or low value to move from the overfitted model to the good fit model? Explain. \textbf{[3 marks]}""",
        "variables": [
            {"answer": "a) Left: underfitting (too simple), Middle: good fit (captures pattern without noise), Right: overfitting (memorizes noise), b) High λ to increase bias and reduce variance"},
            {"answer": "a) Left: underfitting (linear for non-linear data), Middle: appropriate complexity, Right: overfitting (too flexible), b) Higher λ value to penalize complex terms"}
        ],
        "marks": 7
    },
    # Non-templated subjective questions
    {
        "question": r"""Compare and contrast the following three supervised learning algorithms in terms of their assumptions, strengths, and weaknesses:

\begin{center}
\begin{tabular}{|p{3cm}|p{3cm}|p{3cm}|p{3cm}|}
\hline
\textbf{Algorithm} & \textbf{Key Assumptions} & \textbf{Strengths} & \textbf{Weaknesses} \\
\hline
Linear Regression & & & \\
\hline
Decision Trees & & & \\
\hline
k-NN & & & \\
\hline
\end{tabular}
\end{center}

Fill in the table above and provide a brief explanation for each entry. \textbf{[9 marks]}""",
        "answer": "Linear: Linear relationship, normality | Interpretable, fast | Limited to linear patterns. Trees: No assumptions | Interpretable, handles non-linear | Prone to overfitting. k-NN: Locality assumption | Simple, non-parametric | Computationally expensive, curse of dimensionality",
        "marks": 9
    },
    {
        "question": r"""Derive the gradient descent update rule for logistic regression. Start from the logistic loss function:

$$J(\theta) = -\frac{1}{m} \sum_{i=1}^{m} [y^{(i)} \log(h_\theta(x^{(i)})) + (1-y^{(i)}) \log(1-h_\theta(x^{(i)}))]$$

where $h_\theta(x) = \frac{1}{1 + e^{-\theta^T x}}$

Show all steps clearly including the partial derivatives. \textbf{[8 marks]}""",
        "answer": "∂J/∂θ = (1/m) Σ (h_θ(x⁽ⁱ⁾) - y⁽ⁱ⁾) x⁽ⁱ⁾. Update rule: θ := θ - α(1/m) Σ (h_θ(x⁽ⁱ⁾) - y⁽ⁱ⁾) x⁽ⁱ⁾",
        "marks": 8
    },
    {
        "question": r"""Explain the ensemble methods Random Forest and AdaBoost:

\textbf{a)} Describe how Random Forest reduces overfitting compared to a single decision tree. \textbf{[3 marks]}

\textbf{b)} Explain the boosting principle in AdaBoost and how it differs from bagging. \textbf{[4 marks]}

\textbf{c)} Under what circumstances would you prefer Random Forest over AdaBoost and vice versa? \textbf{[3 marks]}""",
        "answer": "a) Bootstrap sampling + feature randomness reduces variance. b) AdaBoost: sequential, focuses on mistakes; Bagging: parallel, reduces variance. c) RF: noisy data, parallel processing; AdaBoost: clean data, need high accuracy",
        "marks": 10
    }
]