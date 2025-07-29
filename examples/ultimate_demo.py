# Ultimate Setwise Demo - All Features Showcase
# Demonstrates: templated questions, multi-part problems, matrices, chemistry, circuits, SI units, tables, plots

quiz_metadata = {
    "title": "Ultimate Setwise Demo Quiz",
    "subject": "Science & Engineering",
    "duration": "90 minutes",
    "total_marks": 50,
    "instructions": ["Show all working clearly", "Use appropriate units", "Include diagrams where helpful", "Round to 2 decimal places where needed"]
}

mcq = [
    {
        "template": r"""
Calculate {{ a }} $\times$ {{ b }} = ?""",
        "options": [
            r"{{ a * b }}",
            r"{{ a + b }}",
            r"{{ a - b }}",
            r"{{ (a * b) + 1 }}"
        ],
        "answer": r"{{ a * b }}",
        "variables": [
            {"a": 12, "b": 8},
            {"a": 15, "b": 6},
            {"a": 9, "b": 11}
        ],
        "marks": 2
    },
    {
        "question": r"""
Consider the matrix:
\begin{equation}
A = \begin{pmatrix}
3 & 1 \\
2 & 4
\end{pmatrix}
\end{equation}
What is $\det(A)$?""",
        "options": [r"10", r"12", r"14", r"8"],
        "answer": r"10",
        "marks": 3
    },
    {
        "question": r"""
The RC circuit shown has time constant:
\begin{center}
\begin{circuitikz}[scale=0.8]
\draw (0,0) to[V, l=$V_0$] (0,2) to[R, l=\SI{10}{\kilo\ohm}] (3,2) to[C, l=\SI{100}{\micro\farad}] (3,0) -- (0,0);
\end{circuitikz}
\end{center}
What is $\tau$?""",
        "options": [r"\SI{1}{\second}", r"\SI{0.1}{\second}", r"\SI{10}{\second}", r"\SI{0.01}{\second}"],
        "answer": r"\SI{1}{\second}",
        "marks": 4
    },
    {
        "template": r"""
If a circle has radius {{ r }} cm, what is its area using $\pi = 3.14$?""",
        "options": [
            r"${{ 3.14 * r * r }}$ cm$^2$",
            r"${{ 2 * 3.14 * r }}$ cm$^2$",
            r"${{ 3.14 * r }}$ cm$^2$",
            r"${{ r * r }}$ cm$^2$"
        ],
        "answer": r"${{ 3.14 * r * r }}$ cm$^2$",
        "variables": [
            {"r": 5},
            {"r": 7},
            {"r": 10}
        ],
        "marks": 3
    }
]

subjective = [
    {
        "template": r"Physics Problem - Projectile Motion with velocity {{ v0 }} m/s at {{ angle }}$^\circ$:",
        "parts": [
            {
                "question": r"Calculate the maximum height reached (use $g = \SI{9.8}{\meter\per\second\squared}$).",
                "answer": r"$h = \frac{(v_0 \sin\theta)^2}{2g} = \frac{({{ v0 }} \sin {{ angle }}°)^2}{2 \times 9.8} = {{ (v0 * sin_angle)**2 / (2 * 9.8) | round(1) }}$ m",
                "marks": 4
            },
            {
                "question": r"Find the time of flight.",
                "answer": r"$t = \frac{2v_0 \sin\theta}{g} = \frac{2 \times {{ v0 }} \times \sin {{ angle }}°}{9.8} = {{ 2 * v0 * sin_angle / 9.8 | round(2) }}$ s",
                "marks": 3
            }
        ],
        "variables": [
            {"v0": 20, "angle": 30, "sin_angle": 0.5},
            {"v0": 25, "angle": 45, "sin_angle": 0.707}
        ],
        "marks": 7
    },
    {
        "question": r"""
Chemical Analysis - Consider ethanol:
\begin{center}
\chemfig{H-C(-[2]H)(-[6]H)-C(-[2]H)(-[6]H)-OH}
\end{center}""",
        "parts": [
            {
                "question": r"What is the molecular formula?",
                "answer": r"C$_2$H$_6$O (or C$_2$H$_5$OH)",
                "marks": 2
            },
            {
                "question": r"Calculate the molar mass using atomic masses: C=12, H=1, O=16.",
                "answer": r"Molar mass = $2 \times 12 + 6 \times 1 + 1 \times 16 = 24 + 6 + 16 = 46$ g/mol",
                "marks": 3
            },
            {
                "question": r"How many moles are in 92g of ethanol?",
                "answer": r"$n = \frac{m}{M} = \frac{92}{46} = 2$ moles",
                "marks": 2
            }
        ],
        "marks": 7
    },
    {
        "question": r"""
Data Analysis - Material Properties:
\begin{center}
\begin{tabular}{|l|c|c|c|}
\hline
\textbf{Material} & \textbf{Density} & \textbf{Young's Modulus} & \textbf{Yield Strength} \\
& \textbf{(\si{\gram\per\cubic\centi\meter})} & \textbf{(\si{\giga\pascal})} & \textbf{(\si{\mega\pascal})} \\
\hline
Steel & 7.85 & 200 & 250 \\
\hline
Aluminum & 2.70 & 70 & 95 \\
\hline
Titanium & 4.50 & 110 & 880 \\
\hline
\multirow{2}{*}{Carbon Fiber} & \multirow{2}{*}{1.60} & 150 & 1200 \\
& & (fiber direction) & (tensile) \\
\hline
\end{tabular}
\end{center}""",
        "parts": [
            {
                "question": r"Calculate the specific strength (yield strength/density) for each material.",
                "answer": r"Steel: $250/7.85 = 31.8$ MPa·cm³/g\nAluminum: $95/2.70 = 35.2$ MPa·cm³/g\nTitanium: $880/4.50 = 195.6$ MPa·cm³/g\nCarbon Fiber: $1200/1.60 = 750$ MPa·cm³/g",
                "marks": 6
            },
            {
                "question": r"Which material would you choose for aerospace applications and justify your choice.",
                "answer": r"Carbon fiber has the highest specific strength (750 MPa·cm³/g), making it ideal for aerospace where weight reduction is critical. However, cost and manufacturing complexity must be considered.",
                "marks": 4
            }
        ],
        "marks": 10
    },
    {
        "question": r"""
Advanced Mathematics - Matrix Operations:
\begin{equation}
\text{Given: } A = \begin{pmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 1 & 2 \end{pmatrix}, \quad \mathbf{b} = \begin{pmatrix} 5 \\ 8 \\ 3 \end{pmatrix}
\end{equation}""",
        "parts": [
            {
                "question": r"Calculate $\det(A)$ using cofactor expansion.",
                "answer": r"$\det(A) = 2(3 \times 2 - 1 \times 1) - 1(1 \times 2 - 0 \times 1) + 0 = 2(5) - 1(2) = 8$",
                "marks": 4
            },
            {
                "question": r"Solve the system $A\mathbf{x} = \mathbf{b}$ for the first component $x_1$.",
                "answer": r"Using Cramer's rule: $x_1 = \frac{\det(A_1)}{\det(A)}$ where $A_1$ has first column replaced by $\mathbf{b}$.\n$\det(A_1) = 16$, so $x_1 = 16/8 = 2$",
                "marks": 5
            }
        ],
        "marks": 9
    },
    {
        "question": r"""
Experimental Data Analysis:
\begin{center}
\begin{tikzpicture}
\begin{axis}[
    xlabel={Temperature (\si{\celsius})},
    ylabel={Reaction Rate (\si{\mole\per\liter\per\second})},
    width=10cm,
    height=7cm,
    grid=both,
    legend pos=north west
]
\addplot[blue, mark=*, mark size=2pt] coordinates {
    (20, 0.05) (30, 0.15) (40, 0.45) (50, 1.35) (60, 4.05)
};
\addplot[red, dashed, thick, domain=20:60] {0.00167*exp(0.1099*x)};
\legend{Experimental Data, Arrhenius Fit: $k = Ae^{-E_a/RT}$}
\end{axis}
\end{tikzpicture}
\end{center}""",
        "parts": [
            {
                "question": r"What type of relationship exists between temperature and reaction rate?",
                "answer": r"Exponential relationship following Arrhenius equation: $k = Ae^{-E_a/RT}$, where rate increases exponentially with temperature.",
                "marks": 3
            },
            {
                "question": r"Estimate the rate at \SI{35}{\celsius} using the trend.",
                "answer": r"From the exponential fit, at 35°C the rate would be approximately \SI{0.25}{\mole\per\liter\per\second}",
                "marks": 2
            },
            {
                "question": r"Explain why this relationship is important in chemical kinetics.",
                "answer": r"The Arrhenius relationship shows that small temperature increases can dramatically increase reaction rates, which is crucial for controlling reaction conditions in industrial processes and understanding biological systems.",
                "marks": 3
            }
        ],
        "marks": 8
    }
]