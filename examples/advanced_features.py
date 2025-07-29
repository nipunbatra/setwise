# Advanced LaTeX Features Example
# Demonstrates images, matrices, chemistry, circuits, and more

quiz_metadata = {
    "title": "Advanced LaTeX Features Quiz",
    "subject": "Science & Engineering",
    "duration": "90 minutes",
    "total_marks": 50,
    "instructions": ["Show all working", "Use proper units", "Include diagrams where helpful"]
}

mcq = [
    {
        "question": r"""
Consider the matrix:
\begin{equation}
A = \begin{pmatrix}
2 & -1 & 0 \\
-1 & 2 & -1 \\
0 & -1 & 2
\end{pmatrix}
\end{equation}
What is the determinant of matrix A?""",
        "options": [r"4", r"6", r"8", r"2"],
        "answer": r"4",
        "marks": 4
    },
    {
        "question": r"""
The chemical reaction for photosynthesis can be represented as:
\begin{center}
\chemfig{6CO_2} + \chemfig{6H_2O} $\xrightarrow{\text{light}}$ \chemfig{C_6H_{12}O_6} + \chemfig{6O_2}
\end{center}
How many molecules of glucose are produced from 12 molecules of CO$_2$?""",
        "options": [r"1", r"2", r"6", r"12"],
        "answer": r"2",
        "marks": 3
    },
    {
        "question": r"""
In the RC circuit shown below:
\begin{center}
\begin{circuitikz}
\draw (0,0) to[V, l=$V_0$] (0,2) to[R, l=$R$] (3,2) to[C, l=$C$] (3,0) -- (0,0);
\end{circuitikz}
\end{center}
What is the time constant $\tau$?""",
        "options": [r"$RC$", r"$\frac{R}{C}$", r"$\frac{C}{R}$", r"$R + C$"],
        "answer": r"$RC$",
        "marks": 3
    },
    {
        "question": r"""
Consider the data plot:
\begin{center}
\begin{tikzpicture}
\begin{axis}[
    xlabel={Time (s)},
    ylabel={Velocity (m/s)},
    width=8cm,
    height=6cm,
    grid=both
]
\addplot coordinates {(0,0) (1,2) (2,4) (3,6) (4,8)};
\end{axis}
\end{tikzpicture}
\end{center}
What is the acceleration?""",
        "options": [r"\SI{1}{\meter\per\second\squared}", r"\SI{2}{\meter\per\second\squared}", r"\SI{4}{\meter\per\second\squared}", r"\SI{8}{\meter\per\second\squared}"],
        "answer": r"\SI{2}{\meter\per\second\squared}",
        "marks": 4
    },
    {
        "template": r"""
Calculate the area under the curve $y = {{ function }}$ from $x = 0$ to $x = {{ limit }}$:
\begin{center}
\begin{tikzpicture}
\begin{axis}[
    domain=0:{{ limit }},
    samples=100,
    xlabel={$x$},
    ylabel={$y$},
    width=8cm,
    height=6cm
]
\addplot[blue, thick] {{{ function_plot }}};
\addplot[fill=blue, opacity=0.3] {{{ function_plot }}} \closedcycle;
\end{axis}
\end{tikzpicture}
\end{center}""",
        "options": [
            r"${{ result }}$",
            r"${{ result * 2 }}$",
            r"${{ result / 2 }}$",
            r"${{ result + 1 }}$"
        ],
        "answer": r"${{ result }}$",
        "variables": [
            {"function": "x^2", "function_plot": "x^2", "limit": 2, "result": "8/3"},
            {"function": "2x", "function_plot": "2*x", "limit": 3, "result": 9}
        ],
        "marks": 5
    }
]

subjective = [
    {
        "question": r"""
Analyze the molecular structure:
\begin{center}
\chemfig{H-C(-[2]H)(-[6]H)-C(-[2]H)(-[6]H)-OH}
\end{center}""",
        "parts": [
            {
                "question": r"Name this organic compound.",
                "answer": r"Ethanol (C$_2$H$_5$OH)",
                "marks": 2
            },
            {
                "question": r"What is the molecular formula?",
                "answer": r"C$_2$H$_6$O",
                "marks": 2
            },
            {
                "question": r"Draw the structural isomer of this compound.",
                "answer": r"Dimethyl ether: \chemfig{H-C(-[2]H)(-[6]H)-O-C(-[2]H)(-[6]H)-H}",
                "marks": 3
            }
        ],
        "marks": 7
    },
    {
        "question": r"""
Given the system of equations in matrix form:
\begin{equation}
\begin{pmatrix}
2 & 1 & -1 \\
-3 & -1 & 2 \\
-2 & 1 & 2
\end{pmatrix}
\begin{pmatrix}
x \\ y \\ z
\end{pmatrix}
=
\begin{pmatrix}
8 \\ -11 \\ -3
\end{pmatrix}
\end{equation}""",
        "parts": [
            {
                "question": r"Solve for $x$, $y$, and $z$ using matrix methods.",
                "answer": r"Using Gaussian elimination or Cramer's rule: $x = 2$, $y = 3$, $z = -1$",
                "marks": 6
            },
            {
                "question": r"Verify your solution by substitution.",
                "answer": r"$2(2) + 1(3) + (-1)(-1) = 4 + 3 + 1 = 8$ ✓\n$-3(2) + (-1)(3) + 2(-1) = -6 - 3 - 2 = -11$ ✓\n$-2(2) + 1(3) + 2(-1) = -4 + 3 - 2 = -3$ ✓",
                "marks": 3
            }
        ],
        "marks": 9
    },
    {
        "question": r"""
Consider the data table:
\begin{center}
\begin{tabular}{|c|c|c|}
\hline
\textbf{Material} & \textbf{Density (\si{\gram\per\cubic\centi\meter})} & \textbf{Young's Modulus (\si{\giga\pascal})} \\
\hline
Steel & 7.85 & 200 \\
\hline
Aluminum & 2.70 & 70 \\
\hline
Copper & 8.96 & 110 \\
\hline
\multirow{2}{*}{Composite} & \multirow{2}{*}{1.60} & 150 \\
& & (fiber direction) \\
\hline
\end{tabular}
\end{center}""",
        "parts": [
            {
                "question": r"Calculate the specific strength (Young's Modulus / Density) for each material.",
                "answer": r"Steel: $200/7.85 = 25.5$ GPa·cm³/g\nAluminum: $70/2.70 = 25.9$ GPa·cm³/g\nCopper: $110/8.96 = 12.3$ GPa·cm³/g\nComposite: $150/1.60 = 93.8$ GPa·cm³/g",
                "marks": 4
            },
            {
                "question": r"Which material has the highest specific strength and why is this important?",
                "answer": r"The composite material has the highest specific strength (93.8 GPa·cm³/g). This is important for aerospace applications where high strength-to-weight ratio is crucial for fuel efficiency and performance.",
                "marks": 3
            }
        ],
        "marks": 7
    },
    {
        "question": r"""
Analyze the experimental data shown in the graph:
\begin{center}
\begin{tikzpicture}
\begin{axis}[
    xlabel={Temperature (\si{\celsius})},
    ylabel={Reaction Rate (\si{\mole\per\liter\per\second})},
    width=10cm,
    height=8cm,
    grid=both,
    legend pos=north west
]
\addplot[blue, mark=*, mark size=2pt] coordinates {
    (20, 0.1) (30, 0.2) (40, 0.4) (50, 0.8) (60, 1.6) (70, 3.2)
};
\addplot[red, dashed, thick] {0.0125*exp(0.0693*x)};
\legend{Experimental Data, Arrhenius Fit}
\end{axis}
\end{tikzpicture}
\end{center}""",
        "parts": [
            {
                "question": r"What type of relationship exists between temperature and reaction rate?",
                "answer": r"An exponential relationship following the Arrhenius equation: $k = A e^{-E_a/RT}$",
                "marks": 3
            },
            {
                "question": r"Estimate the activation energy if the rate doubles every 10°C increase.",
                "answer": r"Using the rule of thumb for temperature coefficient: $E_a \approx 53$ kJ/mol",
                "marks": 4
            }
        ],
        "marks": 7
    }
]