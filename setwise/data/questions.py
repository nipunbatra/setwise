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
            r"Variance only matters in unsupervised learning",
            r"Bias and variance can both be minimized simultaneously without any tradeoff"
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
        "options": [r"0.85", r"0.857", r"0.90", r"0.875", r"0.95", r"0.825"],
        "answer": r"0.857",
        "marks": 3
    },
    {
        "question": r"""In a decision tree, which impurity measure is most commonly used for classification tasks?""",
        "options": [
            r"Mean Squared Error (MSE)",
            r"Gini Impurity", 
            r"Mean Absolute Error (MAE)",
            r"R-squared",
            r"Cross-entropy",
            r"Pearson correlation"
        ],
        "answer": r"Gini Impurity",
        "marks": 2
    },
    {
        "question": r"""Which regularization technique adds a penalty term proportional to the sum of absolute values of parameters?""",
        "options": [
            r"L2 Regularization (Ridge)", 
            r"L1 Regularization (Lasso)", 
            r"Elastic Net", 
            r"Dropout",
            r"Batch Normalization",
            r"Early Stopping"
        ],
        "answer": r"L1 Regularization (Lasso)",
        "marks": 2
    },
    {
        "question": r"""In Support Vector Machines, what happens when the regularization parameter C is very large?""",
        "options": [
            r"The model becomes more regularized and may underfit",
            r"The model focuses on minimizing training error and may overfit",
            r"The kernel function becomes linear",
            r"The support vectors are ignored",
            r"The margin becomes infinite",
            r"All data points become support vectors"
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
            r"It requires k different algorithms",
            r"The value of k should always be equal to the sample size",
            r"It can only be used with linear models"
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
            r"The computational complexity of the algorithm",
            r"The number of false positives in the dataset",
            r"The optimal threshold for classification"
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
        "options": [r"12", r"13", r"15", r"16", r"18", r"20"],
        "answer": r"16",
        "marks": 4
    },
    {
        "question": r"""Which activation function is most commonly used in hidden layers of modern deep neural networks?""",
        "options": [
            r"Sigmoid",
            r"Tanh", 
            r"ReLU",
            r"Linear",
            r"Step function",
            r"Softmax"
        ],
        "answer": r"ReLU",
        "marks": 2
    },
    {
        "question": r"""What is the main advantage of using Random Forest over a single Decision Tree?""",
        "options": [
            r"Faster training time",
            r"Better interpretability",
            r"Reduced overfitting through ensemble averaging",
            r"Lower memory usage",
            r"Better performance on linear relationships",
            r"Simpler hyperparameter tuning"
        ],
        "answer": r"Reduced overfitting through ensemble averaging",
        "marks": 2
    },
    {
        "question": r"""In logistic regression, what does the sigmoid function map the linear combination of features to?""",
        "options": [
            r"Any real number",
            r"Values between 0 and 1",
            r"Values between -1 and 1", 
            r"Only integer values",
            r"Values between -∞ and +∞",
            r"Only binary values (0 or 1)"
        ],
        "answer": r"Values between 0 and 1",
        "marks": 2
    },
    {
        "question": r"""Which of the following best describes the purpose of feature scaling in machine learning?""",
        "options": [
            r"To reduce the number of features",
            r"To ensure all features contribute equally to distance calculations",
            r"To increase model complexity",
            r"To add more training data",
            r"To eliminate the need for cross-validation",
            r"To convert categorical features to numerical"
        ],
        "answer": r"To ensure all features contribute equally to distance calculations",
        "marks": 2
    },
    {
        "question": r"""What is the primary difference between bagging and boosting ensemble methods?""",
        "options": [
            r"Bagging uses different algorithms, boosting uses the same algorithm",
            r"Bagging trains models in parallel, boosting trains models sequentially",
            r"Bagging is only for regression, boosting is only for classification",
            r"Bagging uses all features, boosting uses feature subsets",
            r"Bagging requires more computational resources than boosting",
            r"Bagging and boosting are exactly the same technique"
        ],
        "answer": r"Bagging trains models in parallel, boosting trains models sequentially",
        "marks": 3
    },
    {
        "question": r"""In k-Nearest Neighbors (k-NN), what happens when k is set to 1?""",
        "options": [
            r"The model becomes more biased",
            r"The model may overfit to training data",
            r"The model always underfits",
            r"The algorithm becomes faster",
            r"All predictions become the same",
            r"The model cannot make any predictions"
        ],
        "answer": r"The model may overfit to training data",
        "marks": 2
    },
    {
        "question": r"""Which metric is most appropriate for evaluating a model on an imbalanced classification dataset?""",
        "options": [
            r"Accuracy",
            r"Mean Squared Error",
            r"F1-Score", 
            r"R-squared",
            r"Mean Absolute Error",
            r"Pearson Correlation"
        ],
        "answer": r"F1-Score",
        "marks": 3
    },
    {
        "question": r"""What is the kernel trick in Support Vector Machines?""",
        "options": [
            r"A method to reduce training time",
            r"A way to implicitly map data to higher dimensions without explicit computation",
            r"A technique to reduce the number of support vectors",
            r"A method to automatically select the best features",
            r"A way to handle missing values in the dataset",
            r"A technique to balance imbalanced datasets"
        ],
        "answer": r"A way to implicitly map data to higher dimensions without explicit computation",
        "marks": 3
    },
    {
        "question": r"""Which of the following is NOT a hyperparameter in a Random Forest model?""",
        "options": [
            r"Number of trees in the forest",
            r"Maximum depth of each tree",
            r"Number of features considered at each split",
            r"The trained weights of the model",
            r"Minimum samples required to split a node",
            r"Bootstrap sample size"
        ],
        "answer": r"The trained weights of the model",
        "marks": 2
    },
    {
        "question": r"""What is the main purpose of using validation curves in machine learning?""",
        "options": [
            r"To visualize the training data distribution",
            r"To select optimal hyperparameters by plotting performance vs hyperparameter values",
            r"To compare different algorithms",
            r"To detect outliers in the dataset",
            r"To visualize feature importance",
            r"To show the model architecture"
        ],
        "answer": r"To select optimal hyperparameters by plotting performance vs hyperparameter values",
        "marks": 3
    },
    {
        "question": r"""In gradient descent optimization, what does the learning rate control?""",
        "options": [
            r"The number of iterations to run",
            r"The size of steps taken towards the minimum",
            r"The number of features to use",
            r"The complexity of the model",
            r"The size of the training dataset",
            r"The number of layers in a neural network"
        ],
        "answer": r"The size of steps taken towards the minimum",
        "marks": 2
    },
    {
        "question": r"""Which statement about overfitting is most accurate?""",
        "options": [
            r"Overfitting only occurs with neural networks",
            r"A model that overfits will always have high training accuracy and low validation accuracy",
            r"Overfitting can be completely eliminated by using more data",
            r"Overfitted models perform well on both training and test data",
            r"Overfitting is beneficial for model performance",
            r"Simple models never overfit"
        ],
        "answer": r"A model that overfits will always have high training accuracy and low validation accuracy",
        "marks": 2
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
    {
        "template": r"""A k-Nearest Neighbors classifier is trained on a dataset with {{ n_samples }} samples and {{ n_features }} features.

\textbf{a)} What is the time complexity for predicting a single test sample when k = {{ k_value }}? \textbf{[2 marks]}

\textbf{b)} If we use Euclidean distance and the training data has features with very different scales (e.g., age in years vs income in dollars), what preprocessing step should be applied and why? \textbf{[3 marks]}

\textbf{c)} How would you choose the optimal value of k for this dataset? Describe the method and potential issues. \textbf{[3 marks]}""",
        "variables": [
            {
                "n_samples": 1000, "n_features": 20, "k_value": 5,
                "answer": "a) O(n*d) = O(20000) for distance calculation + O(n log k) for finding k nearest, b) Feature scaling/normalization to prevent features with larger scales from dominating, c) Cross-validation; issues: bias-variance tradeoff, computational cost"
            },
            {
                "n_samples": 5000, "n_features": 50, "k_value": 3,
                "answer": "a) O(n*d) = O(250000) for distance calculation + O(n log k) for finding k nearest, b) Standardization or min-max scaling to ensure equal contribution, c) Grid search with CV; issues: curse of dimensionality, choice of distance metric"
            }
        ],
        "marks": 8
    },
    {
        "template": r"""A neural network is being trained using backpropagation with the following parameters:
- Learning rate: {{ lr }}
- Batch size: {{ batch_size }}
- Training samples: {{ train_samples }}

\textbf{a)} How many weight updates will occur in one epoch? \textbf{[2 marks]}

\textbf{b)} If the loss decreases very slowly, suggest three specific modifications to improve convergence. \textbf{[3 marks]}

\textbf{c)} Explain the vanishing gradient problem and how it affects deep networks. \textbf{[3 marks]}""",
        "variables": [
            {
                "lr": 0.01, "batch_size": 32, "train_samples": 1000,
                "answer": "a) 1000/32 = 31.25 ≈ 31 updates, b) Increase learning rate, use adaptive optimizers (Adam), better initialization, c) Gradients become exponentially small in early layers, preventing learning"
            },
            {
                "lr": 0.001, "batch_size": 64, "train_samples": 2000,
                "answer": "a) 2000/64 = 31.25 ≈ 31 updates, b) Learning rate scheduling, batch normalization, different activation functions, c) Product of small derivatives causes gradients to vanish, especially in deep networks"
            }
        ],
        "marks": 8
    },
    {
        "template": r"""Consider an ensemble method combining {{ n_models }} different models with the following individual accuracies:
Model 1: {{ acc1 }}\%, Model 2: {{ acc2 }}\%, Model 3: {{ acc3 }}\%

\textbf{a)} If we use simple majority voting, what conditions must be met for the ensemble to outperform the individual models? \textbf{[3 marks]}

\textbf{b)} Calculate the expected ensemble accuracy assuming the models make independent errors and using majority voting. \textbf{[4 marks]}

\textbf{c)} Compare the advantages and disadvantages of majority voting vs. weighted voting in ensemble methods. \textbf{[3 marks]}""",
        "variables": [
            {
                "n_models": 3, "acc1": 85, "acc2": 80, "acc3": 82,
                "answer": "a) Models should be better than random (>50%) and make different errors, b) P(ensemble correct) ≈ 87.4% (detailed calculation needed), c) Majority: simple, robust; Weighted: better performance but needs weight optimization"
            },
            {
                "n_models": 3, "acc1": 78, "acc2": 83, "acc3": 79,
                "answer": "a) Individual accuracy > 50% and diversity in predictions, b) Expected accuracy ≈ 84.2% with independence assumption, c) Majority: equal importance, less overfitting; Weighted: leverages best models but complex tuning"
            }
        ],
        "marks": 10
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
    },
    {
        "question": r"""Analyze the model selection process in machine learning:

\textbf{a)} Explain the difference between validation error and test error. Why do we need both? \textbf{[3 marks]}

\textbf{b)} Describe the data leakage problem and provide two specific examples of how it can occur. \textbf{[4 marks]}

\textbf{c)} What is the purpose of nested cross-validation and when should it be used? \textbf{[3 marks]}""",
        "answer": "a) Validation: model selection, Test: final evaluation. Need both to avoid overoptimistic estimates. b) Information from test set influencing training. Examples: scaling before split, temporal leakage. c) Unbiased model selection when tuning hyperparameters with limited data",
        "marks": 10
    },
    {
        "question": r"""Design a complete machine learning pipeline for a real-world classification problem:

You are tasked with building a system to predict customer churn for a telecommunications company.

\textbf{a)} Describe the data preprocessing steps you would implement, including handling missing values, categorical variables, and feature scaling. \textbf{[4 marks]}

\textbf{b)} Explain your approach to feature selection and engineering for this problem. \textbf{[3 marks]}

\textbf{c)} Which evaluation metrics would you use and why? Consider the business impact of false positives vs false negatives. \textbf{[3 marks]}

\textbf{d)} How would you handle class imbalance if 95\% of customers don't churn? \textbf{[3 marks]}""",
        "answer": "a) Handle missing: imputation/removal, encode categoricals: one-hot/label encoding, scale numerical features. b) Domain features: tenure, usage patterns; RFE, correlation analysis. c) Precision/Recall, F1, AUC - FN costlier (losing customers). d) SMOTE, cost-sensitive learning, threshold tuning, stratified sampling",
        "marks": 13
    },
    {
        "question": r"""Evaluate the impact of different optimization algorithms on neural network training:

\textbf{a)} Compare SGD, Adam, and RMSprop optimizers in terms of convergence speed, memory requirements, and robustness to hyperparameters. \textbf{[4 marks]}

\textbf{b)} Explain the concept of learning rate scheduling and describe two specific scheduling strategies. \textbf{[3 marks]}

\textbf{c)} What is the Adam optimizer's bias correction mechanism and why is it necessary? \textbf{[3 marks]}""",
        "answer": "a) SGD: slow but stable, low memory; Adam: fast, adaptive, higher memory; RMSprop: good for RNNs, adaptive. b) Decay over time, reduce on plateau. Examples: exponential decay, step decay. c) Corrects initialization bias in momentum estimates using bias correction terms",
        "marks": 10
    },
    {
        "question": r"""Analyze dimensionality reduction techniques and their applications:

\textbf{a)} Compare PCA and t-SNE in terms of their objectives, computational complexity, and typical use cases. \textbf{[4 marks]}

\textbf{b)} Explain the curse of dimensionality and how it affects k-NN and SVM algorithms differently. \textbf{[3 marks]}

\textbf{c)} When would you choose feature selection over feature extraction methods? Provide specific scenarios. \textbf{[3 marks]}""",
        "answer": "a) PCA: linear, global structure, O(d³); t-SNE: non-linear, local structure, O(n²). b) k-NN: distance becomes meaningless; SVM: kernel trick helps but computational cost increases. c) Feature selection: interpretability needed, regulatory requirements, small datasets",
        "marks": 10
    }
]