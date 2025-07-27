"""
Sample Chemistry Questions for Setwise Quiz Generator

Demonstrates chemical equations, molecular structures, and calculations.
Usage: setwise generate --questions-file chemistry_questions.py
"""

# Multiple Choice Questions - Chemistry
mcq = [
    {
        "question": r"What is the molecular formula of glucose?",
        "options": [
            r"C$_6$H$_{12}$O$_6$",
            r"C$_6$H$_{10}$O$_5$", 
            r"C$_{12}$H$_{22}$O$_{11}$",
            r"C$_6$H$_6$O$_6$",
            r"C$_5$H$_{10}$O$_5$"
        ],
        "answer": r"C$_6$H$_{12}$O$_6$",
        "marks": 1
    },
    {
        "question": r"Which of the following represents the balanced equation for combustion of methane?",
        "options": [
            r"CH$_4$ + O$_2$ $\rightarrow$ CO$_2$ + H$_2$O",
            r"CH$_4$ + 2O$_2$ $\rightarrow$ CO$_2$ + 2H$_2$O",
            r"2CH$_4$ + 3O$_2$ $\rightarrow$ 2CO$_2$ + 3H$_2$O",
            r"CH$_4$ + 3O$_2$ $\rightarrow$ CO$_2$ + 2H$_2$O",
            r"CH$_4$ + O$_2$ $\rightarrow$ C + 2H$_2$O"
        ],
        "answer": r"CH$_4$ + 2O$_2$ $\rightarrow$ CO$_2$ + 2H$_2$O",
        "marks": 2
    },
    {
        "question": r"What is the pH of a 0.01 M HCl solution?",
        "options": [
            r"1",
            r"2", 
            r"12",
            r"13",
            r"7"
        ],
        "answer": r"2",
        "marks": 2
    },
    {
        "question": r"Which orbital has the highest energy in a multi-electron atom?",
        "options": [
            r"3s",
            r"3p",
            r"3d",
            r"4s",
            r"4p"
        ],
        "answer": r"4p",
        "marks": 2
    },
    {
        "question": r"The hybridization of carbon in methane (CH$_4$) is:",
        "options": [
            r"sp",
            r"sp$^2$",
            r"sp$^3$",
            r"sp$^3$d",
            r"sp$^3$d$^2$"
        ],
        "answer": r"sp$^3$",
        "marks": 2
    }
]

# Subjective Questions - Chemistry
subjective = [
    {
        "question": r"""Balance the following chemical equation and identify the type of reaction:

$$\text{Al} + \text{Fe}_2\text{O}_3 \rightarrow \text{Al}_2\text{O}_3 + \text{Fe}$$

\textbf{a)} Write the balanced equation with proper coefficients. \textbf{[3 marks]}

\textbf{b)} Identify the type of reaction and explain your reasoning. \textbf{[2 marks]}

\textbf{c)} Which element is oxidized and which is reduced? \textbf{[3 marks]}""",
        "answer": r"""a) Balanced equation: $2\text{Al} + \text{Fe}_2\text{O}_3 \rightarrow \text{Al}_2\text{O}_3 + 2\text{Fe}$

b) This is a single displacement (redox) reaction where aluminum displaces iron from iron oxide.

c) Aluminum is oxidized (0 to +3), Iron is reduced (+3 to 0)""",
        "marks": 8
    },
    {
        "template": r"""Calculate the molarity of a solution prepared by dissolving {{ mass }} g of {{ compound }} in {{ volume }} mL of water.

\textbf{Given:} Molecular weight of {{ compound }} = {{ mw }} g/mol

\textbf{a)} Calculate the number of moles of {{ compound }}. \textbf{[2 marks]}

\textbf{b)} Convert the volume to liters. \textbf{[1 mark]}

\textbf{c)} Calculate the molarity using M = moles/volume(L). \textbf{[2 marks]}""",
        "variables": [
            {
                "mass": 58.5, "compound": "NaCl", "volume": 250, "mw": 58.5,
                "answer": "a) moles = 58.5/58.5 = 1.0 mol; b) Volume = 250/1000 = 0.25 L; c) Molarity = 1.0/0.25 = 4.0 M"
            },
            {
                "mass": 40.0, "compound": "NaOH", "volume": 500, "mw": 40.0,
                "answer": "a) moles = 40.0/40.0 = 1.0 mol; b) Volume = 500/1000 = 0.5 L; c) Molarity = 1.0/0.5 = 2.0 M"
            },
            {
                "mass": 98.0, "compound": "H₂SO₄", "volume": 1000, "mw": 98.0,
                "answer": "a) moles = 98.0/98.0 = 1.0 mol; b) Volume = 1000/1000 = 1.0 L; c) Molarity = 1.0/1.0 = 1.0 M"
            }
        ],
        "marks": 5
    },
    {
        "template": r"""For the reaction: A$_2$ + 3B$_2$ $\rightarrow$ 2AB$_3$

If {{ reactant_amount }} mol of {{ reactant }} reacts completely:

\textbf{a)} How many moles of the other reactant are needed? \textbf{[2 marks]}

\textbf{b)} How many moles of product AB$_3$ will be formed? \textbf{[2 marks]}

\textbf{c)} If the actual yield is {{ yield_percent }}\%, calculate the actual moles of product obtained. \textbf{[2 marks]}""",
        "variables": [
            {
                "reactant_amount": 2, "reactant": "A₂", "yield_percent": 85,
                "answer": "a) 2 mol A₂ needs 6 mol B₂; b) 4 mol AB₃ formed; c) Actual = 4 × 0.85 = 3.4 mol"
            },
            {
                "reactant_amount": 6, "reactant": "B₂", "yield_percent": 92,
                "answer": "a) 6 mol B₂ needs 2 mol A₂; b) 4 mol AB₃ formed; c) Actual = 4 × 0.92 = 3.68 mol"
            }
        ],
        "marks": 6
    },
    {
        "question": r"""Explain the concept of chemical equilibrium using Le Chatelier's principle.

\textbf{Consider the reaction:} N$_2$(g) + 3H$_2$(g) $\rightleftharpoons$ 2NH$_3$(g) + heat

\textbf{a)} State Le Chatelier's principle. \textbf{[2 marks]}

\textbf{b)} Predict the effect of the following changes on the equilibrium position:
\begin{itemize}
\item Increasing temperature \textbf{[2 marks]}
\item Increasing pressure \textbf{[2 marks]}
\item Adding more N$_2$ \textbf{[2 marks]}
\item Removing NH$_3$ \textbf{[2 marks]}
\end{itemize}""",
        "answer": r"""a) Le Chatelier's principle: When a system at equilibrium is disturbed, it will shift to counteract the disturbance.

b) Effects:
- Increasing temperature: Shifts left (endothermic direction) to absorb heat
- Increasing pressure: Shifts right (fewer gas molecules side) to reduce pressure  
- Adding N₂: Shifts right to consume excess N₂
- Removing NH₃: Shifts right to replace removed NH₃""",
        "marks": 10
    }
]