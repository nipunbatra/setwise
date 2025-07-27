"""
Sample Mathematics Questions for Setwise Quiz Generator

Covers calculus, algebra, and statistics with proper LaTeX formatting.
Usage: setwise generate --questions-file mathematics_questions.py
"""

# Multiple Choice Questions - Mathematics
mcq = [
    {
        "question": r"What is the derivative of $f(x) = x^3 + 2x^2 - 5x + 1$?",
        "options": [
            r"$3x^2 + 4x - 5$",
            r"$3x^2 + 2x - 5$", 
            r"$x^3 + 4x - 5$",
            r"$3x^2 + 4x - 1$",
            r"$3x^2 + x - 5$"
        ],
        "answer": r"$3x^2 + 4x - 5$",
        "marks": 2
    },
    {
        "question": r"The integral $\int x^2 dx$ equals:",
        "options": [
            r"$\frac{x^3}{3} + C$",
            r"$x^3 + C$",
            r"$\frac{x^2}{2} + C$",
            r"$2x + C$",
            r"$\frac{2x^3}{3} + C$"
        ],
        "answer": r"$\frac{x^3}{3} + C$",
        "marks": 2
    },
    {
        "question": r"If $\log_2 8 = x$, then $x$ equals:",
        "options": [
            r"2",
            r"3",
            r"4", 
            r"8",
            r"16"
        ],
        "answer": r"3",
        "marks": 1
    },
    {
        "question": r"The determinant of the matrix $\begin{pmatrix} 2 & 1 \\ 3 & 4 \end{pmatrix}$ is:",
        "options": [
            r"5",
            r"8",
            r"11",
            r"14", 
            r"17"
        ],
        "answer": r"5",
        "marks": 2
    },
    {
        "question": r"What is the limit $\lim_{x \to 0} \frac{\sin x}{x}$?",
        "options": [
            r"0",
            r"1",
            r"$\infty$",
            r"Does not exist",
            r"$\frac{1}{2}$"
        ],
        "answer": r"1",
        "marks": 2
    }
]

# Subjective Questions - Mathematics
subjective = [
    {
        "question": r"""Find the critical points and classify them for the function $f(x) = x^3 - 6x^2 + 9x + 2$.

\textbf{a)} Find $f'(x)$ and set it equal to zero. \textbf{[3 marks]}

\textbf{b)} Solve for the critical points. \textbf{[2 marks]}

\textbf{c)} Use the second derivative test to classify each critical point. \textbf{[4 marks]}

\textbf{d)} Sketch the behavior of the function near these points. \textbf{[3 marks]}""",
        "answer": r"""a) $f'(x) = 3x^2 - 12x + 9 = 0$

b) $3(x^2 - 4x + 3) = 0$, so $x^2 - 4x + 3 = 0$
   $(x-1)(x-3) = 0$, giving $x = 1$ and $x = 3$

c) $f''(x) = 6x - 12$
   At $x = 1$: $f''(1) = -6 < 0$ → local maximum
   At $x = 3$: $f''(3) = 6 > 0$ → local minimum

d) Function increases to $(1,6)$, decreases to $(3,2)$, then increases""",
        "marks": 12
    },
    {
        "template": r"""Evaluate the definite integral:

$$\int_{{ lower }}^{{ upper }} ({{ integrand }}) \, dx$$

\textbf{a)} Find the antiderivative. \textbf{[3 marks]}

\textbf{b)} Apply the fundamental theorem of calculus. \textbf{[2 marks]}

\textbf{c)} Calculate the numerical value. \textbf{[2 marks]}""",
        "variables": [
            {
                "lower": 0, "upper": 2, "integrand": "x^2 + 1",
                "answer": "a) $\\frac{x^3}{3} + x$; b) $[\\frac{x^3}{3} + x]_0^2$; c) $\\frac{8}{3} + 2 - 0 = \\frac{14}{3}$"
            },
            {
                "lower": 1, "upper": 3, "integrand": "2x - 1", 
                "answer": "a) $x^2 - x$; b) $[x^2 - x]_1^3$; c) $(9-3) - (1-1) = 6$"
            },
            {
                "lower": 0, "upper": 1, "integrand": "e^x",
                "answer": "a) $e^x$; b) $[e^x]_0^1$; c) $e^1 - e^0 = e - 1$"
            }
        ],
        "marks": 7
    },
    {
        "template": r"""A statistics problem involving normal distribution.

Given: A population with mean $\mu = {{ mean }}$ and standard deviation $\sigma = {{ std }}$.

\textbf{a)} What is the probability that a randomly selected value is greater than {{ value1 }}? \textbf{[3 marks]}

\textbf{b)} Find the {{ percentile }}th percentile of this distribution. \textbf{[3 marks]}

\textbf{c)} If we take a sample of size {{ sample_size }}, what is the standard error of the mean? \textbf{[2 marks]}

Use the standard normal table or state your method clearly.""",
        "variables": [
            {
                "mean": 100, "std": 15, "value1": 115, "percentile": 90, "sample_size": 25,
                "answer": "a) Z = (115-100)/15 = 1, P(X>115) = P(Z>1) = 0.1587; b) 90th percentile: Z=1.28, X = 100+1.28(15) = 119.2; c) SE = 15/√25 = 3"
            },
            {
                "mean": 50, "std": 10, "value1": 65, "percentile": 75, "sample_size": 16,
                "answer": "a) Z = (65-50)/10 = 1.5, P(X>65) = P(Z>1.5) = 0.0668; b) 75th percentile: Z=0.67, X = 50+0.67(10) = 56.7; c) SE = 10/√16 = 2.5"
            }
        ],
        "marks": 8
    },
    {
        "question": r"""Prove that the series $\sum_{n=1}^{\infty} \frac{1}{n^2}$ converges using the integral test.

\textbf{a)} State the integral test conditions. \textbf{[2 marks]}

\textbf{b)} Verify that $f(x) = \frac{1}{x^2}$ satisfies these conditions for $x \geq 1$. \textbf{[3 marks]}

\textbf{c)} Evaluate the improper integral $\int_1^{\infty} \frac{1}{x^2} dx$. \textbf{[4 marks]}

\textbf{d)} State your conclusion about the series convergence. \textbf{[1 mark]}""",
        "answer": r"""a) Integral test: If $f(x)$ is positive, continuous, and decreasing for $x \geq N$, then $\sum f(n)$ and $\int f(x)dx$ have the same convergence behavior.

b) For $f(x) = \frac{1}{x^2}$ on $[1,\infty)$:
   - Positive: $\frac{1}{x^2} > 0$ for all $x \geq 1$
   - Continuous: polynomial in denominator, no zeros
   - Decreasing: $f'(x) = -\frac{2}{x^3} < 0$ for $x \geq 1$

c) $\int_1^{\infty} \frac{1}{x^2} dx = \lim_{t \to \infty} \int_1^t x^{-2} dx = \lim_{t \to \infty} [-x^{-1}]_1^t = \lim_{t \to \infty} (-\frac{1}{t} + 1) = 1$

d) Since the integral converges, the series $\sum_{n=1}^{\infty} \frac{1}{n^2}$ converges.""",
        "marks": 10
    }
]