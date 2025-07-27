"""
Sample Physics Questions for Setwise Quiz Generator

This demonstrates how to create custom question libraries for different subjects.
You can place this file anywhere and use it with: 
setwise generate --questions-file physics_questions.py
"""

# Multiple Choice Questions - Physics
mcq = [
    {
        "question": r"What is the speed of light in vacuum?",
        "options": [
            r"299,792,458 m/s",
            r"300,000,000 m/s", 
            r"186,000 miles/s",
            r"3.00 × 10^8 m/s",
            r"2.99 × 10^8 m/s"
        ],
        "answer": r"299,792,458 m/s",
        "marks": 2
    },
    {
        "question": r"According to Newton's first law of motion, an object at rest will:",
        "options": [
            r"Always remain at rest",
            r"Remain at rest unless acted upon by an external force",
            r"Start moving spontaneously",
            r"Accelerate due to gravity",
            r"Change direction randomly"
        ],
        "answer": r"Remain at rest unless acted upon by an external force",
        "marks": 1
    },
    {
        "question": r"The unit of electric charge is:",
        "options": [
            r"Ampere (A)",
            r"Volt (V)",
            r"Coulomb (C)", 
            r"Ohm (Ω)",
            r"Watt (W)"
        ],
        "answer": r"Coulomb (C)",
        "marks": 1
    },
    {
        "question": r"Which of the following is a scalar quantity?",
        "options": [
            r"Velocity",
            r"Acceleration",
            r"Force",
            r"Temperature",
            r"Displacement"
        ],
        "answer": r"Temperature",
        "marks": 2
    },
    {
        "question": r"The frequency of a wave is 50 Hz. What is its period?",
        "options": [
            r"0.02 s",
            r"0.2 s",
            r"2 s", 
            r"50 s",
            r"Cannot be determined"
        ],
        "answer": r"0.02 s",
        "marks": 2
    }
]

# Subjective Questions - Physics
subjective = [
    {
        "question": r"""Derive the kinematic equation $v^2 = u^2 + 2as$ starting from the basic equations of motion.

\textbf{Given equations:}
\begin{align}
v &= u + at\\
s &= ut + \frac{1}{2}at^2
\end{align}

Show all steps clearly.""",
        "answer": r"""From the first equation: $t = \frac{v-u}{a}$

Substituting into the second equation:
$s = u \cdot \frac{v-u}{a} + \frac{1}{2}a \left(\frac{v-u}{a}\right)^2$

Simplifying:
$s = \frac{u(v-u)}{a} + \frac{(v-u)^2}{2a}$

$s = \frac{2u(v-u) + (v-u)^2}{2a} = \frac{(v-u)(2u + v - u)}{2a} = \frac{(v-u)(v+u)}{2a}$

$s = \frac{v^2 - u^2}{2a}$

Therefore: $v^2 = u^2 + 2as$""",
        "marks": 8
    },
    {
        "template": r"""A projectile is launched at an angle of {{ angle }}° with an initial velocity of {{ velocity }} m/s.

\textbf{a)} Calculate the horizontal and vertical components of the initial velocity. \textbf{[3 marks]}

\textbf{b)} Find the time of flight assuming the projectile lands at the same height. \textbf{[4 marks]}

\textbf{c)} Calculate the maximum range. \textbf{[3 marks]}

Use $g = 9.8 \text{ m/s}^2$.""",
        "variables": [
            {
                "angle": 30, "velocity": 20,
                "answer": "a) vₓ = 20cos30° = 17.32 m/s, vᵧ = 20sin30° = 10 m/s; b) t = 2vᵧ/g = 2.04 s; c) R = v²sin(2θ)/g = 35.35 m"
            },
            {
                "angle": 45, "velocity": 25, 
                "answer": "a) vₓ = 25cos45° = 17.68 m/s, vᵧ = 25sin45° = 17.68 m/s; b) t = 2vᵧ/g = 3.61 s; c) R = v²sin(2θ)/g = 63.78 m"
            },
            {
                "angle": 60, "velocity": 15,
                "answer": "a) vₓ = 15cos60° = 7.5 m/s, vᵧ = 15sin60° = 12.99 m/s; b) t = 2vᵧ/g = 2.65 s; c) R = v²sin(2θ)/g = 19.89 m"
            }
        ],
        "marks": 10
    },
    {
        "template": r"""An electric circuit contains a resistor of {{ resistance }} Ω connected to a {{ voltage }} V battery.

\textbf{a)} Calculate the current flowing through the circuit using Ohm's law. \textbf{[2 marks]}

\textbf{b)} Find the power dissipated in the resistor. \textbf{[3 marks]}

\textbf{c)} If the circuit operates for {{ time }} hours, calculate the energy consumed in kWh. \textbf{[3 marks]}""",
        "variables": [
            {
                "resistance": 10, "voltage": 12, "time": 2,
                "answer": "a) I = V/R = 12/10 = 1.2 A; b) P = I²R = 1.44 × 10 = 14.4 W; c) E = Pt = 14.4 × 2 = 28.8 Wh = 0.0288 kWh"
            },
            {
                "resistance": 25, "voltage": 9, "time": 3,
                "answer": "a) I = V/R = 9/25 = 0.36 A; b) P = I²R = 0.1296 × 25 = 3.24 W; c) E = Pt = 3.24 × 3 = 9.72 Wh = 0.00972 kWh"
            }
        ],
        "marks": 8
    },
    {
        "question": r"""Compare and contrast the wave and particle theories of light. Discuss at least two experimental observations that support each theory.

\textbf{Structure your answer as follows:}
\begin{enumerate}
\item Wave theory characteristics and supporting experiments
\item Particle theory characteristics and supporting experiments  
\item Modern understanding (wave-particle duality)
\end{enumerate}""",
        "answer": r"""1. Wave Theory: Light exhibits interference, diffraction, and polarization. Supported by Young's double-slit experiment and diffraction gratings.

2. Particle Theory: Light consists of discrete photons with energy E=hf. Supported by photoelectric effect and Compton scattering.

3. Modern Understanding: Light exhibits wave-particle duality - behaves as waves in propagation and particles in interactions. This is described by quantum mechanics.""",
        "marks": 12
    }
]